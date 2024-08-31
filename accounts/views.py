from rest_framework.decorators import permission_classes

from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# https://medium.com/@abdullah.bakir.204/boosting-your-django-api-performance-with-drf-decorators-94087b347333

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


    # 회원 탈퇴
    # Endpoint :  `/api/accounts`
    # Method :  `DELETE`
    # 조건 : 로그인 상태, 비밀번호 재입력 필요.
    # 검증 : 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
    # 구현 : 비밀번호 확인 후 계정 삭제.
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        data = request.data

        # 비밀번호 확인
        password = data.get("password")
        if not password or not check_password(password, user.password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 계정 삭제
        user.delete()
        return Response({"message": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


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

    # 본인 정보 수정
    # Endpoint: `/api/accounts/<str:username>`
    # Method: `PUT`
    # 조건: 이메일, 이름, 닉네임, 생일 입력 필요하며, 성별, 자기소개 생략 가능
    # 검증: 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.
    # 구현: 입력된 정보를 검증 후 데이터베이스를 업데이트.

    def put(self, request, username):
        # 로그인한 사용자와 요청된 사용자가 같은지 확인
        if request.user.username != username:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 요청된 사용자 정보를 가져옴
        user = User.objects.get(username=username)

        # 업데이트할 데이터
        data = request.data

        # 이메일 중복 체크
        if 'email' in data and User.objects.filter(email=data['email']).exclude(username=username).exists():
            raise ValidationError({"email": "이미 사용 중인 이메일입니다."})


        # 시리얼라이저를 통해 데이터 검증 및 업데이트
        serializer = UserRegistrationSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutAPI(APIView):

    # 로그아웃
    # Endpoint: /api/accounts/logout
    # Method: POST
    # 조건: 로그인 상태 필요.
    # 구현: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
    permission_classes = [IsAuthenticated]

    def post(self, request):

        #POST 메소드를 사용하여 로그아웃을 수행합니다.
        #클라이언트 측에서 저장된 토큰을 쿠키에서 삭제합니다.

        response = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')  # 접근 토큰 삭제
        response.delete_cookie('refresh_token')  # 갱신 토큰 삭제
        return response


class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        # 기존 패스워드 확인
        current_password = data.get("current_password")
        if not current_password or not check_password(current_password, user.password):
            return Response({"error": "기존 패스워드가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 패스워드 확인
        new_password = data.get("new_password")
        if not new_password:
            return Response({"error": "새로운 패스워드를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 패스워드와 새로운 패스워드 비교
        if current_password == new_password:
            return Response({"error": "기존 패스워드와 새로운 패스워드는 달라야 합니다."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            # 패스워드 업데이트
            user.set_password(new_password)
            user.full_clean() # 추가적인 검증이 필요할 경우 사용
            user.save()  # 패스워드 저장과 사용자 업데이트
            return Response({"message": "패스워드가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)