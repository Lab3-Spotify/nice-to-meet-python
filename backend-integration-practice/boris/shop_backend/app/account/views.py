from django.contrib.auth import authenticate, login, logout
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
from account.services import (
    create_profile_with_user,
    update_profile_and_email_sync,
    deposit_balance,
)


class RegisterView(BaseAPIView):
    """
    註冊帳號：
     1. 建 UserProfile和Django User
     2. 建 Cart
     3. 回傳 Profile 資訊
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        name = serializer.validated_data["name"]
        phone = serializer.validated_data.get("phone", "")
        user_type = serializer.validated_data.get("type", UserType.BASIC)

        # 呼叫 service 進行實際建立
        profile = create_profile_with_user(
            email=email,
            password=password,
            name=name,
            phone=phone,
            user_type=user_type,
        )

        # 註冊完成後自動登入
        login(request, profile.user)

        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
            msg="註冊成功",
        )


class LoginView(BaseAPIView):
    """
    登入：
     1. 用 UserProfile.email 找人
     2. 確認該 user.is_active
     3. 驗證密碼
     4. 成功後 login() 建 session
     5. 回傳該使用者的 Profile 資料
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # 用UserProfile對User
        try:
            profile = UserProfile.objects.select_related("user").get(email=email)
        except UserProfile.DoesNotExist:
            return APIFailedResponse(
                code=ResponseCode.USER_NOT_FOUND,
                msg=ResponseMessage.USER_NOT_FOUND,
                details={"email": email},
            )

        # 檢查是否啟用
        if not profile.user.is_active:
            return APIFailedResponse(
                code=ResponseCode.USER_INACTIVE,
                msg="用戶已被停用",
            )

        # 驗證密碼
        # 預設authenticate() 走 username/password。
        # 在create_profile_with_user() 時，把 username 設成 email。
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

        # 建session
        login(request, user)

        # 回傳profile資訊
        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
            msg="登入成功",
        )


class LogoutView(BaseAPIView):
    """
    登出：
     1. 需要已登入（IsAuthenticated）
     2. 呼叫 logout() 清掉 session
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return APISuccessResponse(
            msg="已登出",
        )


class MeView(BaseAPIView):
    """
    讀寫自己的資料：
    GET  -> 回傳自己的Profile
    PATCH -> 更新name/phone/type/email
    若 email 有更新會同步到 Django User
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        return APISuccessResponse(
            data=ProfileSerializer(profile).data,
        )

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            updated_profile = update_profile_and_email_sync(
                profile=profile,
                name=serializer.validated_data.get("name"),
                phone=serializer.validated_data.get("phone"),
                new_email=serializer.validated_data.get("email"),
                new_type=serializer.validated_data.get("type"),
            )
        except ValueError as e:
            # 如email已被使用
            return APIFailedResponse(
                code=ResponseCode.EMAIL_IN_USE,
                msg=str(e),
            )

        return APISuccessResponse(
            data=ProfileSerializer(updated_profile).data,
            msg="更新成功",
        )


class DepositView(BaseAPIView):
    """
    加值 / 儲值 API：
     1. 驗證 amount > 0
     2. 呼叫 deposit_balance()
     3. 回傳更新後餘額
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile

        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        try:
            updated_profile = deposit_balance(
                profile=profile,
                amount=amount,
            )
        except ValueError as e:
            # 通常是 amount <= 0
            return APIFailedResponse(
                code=ResponseCode.INVALID_AMOUNT,
                msg=str(e),
            )

        return APISuccessResponse(
            data={"balance": str(updated_profile.balance)},
            msg="儲值成功",
        )
