from django.contrib import admin
from blog.models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...