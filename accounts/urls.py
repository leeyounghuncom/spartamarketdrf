from django.urls import path
from .views import RegisterAPI, LoginAPI

app_name = "accounts"
urlpatterns = [
    path('', RegisterAPI.as_view()), #회원가입
    path('login/', LoginAPI.as_view()), #로그인
]
