# account/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 列表頁欄位
    list_display = ("id", "user", "email", "type", "balance", "updated_at")
    list_select_related = ("user",)
    search_fields = ("user__username", "user__email", "name", "phone", "email")

    # 支援搜尋
    search_fields = ("user__username", "user__email", "name", "phone")

    # 右側篩選器
    list_filter = ("type",)

    readonly_fields = ("updated_at", "created_at")

    # 編輯頁欄位分組
    fieldsets = (
        ("帳號資訊", {
            "fields": ("user", "type")
        }),
        ("個人資料", {
            "fields": ("name", "phone", "balance"),
        }),
        ("系統時間", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # 透過 @admin.display 定義可排序/可讀名稱的衍生欄位
    @admin.display(description="Username", ordering="user__username")
    def user_username(self, obj: UserProfile):
        return obj.user.username if obj.user_id else "-"

    @admin.display(description="Email", ordering="user__email")
    def user_email(self, obj: UserProfile):
        return obj.user.email if obj.user_id else "-"

    def get_queryset(self, request): # 覆寫以避免N+1查詢
        qs = super().get_queryset(request)
        return qs.select_related("user") # 把user這個外鍵用JOIN一次抓回來
