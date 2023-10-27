from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        'profile/<slug:username>/',
        views.UserProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.EditProfileView.as_view(),
        name='edit_profile'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:pk>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_id>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:comment_id>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),
    path
    (
        'category/<slug:slug>/',
        views.CategoryPostsView.as_view(),
        name='category_posts'
    ),
    path
    (
        '',
        views.PostListView.as_view(),
        name='index'
    ),
]
