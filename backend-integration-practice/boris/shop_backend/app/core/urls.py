from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("account.urls")),
]

def root(_):
    return JsonResponse({"ok": True, "service": "shop-backend"})