import urllib

import markdown2 as markdown2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from focus.forms import CommentForm
from focus.models import Comment, Praise, MyUser, Note
from manager.forms import LoginForm, RegisterForm


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
    return render(request, 'focus/index.html', context)


def index_hot(request):
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
    return render(request, 'focus/index-hot.html', context)


def index_new(request):
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
    return render(request, 'focus/index-new.html', context)


def video(request):
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
    return render(request, 'focus/video.html', context)


def video_hot(request):
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
    return render(request, 'focus/video-hot.html', context)


def video_new(request):
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
    return render(request, 'focus/video-new.html', context)


def pic(request):
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
    return render(request, 'focus/pic.html', context)


def pic_hot(request):
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
    return render(request, 'focus/pic-hot.html', context)


def pic_new(request):
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
    return render(request, 'focus/pic-new.html', context)


def jape(request):
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
    return render(request, 'focus/jape.html', context)


def jape_hot(request):
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
    return render(request, 'focus/jape-hot.html', context)


def jape_new(request):
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
    return render(request, 'focus/jape-new.html', context)


def user_publish(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-publish.html', context)


def user_share(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-share.html', context)


def user_comment(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/u-comment.html', context)


def publish_video(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/publish-video.html', context)


def publish_pic(request):
    if request.method == "POST":
        if 'txt_file' in request.FILES:
            note = Note(user=request.user,
                        text=request.POST.get('text_area'),
                        image=request.FILES.get('txt_file'),
                        category='Picture')
            note.save()
        return render(request, 'focus/publish-pic.html')
    else:
        latest_note_list = Note.objects.query_by_time()
        rows = latest_note_list.count()  # 帖子总条数
        page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

        page_id = int(request.GET.get('page', '1'))
        if page_num > 1:
            latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

        context = {'latest_note_list': latest_note_list,
                   'rows': rows,
                   'page_id': page_id}
        return render(request, 'focus/publish-pic.html', context)


def publish_jape(request):
    latest_note_list = Note.objects.query_by_time()
    rows = latest_note_list.count()  # 帖子总条数
    page_num = (latest_note_list.count() - 1) // 5 + 1  # 总页数

    page_id = int(request.GET.get('page', '1'))
    if page_num > 1:
        latest_note_list = latest_note_list[(page_id - 1) * 5:(page_id - 1) * 5 + 5]

    context = {'latest_note_list': latest_note_list,
               'rows': rows,
               'page_id': page_id}
    return render(request, 'focus/publish-jape.html', context)


def auth_name(request):
    username = request.GET.get('username', 'asdgkg234hsd~jsgasdg')
    try:
        MyUser.objects.get(username=username)
        return HttpResponse("*用户名已存在！")
    except ObjectDoesNotExist:
        return HttpResponse("")


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
