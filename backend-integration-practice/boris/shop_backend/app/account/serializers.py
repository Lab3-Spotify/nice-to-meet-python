from rest_framework import serializers
from account.models import UserProfile, UserType


class RegisterSerializer(serializers.Serializer):
    """
    註冊時的輸入驗證：
    - email
    - password
    - name
    - phone (可選)
    - type  (可選，預設 BASIC)
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    type = serializers.ChoiceField(
        choices=UserType.choices,
        required=False,
    )


class LoginSerializer(serializers.Serializer):
    """
    登入時的輸入驗證：
    - email
    - password
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    """
    回傳會員資料給前端時使用。
    注意：auth_email 是從 Django User 取來的登入信箱。
    email   則是 UserProfile.email
    """
    auth_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "auth_email",
            "type",
            "balance",
            "created_at",
            "updated_at",
        ]


class ProfileUpdateSerializer(serializers.Serializer):
    """
    更新個資 (PATCH /me) 用的輸入驗證。
    全部欄位都可選，因為是 partial update。
    email -> 如果要更新 email，會被當成 new_email，後續會同步到 Django User。
    """
    name = serializers.CharField(max_length=120, required=False)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    email = serializers.EmailField(required=False)  # new_email
    type = serializers.ChoiceField(
        choices=UserType.choices,
        required=False,
    )


class DepositSerializer(serializers.Serializer):
    """
    儲值用的輸入驗證 (POST /deposit)。
    """
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)