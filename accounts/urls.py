from django.urls import path
from .views import RegisterAPI

app_name = "accounts"
urlpatterns = [
    path('', RegisterAPI.as_view()),
]