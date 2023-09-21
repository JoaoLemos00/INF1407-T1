from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import CreateBlogPostForm
from account.models import Account
from django.contrib import messages
from blog.models import BlogPost

# Create your views here.

def create_post_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate.html')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
        messages.success(request, 'Post feito com sucesso!') 
        return redirect('home')

    context['form'] = form

    return render(request,"blog/create_post.html",{})


def detail_post_view(request,slug):

    context = {}

    blog_post = get_object_or_404(BlogPost, slug = slug)
    context['blog_post'] = blog_post

    return render(request,'blog/detail_post.html', context)
