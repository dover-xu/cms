import random

from manager.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from focus.models import MyUser


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
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
                return render(request, 'manager/login.html',
                              {'form': form, 'error': "*用户名或密码错误"})
        else:
            return render(request, 'manager/login.html', {'form': form, 'error': "*登录失败"})
    else:
        request.session['redirect_url'] = request.GET.get('url', '/')
        form = LoginForm()
        return render(request, 'manager/login.html', {'form': form})


@login_required
def log_out(request):
    url = request.GET.get('url', '/')
    logout(request)
    return redirect(url)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username, email, password1, password2 = form.cleaned_data['username'], form.cleaned_data['email'], \
                                                    form.cleaned_data['password1'], form.cleaned_data['password2']
            try:
                MyUser.objects.get(username=username)
                return render(request, 'manager/register.html', {'form': form, 'error': "*用户名已存在！"})
            except ObjectDoesNotExist:
                if len(password1) < 8:
                    form.add_error('password1', '至少包含8位字符')
                    return render(request, 'manager/register.html', {'form': form})
                elif password1.isdigit():
                    form.add_error('password1', '不能全为数字')
                    return render(request, 'manager/register.html', {'form': form})
                elif password1 != password2:
                    form.add_error('password2', '两次密码不一致')
                    return render(request, 'manager/register.html', {'form': form})
                else:
                    pic = '/avatar/default/%d.jpg' % random.randint(1, 4)  # 随机选择默认头像
                    user = MyUser.objects.create_user(username=username, email=email, password=password1, avatar=pic)
                    user.save()
                    return redirect('/manager/login')
        else:
            return render(request, 'manager/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'manager/register.html', {'form': form})
