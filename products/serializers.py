from rest_framework import serializers
from .models import Products, Category, Hashtag

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['content']

class ProductSerializer(serializers.ModelSerializer):
    # 해시태그
    hashtags = HashtagSerializer(many=True, read_only=True)  # 리드
    hashtag_names = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True,
                                          required=False)  # 쓰기
    # 카테고리 모두 가져오기
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Products
        fields = ['id', 'author', 'title', 'content', 'product_image', 'created_at', 'updated_at', 'category', 'likes', 'hashtags', 'hashtag_names',]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes']

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtag_names', [])
        category = validated_data.pop('category')  # 카테고리 값을 가져옵니다
        # validated_data 딕셔너리를 풀어서 **kwargs 형태로 제품 객체 생성 메소드에 전달
        product = Products.objects.create(category=category, **validated_data)  # 카테고리를 포함하여 객체를 생성합니다
        # product = Products.objects.create(**validated_data)
        for hashtag_content in hashtags_data:
            hashtag, created = Hashtag.objects.get_or_create(content=hashtag_content.lower())
            product.hashtags.add(hashtag)
        return product

    def update(self, instance, validated_data):
        hashtags_data = validated_data.pop('hashtag_names', [])
        category = validated_data.pop('category')  # 카테고리 데이터를 가져옴

        # 카테고리 업데이트
        instance.category = category
        instance.save()
        instance.hashtags.clear()  # 기존 해시태그 제거
        for hashtag_content in hashtags_data:
            hashtag, created = Hashtag.objects.get_or_create(content=hashtag_content.lower())
            instance.hashtags.add(hashtag)

        return instance
