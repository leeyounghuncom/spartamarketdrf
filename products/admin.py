from django.contrib import admin
from .models import Category, Products

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['category', 'created_at']