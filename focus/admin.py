from django import forms
from django.contrib import admin
from django.db import models
from .models import Comment, NewUser, Note, Share, Praise, Tread


# class ArticleAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': forms.Textarea(
#                 attrs={'rows': 41,
#                        'cols': 100
#                        })},
#     }
#     list_display = ('title', 'columnm', 'pub_date')
#
#     def columnm(self, obj):
#         return obj.column


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'profile')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_frag', 'user', 'category', 'comment_num', 'praise_num', 'tread_num', 'pub_date')
    list_display_links = ('id', 'text_frag', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'note_num', 'praise_num', 'tread_num', 'pub_date',)


class ShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_num', 'text', 'to', 'share_date')


class PraiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_num', 'comment_num', 'praise_date')


class TreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_num', 'comment_num', 'tread_date')


admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Praise, PraiseAdmin)
admin.site.register(Tread, TreadAdmin)
