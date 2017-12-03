import os

from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
logger = logging.getLogger('django')


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
    profile = models.CharField('profile', max_length=255, blank=True, default='')
    sex = models.CharField(max_length=10, choices=sex_choice, default='m')
    email = models.EmailField(max_length=75, blank=True)
    # objects = MyUserManager()

    # 序列化时代替主键
    def natural_key(self):
        return self.username, "http://127.0.0.1:8008" + self.avatar.url

    def __str__(self):
        return self.username


class NoteManager(models.Manager):
    # def get_by_natural_key(self, text):
    #     return self.get(text=text)

    def query_all_by_recommend(self):
        query = self.get_queryset().order_by('-recmd')[:200]
        return query

    def query_all_by_time(self):
        query = self.get_queryset().order_by('-pub_date')[:200]
        return query

    def query_all_by_hot(self):
        query = self.get_queryset().order_by('-hot')[:200]
        return query

    def query_pic_by_recommend(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-recmd')[:200]
        return query

    def query_pic_by_time(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-pub_date')[:200]
        return query

    def query_pic_by_hot(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-hot')[:200]
        return query

    def query_jape_by_recommend(self):
        query = self.get_queryset().filter(category__exact='Jape').order_by('-recmd')[:200]
        return query

    def query_jape_by_time(self):
        query = self.get_queryset().filter(category__exact='Jape').order_by('-pub_date')[:200]
        return query

    def query_jape_by_hot(self):
        query = self.get_queryset().filter(category__exact='Jape').order_by('-hot')[:200]
        return query

    def query_by_haha(self):
        query = self.get_queryset().filter(category__exact='Picture').order_by('-haha')[:4]
        return query

    def query_by_id(self, note_id):
        try:
            return self.get_queryset().get(id=note_id)
        except:
            return None

    def query_by_user(self, user):
        # user = MyUser.objects.get(id=user_id)
        # query = user.note_set.all().order_by('-pub_date')
        query = self.get_queryset().filter(user=user).order_by('-pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(text__contains=keyword)
        return query


class Tag(models.Model):
    tag_name = models.CharField(max_length=20, blank=True)


cate_choice = (
    ('Video', 'Video'),
    ('Picture', 'Picture'),
    ('Jape', 'Jape'),
    ('Others', 'Others')
)


class Note(models.Model):
    user = models.ForeignKey('MyUser', related_name='note_set', verbose_name='who public')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    category = models.CharField(max_length=20, choices=cate_choice, default='Picture', verbose_name="Belong to")
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    comment_num = models.IntegerField(default=0)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)
    share_num = models.IntegerField(default=0)
    comment_str = models.CharField(max_length=20, blank=True, default="0")
    praise_str = models.CharField(max_length=20, blank=True, default="0")
    tread_str = models.CharField(max_length=20, blank=True, default="0")
    share_str = models.CharField(max_length=20, blank=True, default="0")
    click_num = models.IntegerField(default=0)
    hot = models.IntegerField(default=0)  # 热度值：分享10分、评论10分、点赞3分、点踩1分、访问1分
    recmd = models.IntegerField(default=0)  # 推荐值
    haha = models.IntegerField(default=0)  # 欢笑值
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

    def increase_comment(self):
        num = self.comment_num = self.comment_num + 1
        num_i = num // 10000
        self.comment_str = str(num) if num_i == 0 else str("%.1f万" % (num / 10000))

    def increase_praise(self):
        num = self.praise_num = self.praise_num + 1
        num_i = num // 10000
        self.praise_str = str(num) if num_i == 0 else str("%.1f万" % (num / 10000))

    def increase_tread(self):
        num = self.tread_num = self.tread_num + 1
        num_i = num // 10000
        self.tread_str = str(num) if num_i == 0 else str("%.1f万" % (num / 10000))

    def increase_share(self):
        num = self.share_num = self.share_num + 1
        num_i = num // 10000
        self.share_str = str(num) if num_i == 0 else str("%.1f万" % (num / 10000))

    def __str__(self):
        return 'Content: ' + self.text

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'
        ordering = ['id']
        # unique_together = (('text', 'user'),)


@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('MyUser', null=True, related_name='comments', verbose_name='who comment')
    note = models.ForeignKey('Note', null=True, related_name='comments')
    text = models.TextField(blank=False, default='')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    praise_num = models.IntegerField(default=0)
    tread_num = models.IntegerField(default=0)

    def note_id(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_id.short_description = 'note id'

    def __str__(self):
        return 'Content: ' + self.text


class Praise(models.Model):
    user = models.ForeignKey('MyUser', null=True, related_name='praises', verbose_name='who praise')
    note = models.ForeignKey('Note', null=True, blank=True)
    comment = models.ForeignKey('Comment', null=True, blank=True)
    praise_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_id(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_id.short_description = 'note id'

    def comment_num(self):
        if self.comment:
            return self.comment.id
        else:
            return self.comment

    comment_num.short_description = 'comment id'


class Tread(models.Model):
    user = models.ForeignKey('MyUser', null=True, related_name='treads', verbose_name='who tread')
    note = models.ForeignKey('Note', null=True, blank=True)
    comment = models.ForeignKey('Comment', null=True, blank=True)
    tread_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_id(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_id.short_description = 'note id'

    def comment_num(self):
        if self.comment:
            return self.comment.id
        else:
            return self.comment

    comment_num.short_description = 'comment id'


class Share(models.Model):
    user = models.ForeignKey('MyUser', related_name='shares', verbose_name='who share')
    note = models.ForeignKey('Note', null=True)
    text = models.CharField(max_length=200, default='', blank=True)
    to = models.CharField(max_length=256)
    share_date = models.DateTimeField(auto_now_add=True, editable=True)

    def note_id(self):
        if self.note:
            return self.note.id
        else:
            return self.note

    note_id.short_description = 'note id'

    def __str__(self):
        if self.text:
            return 'Content: ' + self.text
        else:
            return 'Shared to: ' + self.to


@receiver(post_delete, sender=Share)
@receiver(post_delete, sender=Tread)
@receiver(post_delete, sender=Praise)
@receiver(post_delete, sender=Comment)
def comment_praise_tread_share_delete(sender, instance, **kwargs):
    # 初始化评论、赞踩的个数的字符串显示
    note, comment = None, None
    if isinstance(instance, Comment):
        note = instance.note
        note.comment_num = Comment.objects.filter(note=note).count()
        i = note.comment_num // 10000
        note.comment_str = str(note.comment_num) if i == 0 else str("%.1f万" % (note.comment_num / 10000))
    elif isinstance(instance, Praise):
        note = instance.note
        comment = instance.comment
        if note:
            note.praise_num = Praise.objects.filter(note=note).count()
            i = note.praise_num // 10000
            note.praise_str = str(note.praise_num) if i == 0 else str("%.1f万" % (note.praise_num / 10000))
        if comment:
            comment.praise_num = Praise.objects.filter(comment=comment).count()
    elif isinstance(instance, Tread):
        note = instance.note
        comment = instance.comment
        if note:
            note.tread_num = Tread.objects.filter(note=note).count()
            i = note.tread_num // 10000
            note.tread_str = str(note.tread_num) if i == 0 else str("%.1f万" % (note.tread_num / 10000))
        if comment:
            comment.tread_num = Tread.objects.filter(comment=comment).count()
    elif isinstance(instance, Share):
        note.share_num = Share.objects.filter(note=note).count()
        i = note.share_num // 10000
        note.share_str = str(note.share_num) if i == 0 else str("%.1f万" % (note.share_num / 10000))

    # 计算热度值
    note.hot = (note.share_num + note.comment_num) * 10 + note.praise_num * 3 + note.tread_num + note.click_num
    # 计算推荐值
    note.recmd = (note.share_num + note.comment_num + note.praise_num + note.click_num) / (note.tread_num + 1)
    # 计算欢笑值
    note.haha = note.share_num + note.comment_num + note.praise_num + note.click_num
    note.save()
