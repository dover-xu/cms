# coding=utf-8
import json
import os
import time
import re
import coreapi
import coreschema
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from focus.models import Comment, Praise, MyUser, Note, Tread, Share
from focus.permissions import IsOwnerOrReadOnly
from manager.forms import LoginForm
from focus.serializers import MyUserSerializer, NoteSerializer, CommentSerializer, PraiseSerializer, TreadSerializer, \
    ShareSerializer
from rest_framework import status, authentication
from rest_framework import schemas
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, list_route, detail_route
from rest_framework.schemas import SchemaGenerator, ManualSchema
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
# from cms.settings import FRONTEND_HOST_PORT
from PIL import Image
from schema.WebSchema import contentsSchema, ucenterSchema, delNoteOrCommentSchema, publishSchema, addCommentSchema, \
    addPraiseTreadShareSchema, detailsSchema
from focus.tasks import async_log


TYPE_ALL = 0
TYPE_PIC = 1
TYPE_JAPE = 2
SORT_RECMD = 0
SORT_NEW = 1
SORT_HOT = 2

USER_NOTE = 0
USER_SHARE = 1
USER_COMMENT = 2


class log(object):

    @staticmethod
    def debug(message):
        async_log.delay('debug', message)

    @staticmethod
    def info(message):
        async_log.delay('info', message)

    @staticmethod
    def warn(message):
        async_log.delay('warn', message)

    @staticmethod
    def error(message):
        async_log.delay('error', message)


class SwaggerSchemaView(APIView):
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]

    def get(self, request):
        generator = SchemaGenerator(title='Backend API Document@www.hahajh.com', urlconf='cms.urls')
        schema = generator.get_schema(request=request)
        return Response(schema)


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Core API')
    return Response(generator.get_schema(request=request))


class MyUserViewSet(viewsets.ModelViewSet):
    """
    用户Model
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class NoteViewSet(viewsets.ModelViewSet):
    """
    帖子Model
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
    评论Model
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PraiseViewSet(viewsets.ModelViewSet):
    """
    点赞Model
    """
    queryset = Praise.objects.all()
    serializer_class = PraiseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TreadViewSet(viewsets.ModelViewSet):
    """
    踩Model
    """
    queryset = Tread.objects.all()
    serializer_class = TreadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShareViewSet(viewsets.ModelViewSet):
    """
    分享Model
    """
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# def repl_with_media_host(datas):
#     if isinstance(datas, dict) and 'avatar' in datas and datas['avatar']:
#         datas['avatar'] = re.sub(r'http://\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{4}/', FRONTEND_HOST_PORT, datas['avatar'])
#     elif isinstance(datas, list):
#         for data in datas:
#             if 'image' in data and data['image']:
#                 data['image'] = re.sub(r'http://\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{4}/', FRONTEND_HOST_PORT,
#                                        data['image'])
#             if 'user' in data and 'avatar' in data['user'] and data['user']['avatar']:
#                 data['user']['avatar'] = re.sub(r'http://\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{4}/', FRONTEND_HOST_PORT,
#                                                 data['user']['avatar'])
#     return datas


def append_praise_tread_info(request, data):
    if request.user.is_authenticated:
        for n in data:
            if Praise.objects.filter(user=request.user, note__id=n['id']):
                n['Praised'] = True
            else:
                n['Praised'] = False
            if Tread.objects.filter(user=request.user, note__id=n['id']):
                n['Treaded'] = True
            else:
                n['Treaded'] = False
    return data


def append_detail_url(data):
    for n in data:
        n['detail_url'] = '/detail/' + str(n['id'])
    return data


def crop_image_for_hxjx(data):
    for n in data:
        path = '/'.join(n['image'].split('/')[3:])
        host = '/'.join(n['image'].split('/')[:3]) + '/'
        dirpath = os.path.dirname(path) + '/'
        filename = 'crop_' + os.path.basename(path)
        img = Image.open(path)
        width = img.size[0]
        height = img.size[1]
        want_height = width * 0.618
        if height > want_height:
            img2 = img.crop((0, 20, width, want_height + 20))
            img2.save(dirpath + filename)
            n['image_crop'] = host + dirpath + filename
    return data


def get_noteset_by_type_and_sort(tp, sort):
    query_set = None
    if tp == TYPE_ALL:
        if sort == SORT_RECMD:
            query_set = Note.objects.query_all_by_recommend()
        elif sort == SORT_NEW:
            query_set = Note.objects.query_all_by_time()
        elif sort == SORT_HOT:
            query_set = Note.objects.query_all_by_hot()
    elif tp == TYPE_PIC:
        if sort == SORT_RECMD:
            query_set = Note.objects.query_pic_by_recommend()
        elif sort == SORT_NEW:
            query_set = Note.objects.query_pic_by_time()
        elif sort == SORT_HOT:
            query_set = Note.objects.query_pic_by_hot()
    elif tp == TYPE_JAPE:
        if sort == SORT_RECMD:
            query_set = Note.objects.query_jape_by_recommend()
        elif sort == SORT_NEW:
            query_set = Note.objects.query_jape_by_time()
        elif sort == SORT_HOT:
            query_set = Note.objects.query_jape_by_hot()
    return query_set


class ucenter(APIView):
    schema = ucenterSchema

    def post(self, request):
        if request.user.is_authenticated:
            is_login = True
        else:
            is_login = False
        user = MyUserSerializer(request.user, context={'request': request})
        user_data = user.data  # repl_with_media_host(dict(user.data))
        post_data = json.loads(request.body.decode('utf8'))
        tp = post_data.get('type')  # 统计类别
        current = post_data.get('current')
        page_size = post_data.get('display')  # 每页显示帖子数
        if (not tp and tp != 0) or not current or not page_size:
            context = {'message': '参数type, current, display不能为空'}
            return JsonResponse(data=context, status=status.HTTP_200_OK)

        if tp == USER_NOTE:
            query_set = Note.objects.query_by_user(request.user)
        elif tp == USER_SHARE:
            query_set = Share.objects.filter(user=request.user).order_by('-share_date')
        elif tp == USER_COMMENT:
            query_set = Comment.objects.filter(user=request.user).order_by('-pub_date')
        else:
            context = {'message': '参数type的值不正确'}
            return JsonResponse(data=context, status=status.HTTP_200_OK)
        total = query_set.count()  # 帖子总条数
        # page_size = 5  # 每页显示帖子数

        if total / page_size > 1:
            start = (current - 1) * page_size
            end = current * page_size
            query_set = query_set[start:end]
        notes = NoteSerializer(query_set, many=True, context={'request': request})
        notes_data = notes.data  # repl_with_media_host(notes.data)
        notes_data = append_praise_tread_info(request, notes_data)
        context = {
            'is_login': is_login,
            'user': user_data,
            'note_list': notes_data,
            'total': total,
            'current': current}
        return JsonResponse(data=context, status=status.HTTP_200_OK)


class contents(APIView):
    schema = contentsSchema

    def post(self, request):
        is_login = True if request.user.is_authenticated else False
        user = MyUserSerializer(request.user, context={'request': request})
        user_data = user.data  # repl_with_media_host(dict(user.data))

        post_data = json.loads(request.body.decode('utf8'))
        tp = post_data.get('type')
        sort = post_data.get('sort')
        current = post_data.get('current')
        page_size = post_data.get('display')  # 每页显示帖子数
        if (not tp and tp != 0) or (not sort and sort != 0) or not current or not page_size:
            context = {'message': '参数type, sort, current, display不能为空'}
            return JsonResponse(context)
        query_set = get_noteset_by_type_and_sort(tp, sort)
        if query_set is None:
            return JsonResponse(status=status.HTTP_200_OK)

        total = query_set.count()
        if current > 0 and total / page_size > 1:
            start = (current - 1) * page_size
            end = current * page_size
            query_set = query_set[start:end]
        notes = NoteSerializer(query_set, many=True, context={'request': request})
        notes_data = notes.data  # repl_with_media_host(notes.data)
        notes_data = append_praise_tread_info(request, notes_data)

        context = {
            'is_login': is_login,
            'user': user_data,
            'note_list': notes_data,
            'total': total,
            'display': page_size,
            'current': current}
        return JsonResponse(data=context, status=status.HTTP_200_OK)


class note_jx(APIView):
    """获取精选帖子"""
    def get(self, request):
        query_set_haha = Note.objects.query_by_haha()
        notes_haha = NoteSerializer(query_set_haha[:4], many=True, context={'request': request})
        notes_haha_data = notes_haha.data  # repl_with_media_host(notes_haha.data)
        notes_haha_data = append_detail_url(notes_haha_data)
        notes_haha_data = crop_image_for_hxjx(notes_haha_data)  # 欢笑精选截图
        context = {
            'note_haha_list': notes_haha_data,
        }
        return JsonResponse(context)


class details(APIView):
    schema = detailsSchema

    def post(self, request):
        if request.user.is_authenticated:
            is_login = True
        else:
            is_login = False
        user = MyUserSerializer(request.user, context={'request': request})
        user_data = user.data  # repl_with_media_host(dict(user.data))
        post_data = json.loads(request.body.decode('utf8'))
        note_id = post_data.get('id')
        current = post_data.get('current')
        page_size = post_data.get('display')  # 每页显示评论数
        if note_id is None or current is None or page_size is None:
            context = {'message': '参数id，current，page_size不能为空'}
            return JsonResponse(context)
        comment_set = Comment.objects.filter(note=note_id).order_by('-pub_date')
        total = comment_set.count()

        if total / page_size > 1:
            start = (current - 1) * page_size
            end = current * page_size
            comment_set = comment_set[start:end]
        comments = CommentSerializer(comment_set, many=True, context={'request': request})
        comments_data = comments.data  # repl_with_media_host(comments.data)

        note_set = Note.objects.filter(id=note_id)
        if len(note_set) > 0:
            note_set[0].click_num += 1
            note_set[0].save()
        else:
            context = {'message': '帖子不存在'}
            return JsonResponse(context)
        notes = NoteSerializer(note_set, many=True, context={'request': request})
        notes_data = notes.data  # repl_with_media_host(notes.data)
        notes_data = append_praise_tread_info(request, notes_data)

        context = {
            'user': user_data,
            'is_login': is_login,
            'note': notes_data[0],
            'comments': comments_data,
            'total': total,
            'current': current,
            'display': page_size,
        }
        return JsonResponse(context)


class publish(APIView):
    schema = publishSchema

    def post(self, request):
        context = {
            'is_success': False,
            'message': '',
        }
        if 'pic' in request.FILES:
            photo = request.FILES.get('pic')
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
            context['is_success'] = True
            return JsonResponse(context)
        elif 'text_area' in request.POST:
            note = Note(user=request.user,
                        text=request.POST.get('text_area'),
                        category='Jape')
            note.save()
            context['is_success'] = True
            return JsonResponse(context)
        else:
            return JsonResponse(context)


class add_praise_tread_share(APIView):
    schema = addPraiseTreadShareSchema

    def post(self, request):
        post_data = json.loads(request.body.decode('utf8'))
        action = post_data.get('action')
        note_id = post_data.get('note_id')
        context = {
            'is_success': False,
            'message': '',
            'action': action,
        }
        if note_id is None:
            context['message'] = '帖子ID不能为空'
            return JsonResponse(context)
        if not action:
            context['message'] = '请求类型不能为空'
            return JsonResponse(context)
        note = Note.objects.filter(id=note_id).first()
        if note:
            if action == 'praise':
                if request.user.is_authenticated:
                    note.increase_praise()
                    note.save()
                    praise = Praise.objects.filter(user=request.user, note=note).first()
                    if not praise:
                        Praise.objects.create(user=request.user, note=note)
                        context['is_success'] = True
                    else:
                        context['is_success'] = False
                        context['message'] = '不能重复点赞'
                    context['praise_num'] = note.praise_num
                    return JsonResponse(context)
            elif action == 'tread':
                if request.user.is_authenticated:
                    note.increase_tread()
                    note.save()
                    tread = Tread.objects.filter(user=request.user, note=note).first()
                    if not tread:
                        Tread.objects.create(user=request.user, note=note)
                        context['is_success'] = True
                    else:
                        context['is_success'] = False
                        context['message'] = '不能重复点踩'
                    context['tread_num'] = note.tread_num
                    return JsonResponse(context)
            elif action == 'share':
                if request.user.is_authenticated:
                    note.increase_share()
                    note.save()
                    share = Share.objects.filter(user=request.user, note=note).first()
                    if not share:
                        Share.objects.create(user=request.user, note=note)
                        context['is_success'] = True
                    else:
                        context['is_success'] = False
                        context['message'] = '不能重复点踩'
                    context['share_num'] = note.share_num
                    return JsonResponse(context)
            else:
                context['is_success'] = False
                context['message'] = '帖子不存在'
                return JsonResponse(context)
        else:
            log.warn('[add_praise_tread_share]: 帖子不存在')
            context['message'] = '帖子不存在'
        return JsonResponse(context)


class add_comment(APIView):
    schema = addCommentSchema

    def post(self, request):
        post_data = json.loads(request.body.decode('utf8'))
        text = post_data.get('text')
        note_id = post_data.get('note_id')
        context = {
            'is_success': False,
            'message': ''
        }
        if not text:
            context['message'] = '内容不存在'
            return JsonResponse(context)
        if note_id is None:
            context['message'] = '帖子ID不能为空'
            return JsonResponse(context)
        note = Note.objects.filter(id=note_id).first()
        if note:
            note.increase_comment()
            note.save()
            Comment.objects.create(user=request.user, note=note, text=text)
            context['is_success'] = True
        else:
            log.warn('[add_comment]: 帖子不存在')
            context['message'] = '帖子不存在'

        return JsonResponse(context)


@api_view(['POST'])
def del_note(request):
    """
    删帖
    :param request:
    :return:
    """
    context = {
        'is_success': False
    }
    if request.body:
        post_data = json.loads(request.body.decode('utf8'))
        note_id = post_data.get('note_id', '_no_id_error_')
        try:
            note = Note.objects.filter(id=note_id).first()
            try:
                if note.image:
                    filename = note.image.path
                    os.remove(filename)
            except Exception as reason:
                log.warn('[del_note]: 删除图片失败: ' + str(reason))
            note.delete()
        except Exception as reason:
            log.warn('[del_note]: 删除帖子失败: ' + str(reason))
            return JsonResponse(context)
        context['is_success'] = True
        return JsonResponse(context)
    return JsonResponse(context)


class del_note_comment(APIView):
    schema = delNoteOrCommentSchema

    def post(self, request):
        context = {
            'is_success': False,
            'delete_note': False,
            'delete_comment': False
        }
        if request.body:
            post_data = json.loads(request.body.decode('utf8'))
            note_id = post_data.get('note_id')
            comment_id = post_data.get('comment_id')
            if note_id:
                note = Note.objects.filter(id=note_id).first()
                if note:
                    try:
                        if note.image:
                            filename = note.image.path
                            os.remove(filename)
                    except Exception as reason:
                        log.warn('[del_note]: 删除图片失败: ' + str(reason))
                    note.delete()
                    context['is_success'] = True
                    context['delete_note'] = True
                else:
                    log.warn('[del_note]: 删除帖子失败')

            if comment_id:
                comment = Comment.objects.filter(id=comment_id).first()
                if comment:
                    comment.delete()
                    context['is_success'] = True
                    context['delete_comment'] = True
                else:
                    log.warn('[del_note]: 删除评论失败:')

            return JsonResponse(context)
        return JsonResponse(context)


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
