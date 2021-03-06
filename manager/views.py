import base64
import os
import time
import random
import json
import logging
from PIL import Image
# from django.core.mail import send_mail, EmailMultiAlternatives
# from rest_framework.permissions import IsAuthenticated
# from cms.settings import EMAIL_HOST_USER
# from focus.views import repl_with_media_host
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from itsdangerous import URLSafeTimedSerializer as utsr
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from schema.WebSchema import loginSchema, signupSchema
from cms import settings
from focus.models import MyUser
from focus.serializers import MyUserSerializer
from manager.forms import LoginForm, RegisterForm

logger = logging.getLogger('django')

DEFAULT_AVATAR_NUM = 30


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode(encoding='utf-8'))

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(settings.SECRET_KEY)  # 定义为全局变量


def support_form_para(fun):
    def wrapped(self, request):
        if hasattr(request, 'method') and request.method == 'POST' and hasattr(request, 'body'):
            d = dict(json.loads(request.body.decode('utf8')))
            s = ''
            for k, v in d.items():
                if s:
                    s += str('&')
                s += str(k) + '=' + str(v)
            request.form_para = QueryDict(s)
        return fun(self, request)
    return wrapped


class log_in(APIView):
    schema = loginSchema

    @support_form_para
    def post(self, request):
        form = LoginForm(request.form_para)
        if form.is_valid():
            if request.user.is_authenticated:
                context = {
                    'is_login': False,
                    'message': '已登录',
                }
                return JsonResponse(context)
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user = MyUserSerializer(request.user, context={'request': request})
                user_data = user.data  # repl_with_media_host(dict(user.data))
                context = {
                    'is_login': True,
                    'user': user_data,
                    'message': '',
                }
                return JsonResponse(context)
            else:
                context = {
                    'is_login': False,
                    'message': '密码错误',
                }
                try:
                    user = MyUser.objects.get(username=username)
                    if not user.is_active:
                        context['message'] = '请先完成邮箱验证'
                except ObjectDoesNotExist:
                    context['message'] = '用户名不存在'
                return JsonResponse(context)
        else:
            context = {
                'is_login': False,
                'message': '登录失败',
            }
            return JsonResponse(context)


@api_view(['GET'])
def log_out(request):
    """退出登录请求"""
    # url = request.GET.get('url', '/')
    logout(request)
    # return redirect(url)
    context = {
        'is_login': False,
    }
    return JsonResponse(context)


@api_view(['GET'])
def user_state(request):
    """获取用户当前状态"""
    if request.user.is_authenticated:
        is_login = True
    else:
        is_login = False
    user = MyUserSerializer(request.user, context={'request': request})
    user_data = user.data  # repl_with_media_host(dict(user.data))
    context = {
        'is_login': is_login,
        'user': user_data
    }
    return JsonResponse(context)


class signup(APIView):
    schema = signupSchema

    @support_form_para
    def post(self, request):
        form = RegisterForm(request.form_para)
        if form.is_valid():
            username, password1, password2 = form.cleaned_data['username'], \
                                             form.cleaned_data['password1'], form.cleaned_data['password2']
            try:
                MyUser.objects.get(username=username)
                context = {
                    'is_success': False,
                    'message': '用户名已存在'
                }
                return JsonResponse(context)
            except ObjectDoesNotExist:
                if len(password1) < 8:
                    context = {
                        'is_success': False,
                        'message': '至少包含8位字符'
                    }
                    return JsonResponse(context)
                if password1.isdigit():
                    context = {
                        'is_success': False,
                        'message': '不能全为数字'
                    }
                    return JsonResponse(context)
                if password1 != password2:
                    context = {
                        'is_success': False,
                        'message': '两次密码不一致'
                    }
                    return JsonResponse(context)
                pic = '/avatar/default/%d.jpg' % random.randint(1, DEFAULT_AVATAR_NUM)  # 随机选择默认头像
                user = MyUser.objects.create_user(username=username, password=password1, avatar=pic)
                user.is_active = True
                user.save()
                # token = token_confirm.generate_validate_token(username)
                # message = "\n".join(['{0}，欢迎加入我们<br>'.format(username),
                #                      '请访问该链接，完成邮箱验证:',
                #                      r'<a href={0}>点我激活</a>'.format(
                #                          '/'.join([settings.DOMAIN, 'manager/api/activate', token]))
                #                      ])
                # subject, from_email, to = '欢笑江湖-注册用户验证信息', EMAIL_HOST_USER, [email]
                # msg = EmailMultiAlternatives(subject, message, from_email, to)
                # msg.attach_alternative(message, "text/html")
                # msg.send()

                context = {
                    'is_success': True,
                    'message': '注冊成功！',
                }
                return JsonResponse(context)
                # return render(request, 'manager/activate-msg.html', {'title': '注册-欢笑江湖',
                #                                                      'message': '<div class="alert alert-success">'
                #                                                                 '注册成功！'
                #                                                                 '<a href="/manager/login/">'
                #                                                                 '<b>点此登陆</b>'
                #                                                                 '</a>'
                #                                                                 '</div>'})
        else:
            context = {
                'is_success': False,
                'message': '无效表单',
            }
            return JsonResponse(context)


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


class setting(APIView):
    """用户设置"""

    def post(self, request):
        context = {
            'is_success': False}
        username, sex, profile = request.POST.get('username'), request.POST.get('sex'), request.POST.get('profile')
        if not username:
            username = request.user.username
        user = MyUser.objects.filter(username=username)
        if user and user[0].username != request.user.username:
            return JsonResponse(context)
        else:
            old_user = MyUser.objects.filter(username=request.user.username)
            if old_user:
                if not profile:
                    profile = ''
                if 'pic_file' in request.FILES:
                    photo = request.FILES.get('pic_file')
                    img = Image.open(photo)
                    img.thumbnail((120, 120))
                    imgdir = 'avatar/%s/' % time.strftime("%Y/%m/%d", time.localtime())
                    mkdir('uploads/' + imgdir)
                    imgname = '%s_%s.%s' % (
                        time.strftime("%H_%M_%S", time.localtime()), request.user.username, str(photo).split('.')[-1])
                    img.save('uploads/' + imgdir + imgname)
                    filename = ''
                    try:
                        if old_user.first().avatar:
                            filename = old_user.first().avatar.path
                            os.remove(filename)
                    except Exception as reason:
                        logger.warning(str(reason) + '\n[cms] Remove image failed while change avatar. filename:' + filename)
                    old_user.update(avatar=imgdir + imgname, username=username,
                                    sex=sex, profile=profile)
                else:
                    old_user.update(username=username, sex=sex, profile=profile)
                context = {
                    'is_success': True}
                return JsonResponse(context)
        return JsonResponse(context)


def auth_name(request):
    username = request.GET.get('username', 'asdgkg234hsd~jsgasdg')
    try:
        MyUser.objects.get(username=username)
        return HttpResponse("用户名已存在")
    except ObjectDoesNotExist:
        return HttpResponse("")


def activate_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except Exception:
        username = token_confirm.remove_validate_token(token)
        users = MyUser.objects.filter(username=username)
        for user in users:
            user.delete()
        return render(request, 'manager/activate-msg.html',
                      {'title': '邮箱验证-欢笑江湖',
                       'message': '<div class="alert alert-danger">'
                                  '<h4>非常抱歉!</h4>'
                                  '<br>'
                                  r'验证链接已经过期，请重新<a href="/manager/register"><B>注册</B></a>'
                                  '</div>'})
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return render(request, 'manager/activate-msg.html',
                      {'title': '邮箱验证-欢笑江湖',
                       'message': '<div class="alert alert-danger">'
                                  '<h4>非常抱歉!</h4>'
                                  '<br>'
                                  '您所验证的用户(' + username + ')不存在，请重新注册'
                                                          '</div>'})
    user.is_active = True
    user.save()
    message = '<div class="alert alert-success">' \
              '<h4>验证成功</h4>' \
              '<br>' \
              r'您现在可以<a href="/manager/login"><B>登录</B></a>' \
              '</div>'
    return render(request, 'manager/activate-msg.html', {'title': '邮箱验证-欢笑江湖', 'message': message})


def get_email_addr(email):
    addr = email[email.rindex('@') + 1:email.rindex('.')]
    print(email, addr)
    if addr == '163':
        return 'http://mail.163.com/'
    elif addr == '126':
        return 'http://mail.126.com/'
    elif addr == 'sina':
        return 'http://mail.sina.com.cn/'
    elif addr == 'yahoo':
        return 'http://mail.cn.yahoo.com/'
    elif addr == 'sohu':
        return 'http://mail.sohu.com/'
    elif addr == 'yeah':
        return 'http://www.yeah.net/'
    elif addr == 'gmail':
        return 'http://gmail.google.com/'
    elif addr == 'hotmail':
        return 'http://www.hotmail.com/'
    elif addr == 'live':
        return 'http://www.hotmail.com/'
    elif addr == 'qq':
        return 'https://mail.qq.com/'
    elif addr == '139':
        return 'http://mail.10086.cn/'
    else:
        return 'http://www.hao123.com/mail/'
