from django.contrib import admin
from blog.models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'scope', 'status')
    list_editable = ('scope', 'status')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...