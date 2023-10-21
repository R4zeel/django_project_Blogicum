from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  )

from .models import Post, Category, User
from .forms import CreatePostForm


def post_filtered_query():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = post_filtered_query()
    ordering = '-pub_date'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category.objects.all(), slug=self.kwargs['slug'])
        return Post.objects.select_related(
            'category'
        ).filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__id=category.id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.all(),
            is_published=True,
            slug=self.kwargs['slug']
        )
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'


class EditPost(LoginRequiredMixin, DetailView):
    ...


class UserProfile(DetailView):
    template_name = 'blog/profile.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'





