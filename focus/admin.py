from django import forms
from django.contrib import admin
from django.db import models
from .models import Comment, Article, Column, NewUser, Author, Post


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'pub_date', 'content', 'poll_num')


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
                attrs={'rows': 41,
                       'cols': 100
                       })},
    }
    list_display = ('title', 'columnm', 'pub_date', 'poll_num')

    def columnm(self, obj):
        return obj.column


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'profile')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'image', 'category', 'pub_date', 'comment_num', 'praise_num', 'tread_num')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
