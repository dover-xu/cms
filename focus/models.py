from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

sec_choice = (
    ('m', 'male'),
    ('f', 'female')
)


@python_2_unicode_compatible
class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d')
    profile = models.CharField('profile', max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=sec_choice, default='m')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class NoteManager(models.Manager):
    def query_by_column(self, column_id):
        query = self.get_query().filter(column_id=column_id)

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        note_list = user.note_set.all()
        return note_list

    def query_by_time(self):
        query = self.get_queryset()
        return query

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
    user = models.ForeignKey('MyUser', default='', verbose_name='who public')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    category = models.CharField(max_length=20, choices=cate_choice, default='Video', verbose_name="Belong to")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    comment_num = models.IntegerField(default=0)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)
    comment_str = models.CharField(max_length=20, blank=True, default="0")
    praise_str = models.CharField(max_length=20, blank=True, default="0")
    tread_str = models.CharField(max_length=20, blank=True, default="0")
    objects = NoteManager()

    def text_frag(self):
        if len(self.text) > 20:
            return self.text[:20] + '...'
        else:
            return self.text

    text_frag.short_description = 'CONTENT'

    def save(self, *args, **kwargs):
        # 初始化创建赞踩数据表记录
        Praise.objects.all().delete()
        Tread.objects.all().delete()
        for i in range(0, self.praise_num):
            Praise.objects.create(user=self.user, note=self)
        for i in range(0, self.tread_num):
            Tread.objects.create(user=self.user, note=self)
        # 初始化评论、赞踩的个数的字符串显示
        self.comment_num = 0
        i = self.praise_num // 10000
        r = self.praise_num % 10000
        self.praise_str = str(r) if i == 0 else str(i) + '万+'
        i = self.tread_num // 10000
        r = self.tread_num % 10000
        self.tread_str = str(r) if i == 0 else str(i) + '万+'
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return 'Content: ' + self.text

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'
        ordering = ['id']


@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('MyUser', default='', verbose_name='who comment')
    note = models.ForeignKey('Note', null=True)
    text = models.TextField()
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
    user = models.ForeignKey('MyUser', default='', verbose_name='who praise')
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
    user = models.ForeignKey('MyUser', default='', verbose_name='who tread')
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
    user = models.ForeignKey('MyUser', default='', verbose_name='who share')
    note = models.ForeignKey('Note')
    text = models.CharField(max_length=200, blank=True, null=True)
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
