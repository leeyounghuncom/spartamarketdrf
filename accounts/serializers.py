from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'nickname', 'birthday', 'gender', 'bio']

    #이메일 중복 방지
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("이 이메일은 이미 사용 중입니다.")
        return value

    # 사용자 생성 메서드
    def create(self, validated_data):
        user = CustomUser(**validated_data)  # 검증된 데이터를 사용하여 사용자 객체 생성
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()  # 데이터베이스에 사용자 저장
        return user  # 생성된 사용자 객체 반환