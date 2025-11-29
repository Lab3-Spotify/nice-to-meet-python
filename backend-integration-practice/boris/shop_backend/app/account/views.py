# account/views.py
from decimal import Decimal

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import transaction
from django.db.models import F
from rest_framework.permissions import IsAuthenticated, AllowAny

from utils.views import BaseAPIView
from utils.response import APISuccessResponse, APIFailedResponse
from utils.constants import ResponseCode, ResponseMessage

from account.models import UserProfile, UserType
from account.serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    DepositSerializer,
)
from market.models import Cart

User = get_user_model()


# (gpt建議的)處理username=name後不可重複function
def _generate_unique_username(base: str) -> str:
    base = (base or "").strip() or "user"
    candidate = base
    counter = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}{counter}"
        counter += 1
    return candidate

class RegisterView(BaseAPIView):
    """
    註冊帳號：
     1. 建 Django User
     2. 建 UserProfile
     3. 建 Cart
     4. 回傳 Profile 資訊
    """
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        name = serializer.validated_data["name"]
        phone = serializer.validated_data.get("phone", "")
        user_type = UserType.BASIC

        # 1. 建 Django User
        username = _generate_unique_username(name)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
        )

        # 2. 建 UserProfile
        profile = UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email,
            type=user_type,
            balance=Decimal("0.00"),
        )

        # 3. 建 Cart (一人一車)
        Cart.objects.create(user=user)

        # 4. 註冊完成後自動登入
        login(request, user)

        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
            msg="註冊成功",
        )


class LoginView(BaseAPIView):
    """
    登入：
     1. 用 UserProfile.email 找人
     2. 確認 user.is_active
     3. authenticate 檢查密碼
     4. login 建 session
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # 1. 用 UserProfile 對到 user
        try:
            profile = UserProfile.objects.select_related("user").get(email=email)
        except UserProfile.DoesNotExist:
            return APIFailedResponse(
                code=ResponseCode.USER_NOT_FOUND,
                msg=ResponseMessage.USER_NOT_FOUND,
                details={"email": email},
            )

        # 2. 檢查啟用狀態
        if not profile.user.is_active:
            return APIFailedResponse(
                code=ResponseCode.USER_INACTIVE,
                msg="用戶已被停用",
            )

        # 3. 驗證密碼
        user = authenticate(
            request,
            username=profile.user.username,
            password=password,
        )
        if not user:
            return APIFailedResponse(
                code=ResponseCode.UNAUTHORIZED,
                msg="帳號或密碼錯誤",
            )

        # 4. 建 session
        login(request, user)

        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
            msg="登入成功",
        )


class LogoutView(BaseAPIView):
    """
    登出：清掉 session
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return APISuccessResponse(
            msg="已登出",
        )


class MeView(BaseAPIView):
    """
    讀寫自己的資料
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
        )

    @transaction.atomic
    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get("name")
        phone = serializer.validated_data.get("phone")
        new_email = serializer.validated_data.get("email")
        new_type = serializer.validated_data.get("type")

        # 1. 先改單純欄位
        if name is not None:
            profile.name = name
        if phone is not None:
            profile.phone = phone
        if new_type is not None:
            profile.type = new_type

        # 2. 如果要改 email，就要做唯一性檢查 + 同步到 Django User
        if new_email is not None:
            # 檢查 Django User 是否已用這個 email
            if User.objects.filter(email__iexact=new_email).exclude(pk=profile.user.pk).exists():
                return APIFailedResponse(
                    code=ResponseCode.CONFLICT,
                    msg="Email 已被使用",
                )
            # 檢查 UserProfile 是否已用這個 email
            if UserProfile.objects.filter(email__iexact=new_email).exclude(pk=profile.pk).exists():
                return APIFailedResponse(
                    code=ResponseCode.CONFLICT,
                    msg="Email 已被使用",
                )

            # 同步三個欄位
            profile.email = new_email
            profile.user.email = new_email
            profile.user.save(update_fields=["email", "username"])

        profile.save()

        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
            msg="更新成功",
        )


class DepositView(BaseAPIView):
    """
    儲值 / 加值
    """
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        profile = request.user.profile

        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        # 驗證金額
        if amount <= 0:
            return APIFailedResponse(
                code=ResponseCode.VALIDATION_ERROR,
                msg="儲值金額必須大於0",
            )

        # 原子性更新餘額
        UserProfile.objects.filter(pk=profile.pk).update(
            balance=F("balance") + amount
        )

        profile.refresh_from_db(fields=["balance"])

        return APISuccessResponse(
            data={"balance": str(profile.balance)},
            msg="儲值成功",
        )
