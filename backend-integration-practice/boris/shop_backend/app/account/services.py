from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

from account.models import UserProfile, UserType
from market.models import Cart
User = get_user_model()


@transaction.atomic
def create_profile_with_user(
    *,
    email: str,
    password: str,
    name: str,
    phone: str = "",
    user_type: str = UserType.BASIC,
) -> UserProfile:
    """
    建立一個完整的新會員：
    1. 建 Django User
    2. 建 UserProfile 綁上這個 User
    3. 產生一台購物車Cart
    回傳 UserProfile
    """
    # 1. 建 Django 的內建 User
    user = User.objects.create_user(
        username=email,      # 我們用 email 當 username
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

    # 3. 綁購物車 (一人一車)
    Cart.objects.create(user=user)

    return profile


@transaction.atomic
def update_profile_and_email_sync(
    *,
    profile: UserProfile,
    name=None,
    phone=None,
    new_email=None,
    new_type=None,
) -> UserProfile:
    """
    更新會員資料。
    - 更新 name / phone / type
    - 如果 new_email 有提供則做以下處理：
        1. 檢查是否重複
        2. 同步更新 UserProfile.email
        3. 同步更新 Django User.email / username
    """
    if name is not None:
        profile.name = name

    if phone is not None:
        profile.phone = phone

    if new_type is not None:
        profile.type = new_type

    if new_email is not None:
        # 檢查是否有人已經使用這個 email
        UserModel = get_user_model()
        if UserModel.objects.filter(email__iexact=new_email).exclude(pk=profile.user.pk).exists():
            raise ValueError("Email 已被使用")
        if UserProfile.objects.filter(email__iexact=new_email).exclude(pk=profile.pk).exists():
            raise ValueError("Email 已被使用")

        # 同步 UserProfile 與 Django User
        profile.email = new_email
        profile.user.email = new_email
        profile.user.username = new_email  # 如果 username 與 email 綁定
        profile.user.save(update_fields=["email", "username"])

    profile.save()
    return profile


@transaction.atomic
def deposit_balance(
    *,
    profile: UserProfile,
    amount: Decimal,
) -> UserProfile:
    """
    儲值餘額：將 amount 加到 profile.balance。
    不留交易歷史表。
    """
    if amount <= 0:
        raise ValueError("儲值金額必須大於0")

    # 用 F() 確保原子性，避免競態條件
    UserProfile.objects.filter(pk=profile.pk).update(
        balance=F("balance") + amount
    )

    profile.refresh_from_db(fields=["balance"])
    return profile