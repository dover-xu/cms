import os
import time
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from focus.models import Comment, Praise, MyUser, Note, Tread, Share
from focus.permissions import IsOwnerOrReadOnly
from manager.forms import LoginForm
from PIL import Image
from focus.serializers import MyUserSerializer, NoteSerializer, CommentSerializer, PraiseSerializer, TreadSerializer, \
    ShareSerializer
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes, list_route, detail_route
from rest_framework import schemas
from rest_framework import permissions
import logging

logger = logging.getLogger('django')


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Core API')
    return Response(generator.get_schema(request=request))


# @api_view(['GET'])
# def api_root(request, format=None):
#     from rest_framework.response import Response
#     return Response({
#         'users': reverse('myuser-list', request=request, format=format),
#         'notes': reverse('note-list', request=request, format=format)
#     })


class MyUserViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑user的API endpoint
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class NoteViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑note的API endpoint
    """
    queryset = Note.objects.query_all_by_hot()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @list_route(methods=['get', 'post', 'delete'])
    def list_handler(self, request):
        context = {
            'p': 0
        }
        return Response(context)

    @detail_route(methods=['get'])
    def detail_handler(self, request, pk=None):
        context = {
            'p': 0
        }
        return Response(context)

        # def perform_create(self, serializer):
        #     serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑Comment的API endpoint
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PraiseViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑Comment的API endpoint
    """
    queryset = Praise.objects.all()
    serializer_class = PraiseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TreadViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑Comment的API endpoint
    """
    queryset = Tread.objects.all()
    serializer_class = TreadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShareViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑Comment的API endpoint
    """
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def index(request):
    note_jx = Note.objects.query_pic_by_hot()[:4]
    note_list = Note.objects.query_all_by_time()
    rows = note_list.count()  # 帖子总数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'note_jx': note_jx,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/index.html', context)


class contents(APIView):
    def get(self, request):
        tp = request.GET.get('type', '0')
        sort = request.GET.get('sort', '0')
        current = int(request.GET.get('page', '1'))
        page_size = int(request.GET.get('display', '5'))  # 每页显示帖子数

        query_set = None
        if tp == '0':
            if sort == '0':
                query_set = Note.objects.query_all_by_time()
            elif sort == '1':
                query_set = Note.objects.query_all_by_time()
            elif sort == '2':
                query_set = Note.objects.query_all_by_hot()
        elif tp == '1':
            if sort == '0':
                query_set = Note.objects.query_pic_by_time()
            elif sort == '1':
                query_set = Note.objects.query_pic_by_time()
            elif sort == '2':
                query_set = Note.objects.query_pic_by_hot()
        elif tp == '2':
            if sort == '0':
                query_set = Note.objects.query_jape_by_time()
            elif sort == '1':
                query_set = Note.objects.query_jape_by_time()
            elif sort == '2':
                query_set = Note.objects.query_jape_by_hot()
        if query_set is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # query_set = Note.objects.query_jape_by_hot()
        total = query_set.count()
        # total = (query_set.count() - 1) // page_size + 1  # 总页数

        if total / page_size > 1:
            start = (current - 1) * page_size
            end = current * page_size
            query_set = query_set[start:end]
        ser = NoteSerializer(query_set, many=True, context={'request': request})
        context = {'note_list': ser.data,
                   'total': total,
                   'display': page_size,
                   'current': current}
        return Response(context)

    def post(self, request):
        return Response()


@api_view(['GET'])
def index_hot2(request):
    if request.method == 'GET':
        query = Note.objects.all()
        se = NoteSerializer(query, many=True, context={'request': request})
        logger.debug(se.data)
        return Response(se.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def index_hot1(request):
    note_list = Note.objects.query_all_by_hot()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False

    user = MyUser.objects.get(id=note_list[0].user.id)
    u = {'avatar': {'url': user.avatar.url}, 'username': user.username}

    note = note_list[0]
    note_dict = {
        'id': note.id,
        'test': note.text,
        'user': u,
        'image': note.image.url,
        'pub_date': note.pub_date,
        'P': False,
        'T': False,
        'praise_str': note.praise_str,
        'tread_str': note.tread_str,
        'comment_str': note.comment_str
    }

    query = MyUser.objects.all()
    # se = serializers.serialize('json', query, use_natural_foreign_keys=True, fields=(
    #     'text', 'user', 'image', 'pub_date', 'P', 'T', 'praise_str', 'tread_str', 'comment_str'))
    # logger.info(se)
    # note_dict = serializers.serialize("json", note_list)
    # context = {'note_list': note_dict}

    # context = {'note_list': note_dict,
    #            'rows': rows,
    #            'page_id': page_id}
    # 'loginform': loginform}

    se = MyUserSerializer(query, context={'request': request})
    return JsonResponse(se.data)
    # return render(request, 'focus/index-hot.html', context)


def index_new(request):
    note_list = Note.objects.query_all_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/index-new.html', context)


def video(request):
    note_list = Note.objects.query_all_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/video.html', context)


def video_hot(request):
    note_list = Note.objects.query_all_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/video-hot.html', context)


def video_new(request):
    note_list = Note.objects.query_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/video-new.html', context)


def pic(request):
    note_list = Note.objects.query_pic_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/pic.html', context)


def pic_hot(request):
    note_list = Note.objects.query_pic_by_hot()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/pic-hot.html', context)


def pic_new(request):
    note_list = Note.objects.query_pic_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/pic-new.html', context)


def jape(request):
    note_list = Note.objects.query_jape_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/jape.html', context)


def jape_hot(request):
    note_list = Note.objects.query_jape_by_hot()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/jape-hot.html', context)


def jape_new(request):
    note_list = Note.objects.query_jape_by_time()
    rows = note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        note_list = note_list[(page_id - 1) * page_size:page_id * page_size]
    if request.user.is_authenticated:
        for n in note_list:
            if Praise.objects.filter(user=request.user, note=n):
                n.P = True
            else:
                n.P = False
            if Tread.objects.filter(user=request.user, note=n):
                n.T = True
            else:
                n.T = False
    context = {'note_list': note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'focus/jape-new.html', context)


def user_publish(request):
    notes = Note.objects.query_by_user(request.user)
    rows = notes.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        notes = notes[(page_id - 1) * page_size:page_id * page_size]

    context = {'latest_note_list': notes,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-publish.html', context)


def user_share(request):
    # latest_note_list = Note.objects.query_all_by_time()
    share_list = Share.objects.filter(user=request.user).order_by('-share_date')
    rows = share_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        share_list = share_list[(page_id - 1) * page_size:page_id * page_size]

    context = {'share_list': share_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-share.html', context)


def user_comment(request):
    comment_list = Comment.objects.filter(user=request.user).order_by('-pub_date')
    filter_list = []
    notes = []
    for comment in comment_list:
        if comment.note not in notes:
            notes.append(comment.note)
            filter_list.append(comment)
    rows = len(filter_list)  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (rows - 1) // page_size + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        filter_list = filter_list[(page_id - 1) * page_size:page_id * page_size]

    context = {'comment_list': filter_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-comment.html', context)


# 暂未用，保留
def publish_video(request):
    latest_note_list = Note.objects.query_all_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_size = 5  # 每页显示帖子数
    page_num = (latest_note_list.count() - 1) // page_size + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * page_size:page_id * page_size]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/publish-video.html', context)


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


def publish_pic(request):
    if request.method == "POST":
        if 'txt_file' in request.FILES:
            photo = request.FILES.get('txt_file')
            img = Image.open(photo)
            img.thumbnail((600, 100000))
            imgdir = 'images/%s/' % time.strftime("%Y/%m/%d", time.localtime())
            mkdir('uploads/' + imgdir)
            imgname = '%s_%s.%s' % (
                time.strftime("%H_%M_%S", time.localtime()), str(request.user), str(photo).split('.')[-1])
            img.save('uploads/' + imgdir + imgname)
            note = Note(user=request.user,
                        text=request.POST.get('text_area'),
                        image=imgdir + imgname,
                        category='Picture')
            note.save()
            return redirect('/user/focus/publish')
        else:
            return render(request, 'focus/publish-pic.html', {})
    else:
        return render(request, 'focus/publish-pic.html', {})


def publish_jape(request):
    if request.method == "POST":
        if 'text_area' in request.POST:
            note = Note(user=request.user,
                        text=request.POST.get('text_area'),
                        category='Jape')
            note.save()
            return redirect('/user/focus/publish')
        else:
            return render(request, 'focus/publish-jape.html', {})
    else:
        return render(request, 'focus/publish-jape.html', {})


def detail(request, note_id):
    comments = Comment.objects.filter(note=note_id).order_by('-pub_date')
    n = Note.objects.query_by_id(note_id)
    n.click_num += 1
    n.save()
    loginform = LoginForm()
    if request.user.is_authenticated:
        if Praise.objects.filter(user=request.user, note=n):
            n.P = True
        else:
            n.P = False
        if Tread.objects.filter(user=request.user, note=n):
            n.T = True
        else:
            n.T = False
    context = {'note': n,
               'comments': comments,
               'loginform': loginform}
    return render(request, 'focus/comment.html', context)


def add_praise_tread_share(request):
    action = request.GET.get('action', 'ashf383$#^HHV')
    note_id = request.GET.get('note_id', 'ashf383$#^HHV')
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return HttpResponse(-1)
    if action == 'praise':
        if request.user.is_authenticated:
            note.praise_num += 1
            note.save()
            try:
                Praise.objects.get(user=request.user, note=note)
            except Praise.DoesNotExist:
                Praise.objects.create(user=request.user, note=note)
        return HttpResponse(note.praise_num)
    elif action == 'tread':
        if request.user.is_authenticated:
            note.tread_num += 1
            note.save()
            try:
                Tread.objects.get(user=request.user, note=note)
            except Tread.DoesNotExist:
                Tread.objects.create(user=request.user, note=note)
        return HttpResponse(note.tread_num)
    elif action == 'share':
        if request.user.is_authenticated:
            note.share_num += 1
            print('share:', note.share_num)
            note.save()
            try:
                Share.objects.get(user=request.user, note=note)
            except Share.DoesNotExist:
                Share.objects.create(user=request.user, note=note)
                print('share add')
        return HttpResponse(note.share_num)
    else:
        return HttpResponse(-1)


@login_required
def add_comment(request):
    txt = request.POST.get('txt', '873217asT&^HKhkdfg')
    note_id = request.POST.get('note_id', '873217asT&^HKhkdfg')
    if txt == '873217asT&^HKhkdfg':
        return HttpResponse('内容不存在')
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return HttpResponse('帖子不存在')
    note.comment_num += 1
    note.save()
    Comment.objects.create(user=request.user, note=note, text=txt)
    return HttpResponse(note.comment_str)


@login_required
def del_note(request):
    note_id = request.GET.get('note_id', '^bkh*bbdsf88sdfg458')
    redirect_url = request.GET.get('url', '^bkh*bbdsf88sdfg458')
    if redirect_url == '^bkh*bbdsf88sdfg458':
        redirect_url = '/user/focus/publish'
    try:
        note = Note.objects.get(id=note_id)
        note.delete()
    except Note.DoesNotExist:
        return redirect(redirect_url)
    return redirect(redirect_url)

# def article(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     content = markdown2.markdown(article.content, extras=["code-friendly",
#                                                           "fenced-code-blocks", "header-ids", "toc", "metadata"])
#     commentform = CommentForm()
#     loginform = LoginForm()
#     comments = article.comment_set.all
#
#     return render(request, 'article_page.html', {
#         'article': article,
#         'loginform': loginform,
#         'commentform': commentform,
#         'content': content,
#         'comments': comments
#     })

# @login_required
# def comment(request, article_id):
#     form = CommentForm(request.POST)
#     url = urllib.parse.urljoin('/focus', article_id)
#     if form.is_valid():
#         user = request.user
#         article = Article.objects.get(id=article_id)
#         new_comment = form.cleaned_data['comment']
#         C = Comment(content=new_comment, article_id=article_id)
#         C.user = user
#         C.save()
#         article.comment_num += 1
#     return redirect(url)
#
#
# @login_required
# def get_keep(request, article_id):
#     logged_user = request.user
#     article = Article.objects.get(id=article_id)
#     articles = logged_user.article_set.all()
#     if article not in articles:
#         article.user.add(logged_user)
#         article.keep_num += 1
#         article.save()
#         return redirect('/focus/')
#     else:
#         url = urllib.parse.urljoin('/focus/', article_id)
#         return redirect(url)
#
#
# @login_required
# def get_praise_article(request, note_id):
#     logged_user = request.user
#     article = Article.objects.get(id=note_id)
#     praises = logged_user.praise_set.all()
#     articles = []
#     for praise in praises:
#         articles.append(praise.article)
#     if article in articles:
#         url = urllib.parse.urljoin('/focus', note_id)
#         return redirect(url)
#     else:
#         article.praise_num += 1
#         article.save()
#         praise = Praise(user=logged_user, note=note_id)
#         praise.save()
#         data = {}
#         return redirect('/focus/')
