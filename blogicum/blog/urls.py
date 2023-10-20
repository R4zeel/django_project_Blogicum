from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        'profile/<slug:username>/',
        views.UserProfile.as_view(),
        name='profile'
    ),
    path
    (
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
