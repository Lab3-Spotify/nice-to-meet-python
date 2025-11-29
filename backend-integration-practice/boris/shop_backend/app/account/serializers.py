from rest_framework import serializers
from account.models import UserProfile, UserType
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.Serializer):
    """
    註冊時的輸入驗證：
    - email
    - password
    - name
    - phone
    - type
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    
    def validate_email(self, value):
        """
        建帳號前先確認此email在User和UserProfile都沒被用過
        """
        User = get_user_model()

        # 檢查 Django User
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email 已被使用")

        # 檢查 UserProfile
        if UserProfile.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email 已被使用")

        return value


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
    email = serializers.EmailField(required=False)
    type = serializers.ChoiceField(
        choices=UserType.choices,
        required=False,
    )


class DepositSerializer(serializers.Serializer):
    """
    儲值用的輸入驗證 (POST /deposit)。
    """
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)