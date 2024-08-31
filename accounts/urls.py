from django.urls import path
from .views import RegisterAPI, LoginAPI, ProfileAPI, LogoutAPI, ChangePasswordAPI, FollowAPI

#로그아웃을 프로필 밑에다가 할경우에는 POST 주소를 찾지 못한다.
#
app_name = "accounts"
urlpatterns = [
    path('', RegisterAPI.as_view()), #회원가입, 회원탈퇴
    path('login/', LoginAPI.as_view()), #로그인
    # "detail": "Method \"POST\" not allowed." 발생되는 이유는 포프필 조회를 로그아웃 밑에다 작성했더니 뜬다. 하지만 위치를 바꾸나 잘된다. 쉣!!!!!! 아까운 2시간반 ....
    path('logout/', LogoutAPI.as_view()),  # 로그아웃
    path('password/', ChangePasswordAPI.as_view()), #패스워드변경

    path('<str:username>/', ProfileAPI.as_view()), #프로필 조회, 본인 정보 수정
    path('<str:username>/follow/', FollowAPI.as_view()), #팔로우 팔로워

]
