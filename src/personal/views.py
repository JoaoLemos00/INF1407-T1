from django.shortcuts import render
from blog.models import BlogPost
from django.conf import settings
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from operator import attrgetter
# Create your views here.

def home_screen_view(request):

    context = {}
    
    blog_posts = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts

    page = request.GET.get("page",1)
    blog_posts_paginator = Paginator(blog_posts, settings.BLOG_POST_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(settings.BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts 


    return render(request, "personal/home.html", context)