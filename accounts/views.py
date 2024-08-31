from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer

User = get_user_model()
class RegisterAPI(APIView):

    # 회원가입
    # Endpoint : /api/accounts
    # Method : POST
    # 조건 : username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
    # 검증 : username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
    # 구현 : 데이터 검증 후 저장.
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)  # 요청 데이터로 Serializer 생성
        if serializer.is_valid():  # 데이터가 유효한지 검사
            user = serializer.save()  # 데이터가 유효하면 사용자 생성 및 저장
            return Response({"message": "회원가입이 성공적으로 완료되었습니다.", "user_id": user.id}, status=status.HTTP_201_CREATED) # 성공 응답 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효하지 않은 경우 에러 메시지 반환
