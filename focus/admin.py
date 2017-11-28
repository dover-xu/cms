from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from .models import Comment, MyUser, Tag, Note, Share, Praise, Tread
from django.utils.translation import ugettext_lazy as _


# class NewUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'date_joined', 'profile')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name')
    list_display_links = ('id', 'tag_name')
    # list_editable = ['tag_name', ]
    list_per_page = 50
    ordering = ('id',)
    search_fields = ('id', 'tag_name')  # 搜索字段
    # date_hierarchy = 'pub_date'  # 详细时间分层筛选
    # list_filter = ('')  # 过滤器


class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text_frag', 'user', 'category', 'hot', 'recmd', 'haha', 'click_num', 'comment_num', 'praise_num',
        'tread_num', 'share_num', 'pub_date')
    list_display_links = ('id', 'text_frag')
    list_editable = ['hot', 'recmd', 'haha']
    list_per_page = 50
    ordering = ('-pub_date', )
    search_fields = ('id', 'user', 'text_frag', 'category')  # 搜索字段
    date_hierarchy = 'pub_date'  # 详细时间分层筛选
    list_filter = ('pub_date', 'category')  # 过滤器


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'note_id', 'praise_num', 'tread_num', 'pub_date')
    list_display_links = ('id', 'text')
    list_per_page = 50
    ordering = ('-pub_date',)
    search_fields = ('id', 'user', 'text')  # 搜索字段
    date_hierarchy = 'pub_date'  # 详细时间分层筛选
    list_filter = ('pub_date',)  # 过滤器


class ShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_id', 'text', 'to', 'share_date')
    list_display_links = ('id',)
    list_per_page = 50
    ordering = ('-share_date',)
    search_fields = ('id', 'user', 'text')  # 搜索字段
    date_hierarchy = 'share_date'  # 详细时间分层筛选
    list_filter = ('share_date',)  # 过滤器


class PraiseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_id', 'comment_num', 'praise_date')
    list_display_links = ('id',)
    list_per_page = 50
    ordering = ('-praise_date',)
    search_fields = ('id', 'user')  # 搜索字段
    date_hierarchy = 'praise_date'  # 详细时间分层筛选
    list_filter = ('praise_date',)  # 过滤器


class TreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'note_id', 'comment_num', 'tread_date')
    list_display_links = ('id',)
    list_per_page = 50
    ordering = ('-tread_date', )
    search_fields = ('id', 'user')  # 搜索字段
    date_hierarchy = 'tread_date'  # 详细时间分层筛选
    list_filter = ('tread_date',)  # 过滤器


# class User_exAdmin(admin.ModelAdmin):  # 验证码部分展示
#     list_display = ('valid_code', 'valid_time', 'email')


# custom user admin
class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True  # 为了让此字段在admin中为必选项，自定义一个form


class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('id', 'username', 'sex', 'email', 'is_active', 'is_staff', 'is_superuser')
        self.list_display_links = ('id', 'username')
        self.list_editable = ['is_active', 'is_staff']
        self.list_per_page = 50
        self.ordering = ('id',)
        self.search_fields = ('id', 'username', 'email')  # 搜索字段
        self.date_hierarchy = 'date_joined'  # 详细时间分层筛选
        self.list_filter = ('is_active', 'is_staff', 'is_superuser', 'sex')  # 过滤器
        self.form = MyUserChangeForm  # 编辑用户表单，使用自定义的表单
        self.add_form = MyUserCreationForm  # 添加用户表单，使用自定义的表单
        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

    def changelist_view(self, request,
                        extra_context=None):  # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
        if not request.user.is_superuser:  # 非super用户不能设定编辑是否为super用户
            self.fieldsets = ((_('Basic info'), {'fields': ('username', 'password',)}),
                              (_('Personal info'), {'fields': ('avatar', 'sex', 'email', 'profile')}),
                              # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                              )  # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': (
                                              'username', 'password1', 'password2', 'avatar', 'email', 'is_active',
                                              'is_staff', 'groups'),
                                          }),
                                  )  # 此字段定义UserCreationForm表单中的具体显示内容
        else:  # super账户可以做任何事
            self.fieldsets = ((_('Basic info'), {'fields': ('username', 'password',)}),
                              (_('Personal info'), {'fields': ('avatar', 'sex', 'email', 'profile')}),
                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': (
                                              'username', 'password1', 'password2', 'avatar', 'email', 'is_active',
                                              'is_staff', 'is_superuser', 'groups'),
                                          }),
                                  )
        return super(CustomUserAdmin, self).changelist_view(request, extra_context)


admin.site.register(MyUser, CustomUserAdmin)
# admin.site.register(models.User_ex, User_exAdmin)
# admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Praise, PraiseAdmin)
admin.site.register(Tread, TreadAdmin)
