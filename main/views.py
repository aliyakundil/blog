from django.shortcuts import render
from .models import Post, Category, Likes
from .forms import PostForm, UserRegisterForm, UserLoginForm, SearchForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
# from haystack.query import SeacrhQuerySet
from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


def index(request):
    post = Post.objects.all()
    category2 = Category.objects.all
    return render(request, 'main/index.html', {'post':post, 'category2':category2})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})

def post_new(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        try:
            post.image = request.FILES['image']
        except:
            post.image = post.image
        post.save()
        return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'main/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.title = request.POST['title']
            post.text = request.POST['text']
            post.author = request.user
            post.published_date = timezone.now()
            try:
                post.image = request.FILES['image']
            except:
                post.image = post.image

            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'main/post_edit.html', {'form': form})

def post_delete(request, pk):
    news = Post.objects.get(pk=pk)
    news.delete()
    return redirect('/')

def filter(request, pk):
    post = Post.objects.all()
    if pk == 1:
        now = datetime.now() - timedelta(minutes=60*24*7)
        post = post.filter(created_date__gte=now)
    elif pk == 2:
        now = datetime.now() - timedelta(days=30)
        post = post.filter(created_date__lte=now)
    elif pk == 3:
        post = post

    return render(request, 'main/filter.html', {'post':post})



# def likes(self, request, pk, *args, **kwargs):
#     post = Likes.objects.get(pk=pk)
#
#     is_dislike = False
#
#     for dislike in post.dislikes.all():
#         if dislike == request.user:
#             is_dislike = True
#             break
#
#     if is_dislike:
#         post.dislikes.remove(request.user)
#
#     is_like = False
#
#     for like in post.likes.all():
#         if like == request.user:
#             is_like = True
#             break
#
#     if not is_like:
#         post.likes.add(request.user)
#
#     if is_like:
#         post.likes.remove(request.user)
#
#     return render(reverse('likes', args=[str(pk)]))

class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Likes.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        return HttpResponseRedirect(reverse('video', args=[str(pk)]))

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'login user')
            return redirect('/')
        else:
            messages.error(request, 'Error login')
    else:
        form = UserLoginForm()
    return render(request, 'register/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register Success')
            return redirect('/')
        else:
            messages.error(request, 'Register Error')
    else:
        form = UserRegisterForm()
    return render(request, 'register/register.html', {'form':form})

def show_category(request, pk):
    post = Post.objects.filter(pk=pk)
    all_category = Category.objects.all()
    return render(request, 'main/show_category.html', {
        'all_category' : all_category,
        'post':post
    })

# #  Поиск
# Post.objects.annotate(
#     search = SearchVector('title', 'text')
# ).filter(seacrh='django')

# #  Поиск
# def post_seacrh(request):
#     form = SearchForm()
#     if 'query' in request.GET:
#         if form.is_valid():
#             cd = form.cleaned_data
#             results = SeacrhQuerySet().models(Post).filter(content=cd['query']).load_all()
#             total_result = results.count()
#     return render(request, 'main/search.html',
#                   { 'form': form,
#                     'cd': cd,
#                     'results':results,
#                     'total_result': total_result})



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['text']
    search_fields = ['author', 'title']
    ordering_fields = ['author', 'text']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# СКАЧАТЬ

# pip install -U drf-yasg
# pip install django-filter

def post_detail_view(request, pk):
    handle_page = get_object_or_404(Post, id=pk)
    total_comments = handle_page.comments_blog.all().filter(reply_comment=None).order_by('-id')
    total_comments2 = handle_page.comments_blog.all().order_by('-id')
    total_likes = handle_page.total_likes_post()
    total_saves = handle_page.total_saves_posts()

    context = {}

    context['post'] = handle_page
    return render(request, 'main/post_detail.html', context)

import sys
print(sys.getrecursionlimit())