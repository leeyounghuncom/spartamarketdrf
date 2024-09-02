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

**회원가입**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85.png?raw=true)<br>
**로그인**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EB%A1%9C%EA%B7%B8%EC%9D%B8.png?raw=true)<br>
**프로필 조회**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%94%84%EB%A1%9C%ED%95%84%20%EC%A1%B0%ED%9A%8C.png?raw=true)<br>
**상품 등록**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EB%A6%AC%EC%8A%A4%ED%8A%B8_%EC%B6%94%EA%B0%80(%EC%B6%94%EA%B0%80).png?raw=true)<br>
**상품 목록 조회**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EB%A6%AC%EC%8A%A4%ED%8A%B8_%EC%B6%94%EA%B0%80(%EB%A6%AC%EC%8A%A4%ED%8A%B8).png?raw=true)<br>
**상품 수정**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EC%88%98%EC%A0%95_%EC%82%AD%EC%A0%9C(%EC%88%98%EC%A0%95).png?raw=true)<br>
**상품 삭제**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EC%88%98%EC%A0%95_%EC%82%AD%EC%A0%9C(%EC%82%AD%EC%A0%9C).png?raw=true)<br>
**로그아웃**<br>
**본인 정보 수정**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8.png?raw=true)<br>
**패스워드 변경**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C%EB%B3%80%EA%B2%BD.png?raw=true)<br>
**회원 탈퇴**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%94%84%EB%A1%9C%ED%95%84%20%EC%A1%B0%ED%9A%8C.png?raw=true)<br>
**페이지네이션 및 필터링(검색기능)**<br>
**카테고리 기능(admin page 활용)**<br>
**팔로잉 시스템**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%83%9C%EA%B7%B8.png?raw=true)<br>
**게시글 좋아요 기능**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%EB%9D%BC%EC%9D%B4%ED%81%AC.png?raw=true)<br>
**태그 기능**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/%ED%83%9C%EA%B7%B8.png?raw=true)<br>




