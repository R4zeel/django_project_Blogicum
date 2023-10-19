from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .models import Post, Category

SLICE_END = 5

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
    queryset = post_filtered_query


class CategoryPostsListView(ListView):
    model = Category
    

def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    current_category = get_object_or_404(
        Category.objects.all(),
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        category__id=current_category.id,
        is_published=True,
        pub_date__lt=timezone.now(),
    )
    context = {
        'category': current_category,
        'post_list': post_list
    }
    return render(request, template_name, context)
