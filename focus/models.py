from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

sec_choice = (
    ('m', 'male'),
    ('f', 'female')
)


@python_2_unicode_compatible
class NewUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', blank=True)
    profile = models.CharField('profile', default='', max_length=255)
    sex = models.CharField(max_length=10, choices=sec_choice, default='m')

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('column_name', max_length=256)
    intro = models.TextField('introduction', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'column'
        ordering = ['name']


class ArticleManager(models.Manager):
    def query_by_column(self, column_id):
        query = self.get_query().filter(column_id=column_id)

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query


class Article(models.Model):
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to')
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author')
    user = models.ManyToManyField('NewUser', blank=True)
    content = models.TextField('content')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField('notDraft', default=True)
    comment_num = models.IntegerField(default=0)
    keep_num = models.IntegerField(default=0)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'article'


class Author(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile', default='', max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


##############################################
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
    user = models.ForeignKey('NewUser', default='')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='img/%Y/%m/%d', blank=True)
    category = models.CharField(max_length=20, choices=cate_choice, blank=True, null=True, verbose_name="Belong to")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    comment_num = models.IntegerField(default=0)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)
    objects = NoteManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'


@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('NewUser', default='')
    note = models.ForeignKey('Note', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)

    def __unicode__(self):
        return self.text


class Praise(models.Model):
    user = models.ForeignKey('NewUser', default='')
    note = models.ForeignKey('Note', blank=True, null=True)
    comment = models.ForeignKey('Comment', blank=True, null=True)


class Tread(models.Model):
    user = models.ForeignKey('NewUser', default='')
    note = models.ForeignKey('Note', blank=True, null=True)
    comment = models.ForeignKey('Comment', blank=True, null=True)


class Share(models.Model):
    user = models.ForeignKey('NewUser', default='')
    note = models.ForeignKey('Note')
    text = models.CharField(max_length=200, blank=True, null=True)
    to = models.CharField(max_length=256)
