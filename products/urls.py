from django.urls import path
from .views import ProductLCAPI, ProductUDAPI

app_name = 'products'
urlpatterns = [
    path('', ProductLCAPI.as_view()), #목록 , 등록
    path('<int:pk>/', ProductUDAPI.as_view()), #수정, 삭제


]