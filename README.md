# spartamarketdrf

# **프로젝트 소개**<br>
스파르타 마켓을 DRF로 구현해봅시다!<br>
<br>
# **개발 기간**<br>
2024.08.29.~2024.09.02<br>
<br>
# **개발 환경**<br>
**Python** : Django DRF<br>
**DB** : SQlite<br>
<br>
# **ERD**<br>
![image](https://github.com/leeyounghuncom/spartamarketdrf/blob/main/readme/erd.png?raw=true)
<br>
# **설치 및 실행 방법**
* pip install -r requirements.txt
* .env 확인
* python manage.py migrate
* python manage.py runserver

# ** RESTful API 명세서 **


# **Custom User 이슈
* get_user_model() 커스텀 유저 모델과 유저 시리얼라이져 사용
* 패스워드 그대로 노출 암호화 처리

# ** ORM 이슈 **
* DB에서 해당 값을 못 찾을경우 get_object_or_404() 처리

# ** Permission 이슈 **
* 장고에서 제공하는 permission인 IsAuthenticated, AllowAny 등 있지만 AllowAny보다는 안전한 IsAuthenticatedOrReadOnly이 권장 찾음
* 추후에 비즈니스 상황에 따라 다양한 permission 유형이 필요함을 느껴 Permission custumize 방법도 공부할 필요가 있음




<br>
# **기능 상세**<br>
**회원가입**<br>
**로그인**<br>
**프로필 조회**<br>
**상품 등록**<br>
**상품 목록 조회**<br>
**상품 수정**<br>
**상품 삭제**<br>
**상품 등록**<br>
**상품 목록 조회**<br>
**상품 수정**<br>
**상품 삭제**<br>
**로그아웃**<br>
**본인 정보 수정**<br>
**패스워드 변경**<br>
**회원 탈퇴**<br>
**페이지네이션 및 필터링(검색기능)**<br>
**카테고리 기능(admin page 활용)**<br>
**팔로잉 시스템**<br>
**게시글 좋아요 기능**<br>
**태그 기능**<br>




