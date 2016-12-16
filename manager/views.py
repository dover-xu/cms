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
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url', '/')
                return redirect(url)
            else:
                print("error")
                return render(request, 'manager/login.html',
                              {'form': form, 'error': "*用户名或密码错误"})
        else:
            return render(request, 'manager/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'manager/login.html', {'form': form})


@login_required
def log_out(request):
    url = request.POST.get('source_url', '/')
    logout(request)
    return redirect(url)


def register(request):
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
            try:
                user = MyUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'manager/register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'manager/register.html', {'form': form, 'msg': error1})
        else:
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
                        user = MyUser.objects.create_user(username=username, password=password1)
                        user.save()
                        return redirect('/')
            else:
                return render(request, 'manager/register.html', {'form': form, 'error': "*注册失败"})
    else:
        form = RegisterForm()
        return render(request, 'manager/register.html', {'form': form})
