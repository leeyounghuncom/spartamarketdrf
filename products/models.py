from django.db import models
from django.conf import settings

#카테고리
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
#태그
class Hashtag(models.Model):
    content = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.content = self.content.lower()  # 해시태그를 소문자로 변환하여 저장
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content

#상품
class Products(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploader")
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True, default='default_product.png')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name = "like_products")
    p_hit = models.PositiveIntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, related_name='products', blank=True)

    def __str__(self):
        return self.title

    #게시글 좋아요 기능
    @property
    def like_count(self):
        return self.likes.count()
