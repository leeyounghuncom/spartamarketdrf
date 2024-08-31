from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated


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

class LoginAPI(APIView):

    # 로그인
    # Endpoint : /api/accounts/login
    # Method : POST
    # 조건 : 사용자명과 비밀번호 입력 필요.
    # 검증 : 사용자명과 비밀번호가 데이터베이스의 기록과 일치해야 함.
    # 구현 : 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.

    def post(self, request):

        # username과 password를
        username = request.data['username']
        password = request.data['password']

        # 사용자 검색
        user = CustomUser.objects.filter(username=username).first()

        # 사용자가 존재하지 않거나 비밀번호가 일치하지 않는 경우 에러 메시지 반환
        if user is None or not check_password(password, user.password):
            message = "존재하지 않는 아이디입니다." if user is None else "비밀번호 틀립니다."
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 인증이 성공하면 JWT 토큰 생성
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 응답 데이터와 JWT 토큰을 포함하여 응답 객체 생성
        response = Response(
            {
                'user': UserRegistrationSerializer(user).data,
                "jwt_token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
            },
            status=status.HTTP_200_OK
        )

        # access_token과 refresh_token을 httpOnly 쿠키로 설정
        response.set_cookie("access_token", access_token, httponly=True, secure=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)

        # 응답 반환
        return response


class ProfileAPI(APIView):

    # 프로필 조회
    # Endpoint : /api/accounts/<str:username>
    # Method : GET
    # 조건 : 로그인 상태 필요.
    # 검증 : 로그인 한 사용자만 프로필 조회 가능
    # 구현 : 로그인한 사용자의 정보를 JSON 형태로 반환.

    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        # 사용자 검색
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:

            # 사용자가 존재하지 않으면 404 에러 반환
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 요청한 사용자와 찾은 사용자가 다르면 403 에러 반환
        if request.user != user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 사용자 정보를 직렬화하여 반환
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)