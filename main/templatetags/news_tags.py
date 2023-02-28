from main.models import Category, Post
from django import template
from django.db.models import Count, F

register = template.Library()

# @register.simple_tag(name='get_list_category')
# def get_category():
#     return Category.objects.all()

@register.inclusion_tag('main/show_category.html')
def show_category():
    categories = Category.objects.annotate(
        cnt=Count('post',
            filter=F('post__is_category_id')
                  )).filter(cnt_gt=0)
    return {'categories':categories}

# @register.inclusion_tag('main/show_category.html')
# def get_last_post():
#     posts = Post.objects.order_by('id')[:3]
#     return {'last_post':posts}

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('main/show_category.html')
def last_post(count=3):
    return {'last_post':Post.objects.order_by('-id')[:count]}

@register.simple_tag()
def get_categories2(count=3):
    return Post.objects.order_by('-id')[:count]
#
# @register.inclusion_tag('main/show_category.html')
# def get_last_post():
#     post = Post.objects.order_by('id')[:3]
#     return {'last_post':post}