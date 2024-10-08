# spartamarketdrf

# 프로젝트 소개
스파르타 마켓을 DRF로 구현해봅시다!<br>

# 개발 기간
2024.08.29.~2024.09.02<br>

# 개발 환경
**Python** : Django DRF<br>
**DB** : SQlite<br>

# ERD
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/erd.png?raw=true)

# 설치 및 실행 방법
* pip install -r requirements.txt
* .env 확인
* python manage.py migrate
* python manage.py runserver

# RESTful API 명세서
명칭 | Endpoint | Method | status
|------|---|---|---|
회원가입, 회원탈퇴 | api/accounts/ | POST, DELETE | 201_CREATED, 400_BAD_REQUEST,204_NO_CONTENT
로그인 | api/accounts/login/ | POST | 400_BAD_REQUEST,HTTP_200_OK
로그아웃 | api/accounts/logout/ |  POST | 200_OK
패스워드변경 | api/accounts/password/ | PUT |  400_BAD_REQUEST
프로필 조회, 본인 정보 수정 | api/accounts/<str:username>/ | GET,PUT |404_NOT_FOUND,403_FORBIDDEN,200_OK,400_BAD_REQUEST
팔로우 팔로워 |  api/accounts/<str:username>/follow/ | POST | 400_BAD_REQUEST,200_OK
목록,등록 | api/products/ | GET,POST |
수정, 삭제 | api/products/<int:pk>/ | PUT, DELETE | 204_NO_CONTENT
좋아요 | api/products/<int:product_id>/like/ | POST |  200_OK

# Custom User 이슈
* get_user_model() 커스텀 유저 모델과 유저 시리얼라이져 사용
* 패스워드 그대로 노출 암호화 처리

# ORM 이슈
* DB에서 해당 값을 못 찾을경우 get_object_or_404() 처리

# Permission 이슈
* 장고에서 제공하는 permission인 IsAuthenticated, AllowAny 등 있지만 AllowAny보다는 안전한 IsAuthenticatedOrReadOnly이 권장 찾음
* 추후에 비즈니스 상황에 따라 다양한 permission 유형이 필요함을 느껴 Permission custumize 방법도 공부할 필요가 있음

# 기능 상세
일일이 캡쳐 보기 불편해서 한장으로 하였습니다.<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202024-09-02%2014-00-47.png?raw=true)
<p>&nbsp;</p>

TIL : https://leeyounghun.com/janggyo-simhwa-teureobeul-syuting/
