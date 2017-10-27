import os

from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class MyUserManager(models.Manager):
    # 反序列化到表
    def get_by_natural_key(self, username):
        return self.get(username=username)


sex_choice = (
    ('m', 'male'),
    ('f', 'female')
)


@python_2_unicode_compatible
class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True)
    profile = models.CharField('profile', max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=sex_choice, default='m')
    # objects = MyUserManager()

    # 序列化时代替主键
    def natural_key(self):
        return self.username, "http://127.0.0.1:8008" + self.avatar.url

    def __str__(self):
        return self.username


class NoteManager(models.Manager):
    # def get_by_natural_key(self, text):
    #     return self.get(text=text)

    def query_by_recommend(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_all_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_all_by_hot(self):
        query = self.get_queryset().order_by('-hot')
        return query

    def query_pic_by_time(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-pub_date')
        return query

    def query_pic_by_hot(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-hot')
        return query

    def query_jape_by_time(self):
        query = self.get_queryset().filter(category__exact='Jape').order_by('-pub_date')
        return query

    def query_jape_by_hot(self):
        query = self.get_queryset().filter(category__exact='Jape').order_by('-hot')
        return query

    def query_by_id(self, note_id):
        return Note.objects.get(id=note_id)

    def query_by_column(self, column_id):
        query = self.get_query().filter(column_id=column_id)

    def query_by_user(self, user):
        # user = MyUser.objects.get(id=user_id)
        note_list = user.notes.all().order_by('-pub_date')
        return note_list

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(text__contains=keyword)
        return query


cate_choice = (
    ('Video', 'Video'),
    ('Picture', 'Picture'),
    ('Jape', 'Jape'),
    ('Others', 'Others')
)


class Note(models.Model):
    user = models.ForeignKey('MyUser', default='', related_name='notes', verbose_name='who public')
    text = models.TextField(null=False, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    category = models.CharField(max_length=20, choices=cate_choice, default='Picture', verbose_name="Belong to")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    comment_num = models.IntegerField(default=0)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)
    share_num = models.IntegerField(default=0, null=True, blank=True)
    comment_str = models.CharField(max_length=20, blank=True, default="0")
    praise_str = models.CharField(max_length=20, blank=True, default="0")
    tread_str = models.CharField(max_length=20, blank=True, default="0")
    share_str = models.CharField(max_length=20, blank=True, default="0")
    click_num = models.IntegerField(default=0)
    # 分享10分、评论10分、点赞3分、点踩1分、访问1分
    hot = models.IntegerField(default=0)
    recommend = models.IntegerField(default=0)
    objects = NoteManager()

    def natural_key(self):
        return {
            'text': self.text,
        }

    natural_key.dependencies = ['MyUser']

    def text_frag(self):
        if len(self.text) > 20:
            return self.text[:20] + '...'
        else:
            return self.text

    text_frag.short_description = 'CONTENT'

    def save(self, *args, **kwargs):
        # 初始化评论、赞踩的个数的字符串显示
        i = self.comment_num // 10000
        self.comment_str = str(self.comment_num) if i == 0 else str("%.1f万" % (self.comment_num / 10000))
        i = self.praise_num // 10000
        self.praise_str = str(self.praise_num) if i == 0 else str("%.1f万" % (self.praise_num / 10000))
        i = self.tread_num // 10000
        self.tread_str = str(self.tread_num) if i == 0 else str("%.1f万" % (self.tread_num / 10000))
        i = self.share_num // 10000
        self.share_str = str(self.share_num) if i == 0 else str("%.1f万" % (self.share_num / 10000))
        # 计算热度值
        self.hot = (self.share_num + self.comment_num) * 10 + self.praise_num * 3 + self.tread_num + self.click_num
        super(Note, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        # 删除图片
        if self.image:
            file_full_path = self.image.path
            if os.path.exists(file_full_path):
                if os.path.isfile(file_full_path):
                    os.remove(file_full_path)
        super(Note, self).delete(using=None, keep_parents=False)

    def __str__(self):
        return 'Content: ' + self.text

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'
        ordering = ['id']
        # unique_together = (('text', 'user'),)


@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('MyUser', default='', related_name='comments', verbose_name='who comment')
    note = models.ForeignKey('Note', related_name='comments', null=True)
    text = models.TextField(null=False, blank=False, default='')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)

    def note_num(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_num.short_description = 'note id'

    def __str__(self):
        return 'Content: ' + self.text


class Praise(models.Model):
    user = models.ForeignKey('MyUser', default='', related_name='praises', verbose_name='who praise')
    note = models.ForeignKey('Note', blank=True, null=True)
    comment = models.ForeignKey('Comment', blank=True, null=True)
    praise_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_num(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_num.short_description = 'note id'

    def comment_num(self):
        if self.comment:
            return self.comment.id
        else:
            return self.comment

    comment_num.short_description = 'comment id'


class Tread(models.Model):
    user = models.ForeignKey('MyUser', default='', related_name='treads', verbose_name='who tread')
    note = models.ForeignKey('Note', blank=True, null=True)
    comment = models.ForeignKey('Comment', blank=True, null=True)
    tread_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_num(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_num.short_description = 'note id'

    def comment_num(self):
        if self.comment:
            return self.comment.id
        else:
            return self.comment

    comment_num.short_description = 'comment id'


class Share(models.Model):
    user = models.ForeignKey('MyUser', default='', related_name='shares', verbose_name='who share')
    note = models.ForeignKey('Note', blank=True, null=True)
    text = models.CharField(max_length=200, default='', blank=True, null=True)
    to = models.CharField(max_length=256)
    share_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_num(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_num.short_description = 'note id'

    def __str__(self):
        if self.text:
            return 'Content: ' + self.text
        else:
            return 'Shared to: ' + self.to
