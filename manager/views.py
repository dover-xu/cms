import base64
import os
import time
from PIL import Image
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from itsdangerous import URLSafeTimedSerializer as utsr
import random
import json

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from cms import settings
from cms.settings import EMAIL_HOST_USER
from focus.views import index
from focus.serializers import MyUserSerializer
from manager.forms import LoginForm, RegisterForm, SettingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from focus.models import MyUser
import logging

logger = logging.getLogger('django')


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


def support_form_para_origin(fun):
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
                context = {
                    'is_login': True,
                    'user': user.data,
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
            # return render(request, 'manager/signin.html', {'form': form, 'message': "*登录失败"})

    # def get(self, request):
    #     return HttpResponse()


def log_in2(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                return render(request, 'manager/signin.html', {'form': form, 'message': "已登录"})
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                r_url = request.session.get('redirect_url', default='/')
                try:
                    del request.session['redirect_url']
                except KeyError:
                    pass
                return redirect(r_url)
            else:
                try:
                    user = MyUser.objects.get(username=username)
                    if not user.is_active:
                        return render(request, 'manager/signin.html', {'form': form, 'message': "请先完成邮箱验证"})
                except ObjectDoesNotExist:
                    return render(request, 'manager/signin.html', {'form': form, 'message': "用户名不存在"})
                return render(request, 'manager/signin.html', {'form': form, 'message': "密码错误"})
        else:
            # return HttpResponse()
            return render(request, 'manager/signin.html', {'form': form, 'message': "登录失败"})
    else:
        request.session['redirect_url'] = request.GET.get('url', '/')
        form = LoginForm()
        # return HttpResponse()
        return render(request, 'manager/signin.html', {'form': form})


@login_required
@api_view(['GET'])
def log_out(request):
    # url = request.GET.get('url', '/')
    logout(request)
    # return redirect(url)
    context = {
        'is_login': False,
    }
    return JsonResponse(context)


@api_view(['GET'])
def user_state(request):
    if request.user.is_authenticated:
        is_login = True
    else:
        is_login = False
    user = MyUserSerializer(request.user, context={'request': request})

    context = {
        'is_login': is_login,
        'user': user.data
    }
    return JsonResponse(context)


def auth_name(request):
    username = request.GET.get('username', 'asdgkg234hsd~jsgasdg')
    try:
        MyUser.objects.get(username=username)
        return HttpResponse("用户名已存在")
    except ObjectDoesNotExist:
        return HttpResponse("")


class signup(APIView):

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
                # return render(request, 'manager/signup.html', {'form': form, 'message': "用户名已存在"})
            except ObjectDoesNotExist:
                if len(password1) < 8:
                    context = {
                        'is_success': False,
                        'message': '至少包含8位字符'
                    }
                    return JsonResponse(context)
                    # form.add_error('password1', '至少包含8位字符')
                    # return render(request, 'manager/signup.html', {'form': form})
                if password1.isdigit():
                    context = {
                        'is_success': False,
                        'message': '不能全为数字'
                    }
                    return JsonResponse(context)
                    # form.add_error('password1', '不能全为数字')
                    # return render(request, 'manager/signup.html', {'form': form})
                if password1 != password2:
                    context = {
                        'is_success': False,
                        'message': '两次密码不一致'
                    }
                    return JsonResponse(context)
                    # form.add_error('password2', '两次密码不一致')
                    # return render(request, 'manager/signup.html', {'form': form})
                pic = '/avatar/default/%d.jpg' % random.randint(1, 4)  # 随机选择默认头像
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
            # return render(request, 'manager/signup.html', {'form': form})

    def get(self, request):
        return HttpResponse()
        # form = RegisterForm()
        # return render(request, 'manager/signup.html', {'form': form})


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

    def post(self, request):
        # form = SettingForm(request.POST)
        # if form.is_valid():
        # username, sex, profile = form.cleaned_data['username'], form.cleaned_data['sex'], form.cleaned_data['profile']
        username, sex, profile = request.POST.get('username'), request.POST.get('sex'), request.POST.get('profile')
        logger.debug(profile)
        if 0 == len(username):
            username = str(request.user)
        user = MyUser.objects.filter(username=username)
        if user and user[0].username != request.user.username:
            # form.add_error('username', '用户名已存在')
            u = MyUser.objects.get(username=request.user)
            context = {
                'is_success': True}
            return JsonResponse(context)
        else:
            old_user = MyUser.objects.filter(username=request.user.username)
            if 0 == len(profile):
                profile = old_user[0].profile
            if 'pic_file' in request.FILES:
                photo = request.FILES.get('pic_file')
                img = Image.open(photo)
                img.thumbnail((120, 120))
                imgdir = 'avatar/%s/' % time.strftime("%Y/%m/%d", time.localtime())
                mkdir('uploads/' + imgdir)
                imgname = '%s_%s.%s' % (
                    time.strftime("%H_%M_%S", time.localtime()), request.user.username, str(photo).split('.')[-1])
                img.save('uploads/' + imgdir + imgname)
                old_user.update(avatar=imgdir + imgname, username=username,
                                sex=sex, profile=profile)
            else:
                old_user.update(username=username, sex=sex, profile=profile)
            context = {
                'is_success': True}
            return JsonResponse(context)


def activate_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
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
