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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
            return render(request, 'manager/login.html', {'form': form})
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
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            try:
                MyUser.objects.get(username=username)
                return render(request, 'manager/register.html', {'form': form, 'error': "*用户名已存在！"})
            except ObjectDoesNotExist:
                if password1 != password2:
                    return render(request, 'manager/register.html', {'form': form, 'error': "*请确保两次输入密码一致！"})
                else:
                    pic = '/avatar/default/%d.jpg' % random.randint(1, 4)
                    user = MyUser.objects.create_user(username=username, password=password1,
                                                      avatar=pic)
                    user.save()
                    return redirect('/manager/login')
        else:
            return render(request, 'manager/register.html', {'form': form, 'error': "*注册失败"})
    else:
        form = RegisterForm()
        return render(request, 'manager/register.html', {'form': form})
