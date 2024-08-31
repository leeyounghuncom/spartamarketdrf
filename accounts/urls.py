from django.urls import path
from .views import RegisterAPI, LoginAPI, ProfileAPI

app_name = "accounts"
urlpatterns = [
    path('', RegisterAPI.as_view()), #회원가입
    path('login/', LoginAPI.as_view()), #로그인
    path('<str:username>/', ProfileAPI.as_view()), #프로필 조회
]
