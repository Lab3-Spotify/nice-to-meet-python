from decimal import Decimal
from django.conf import settings
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True 

class UserType(models.TextChoices):
    BASIC = "BASIC", "一般"
    VIP   = "VIP", "VIP"
    ADMIN = "ADMIN", "管理員"

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="profile",)

    name   = models.CharField(max_length=120)
    phone  = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)  # 允許 NULL
    type   = models.CharField(max_length=20, choices=UserType.choices, default=UserType.BASIC)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00")) 

    class Meta:
        db_table = "userprofile"
        indexes = [models.Index(fields=["email"]), models.Index(fields=["type"])]
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=Decimal("0.00")), name="userprofile_balance_non_negative"),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"

