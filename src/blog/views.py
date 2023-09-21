from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import CreateBlogPostForm,UpdateBlogPostFrom
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

def delete_post_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)

    if request.POST:
        blog_post.image.delete()
        blog_post.delete()
        messages.success(request, 'Post excluído com sucesso!')
        return redirect('home')

    
    context['blog_post'] = blog_post

    return render(request, 'blog/delete_post.html', context)


def detail_post_view(request,slug):

    context = {}

    blog_post = get_object_or_404(BlogPost, slug = slug)
    context['blog_post'] = blog_post

    return render(request,'blog/detail_post.html', context)

def edit_post_view(request,slug):
    context = {}

    user = request.user
    if not user.is_authenticated: 
        return redirect('must_authenticate.html')
    
    blog_post = get_object_or_404(BlogPost,slug = slug)
    if request.POST:
        form = UpdateBlogPostFrom(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()  
            messages.success(request, 'Post atualizado com sucesso!') 
            blog_post = obj
            return redirect('home')

    form = UpdateBlogPostFrom(
        initial= {
                "title": blog_post.title,
                "body": blog_post.body,
                "image": blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_post.html', context)