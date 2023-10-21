from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        'profile/<slug:username>/',
        views.UserProfile.as_view(),
        name='profile'
    ),
    path(
        'posts/create/',
        views.CreatePost.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit',
        views.EditPost.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
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
