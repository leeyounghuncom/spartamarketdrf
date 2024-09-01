from django.urls import path
from .views import ProductLCAPI, ProductUDAPI, ProductLikeAPI

app_name = 'products'
urlpatterns = [
    path('', ProductLCAPI.as_view()), #목록 , 등록
    path('<int:pk>/', ProductUDAPI.as_view()), #수정, 삭제
    path('<int:product_id>/like/', ProductLikeAPI.as_view(), name='product_like'), #좋아요

]