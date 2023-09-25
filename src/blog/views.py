from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import CreateBlogPostForm,UpdateBlogPostFrom, CommentBlogPostForm, UpdateCommentBlogPostForm
from account.models import Account
from django.contrib import messages
from blog.models import BlogPost, CommentBlogPost

from django.http import Http404

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


def detail_post_view(request, slug):

    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post
    
    # Verificar se o método de solicitação é POST (ou seja, o formulário foi enviado)
    if request.POST:
        
        form = CommentBlogPostForm(request.POST)
        
        if form.is_valid():
            
            comment = form.save(commit=False)
            comment.author = request.user  # Atribuir o autor do comentário
            comment.post = blog_post  # Atribuir o post relacionado ao comentário
            comment.save()
            form = CommentBlogPostForm()  # Limpar o formulário após a criação do comentário

        
    else:
        form = CommentBlogPostForm()

    # Recuperar os comentários relacionados a este post
    
    comments = CommentBlogPost.objects.filter(post=blog_post)

    context['form'] = form
    context['comments'] = comments

    return render(request, 'blog/detail_post.html', context)

def edit_post_view(request,slug):

    context = {}

    user = request.user
    if not user.is_authenticated: 
        return redirect('must_authenticate.html')
    
    blog_post = get_object_or_404(BlogPost,slug = slug)

    if blog_post.author != user:
        return redirect("home")

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


def edit_comment_post_view(request, slug, comment_id ):

    context = {}

    comment = get_object_or_404(CommentBlogPost, id=comment_id)
    
    if request.user != comment.author:
        return redirect('blog:detail', slug=comment.post.slug)

    if request.POST:
        form = UpdateCommentBlogPostForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', slug=comment.post.slug)  # Redirecione para a página de detalhes do post após a edição do comentário
    

    form = UpdateBlogPostFrom(
        initial= {
                "body": comment.body,    
        }
    )

    context['form'] = form

    return render(request, 'blog/edit_comment.html', context)
