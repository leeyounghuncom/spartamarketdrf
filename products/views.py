from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Products
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductLCAPI(ListCreateAPIView):
    # 상품을 조회
    queryset = Products.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_permissions(self):
        # GET 요청은 인증 X, POST 요청 인증 O.
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [AllowAny()]

    # 페이지네이션 및 필터링(검색기능)
    # 조건 : 상품 목록 조회 시 적용됩니다.
    # 구현 : 제목, 유저명, 내용으로 필터링이 가능하며, 결과는 페이지네이션으로 관리

    def get_queryset(self):

        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        author_username = self.request.query_params.get('author_username', None)
        content = self.request.query_params.get('content', None)
        order_by_likes = self.request.query_params.get('order_by_likes', None)  #라이크 추가

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author_username:
            queryset = queryset.filter(author__username__icontains=author_username)
        if content:
            queryset = queryset.filter(content__icontains=content)

        #라이크 기능 빠짐
        if order_by_likes:
            queryset = queryset.order_by('-like_count')  # 라이크 추가

        return queryset

    def perform_create(self, serializer):
        # 새 상품을 생성할 때 게시 데이터를 저장
        serializer.save(author=self.request.user)


class ProductUDAPI(UpdateAPIView, DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 객체를 검색하고 수정 및 삭제 권한을 검증
        # 권한이 없는 경우 예외를 발생
        product = super().get_object()
        if product.author != self.request.user:
            raise PermissionDenied("수정 및 삭제 권한이 없습니다.")
        return product

    def perform_update(self, serializer):
        # 입력된 정보로 기존 상품 정보를 업데이트합니다.
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # 상품을 삭제하고, 성공 메시지를 포함한 응답을 반환합니다.
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "상품이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 게시글 좋아요 기능
class ProductLikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        user = request.user

        if user in product.likes.all():
            product.likes.remove(user)
            return Response({"message": "좋아요가 취소되었습니다.", "like_count": product.like_count}, status=status.HTTP_200_OK)
        else:
            product.likes.add(user)
            return Response({"message": "좋아요가 추가되었습니다.", "like_count": product.like_count}, status=status.HTTP_200_OK)
