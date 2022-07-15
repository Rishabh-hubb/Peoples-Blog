from django.contrib import admin
from .models import Post,Comment,Category
# Register your models here.


class CommentInline(admin.TabularInline):  # new
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Post, ArticleAdmin)

admin.site.register(Comment)
admin.site.register(Category)

