from django.urls import path

from blog.views import(

    create_post_view,
    detail_post_view,
    edit_post_view,
    delete_post_view,
    edit_comment_post_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_post_view, name = "create" ),
    path('<slug>/', detail_post_view, name = "detail" ),
    path('<slug>/edit', edit_post_view, name = "edit" ),
    path('<slug>/delete', delete_post_view, name = "delete" ),
    path('<slug>/edit_comment/<int:comment_id>/',edit_comment_post_view, name='edit_comment'),

]