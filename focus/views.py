import urllib

import markdown2 as markdown2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from focus.forms import LoginForm, CommentForm, RegisterForm
from focus.models import Comment, Praise, NewUser, Note


def index(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数
    loginform = LoginForm()

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id,
               'loginform': loginform}
    return render(request, 'index.html', context)


def index_hot(request):
    return render(request, 'index-hot.html', {})


def index_new(request):
    return render(request, 'index-new.html', {})


def video(request):
    return render(request, 'video.html', {})


def video_hot(request):
    return render(request, 'video-hot.html', {})


def video_new(request):
    return render(request, 'video-new.html', {})


def pic(request):
    return render(request, 'pic.html', {})


def pic_hot(request):
    return render(request, 'pic-hot.html', {})


def pic_new(request):
    return render(request, 'pic-new.html', {})


def jape(request):
    return render(request, 'jape.html', {})


def jape_hot(request):
    return render(request, 'jape-hot.html', {})


def jape_new(request):
    return render(request, 'jape-new.html', {})


def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url', '/focus')
                return redirect(url)
            else:
                return render(request, 'login.html', {'form': form, 'error': "password or username is not ture!"})
        else:
            return render(request, 'login.html', {'form': form})


@login_required
def log_out(request):
    url = request.POST.get('source_url', '/focus')
    logout(request)
    return redirect(url)


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


def register(request):
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'register.html', {'form': form, 'msg': error1})
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form': form, 'msg': "two password is not equal"})
                else:
                    user = NewUser(username=username, email=email, password=password1)
                    user.save()
                    return redirect('/focus/login')
            else:
                return render(request, 'register.html', {'form': form})
