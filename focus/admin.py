from django import forms
from django.contrib import admin
from django.db import models
from .models import Comment, Article, Column, NewUser, Author, Note, Share, Praise, Tread


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'pub_date', 'text', 'praise_num', 'tread_num')


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
                attrs={'rows': 41,
                       'cols': 100
                       })},
    }
    list_display = ('title', 'columnm', 'pub_date')

    def columnm(self, obj):
        return obj.column


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'profile')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'image', 'category', 'pub_date', 'comment_num', 'praise_num', 'tread_num')


class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'text', 'to')


class PraiseAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'comment')


class TreadAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'comment')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Praise, PraiseAdmin)
admin.site.register(Tread, TreadAdmin)
