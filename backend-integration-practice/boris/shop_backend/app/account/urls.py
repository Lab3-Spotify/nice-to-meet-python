from django.urls import path
from account.views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    DepositView,
)

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login",    LoginView.as_view()),
    path("logout",   LogoutView.as_view()),
    path("me",       MeView.as_view()),
    path("deposit",  DepositView.as_view()),
]