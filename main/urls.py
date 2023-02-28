from django.urls import path
from .views import *
from rest_framework import routers

routers = routers.SimpleRouter()

routers.register(r'post_', PostViewSet)
routers.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('post_edit/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', post_delete, name='post_delete'),
    path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post_new/', post_new, name='post_new'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('filter/<int:pk>/', filter, name='filter'),
    path('show_category/<int:pk>', show_category, name='show_category'),
    # path('last_post/<int:pk>', last_post, name='last_post'),
    # path('search', post_seacrh, name='post_seacrh'),
]

urlpatterns += routers.urls
