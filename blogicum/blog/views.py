from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView
                                  )

from .models import (Post,
                     Category,
                     User,
                     Comment)
from .forms import (CreatePostForm,
                    AddCommentForm,)

PAGINATE_VALUE = 10
POSTS_RELATED_OBJECTS = Post.objects.select_related(
    'category',
    'location',
    'author'
)


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = POSTS_RELATED_OBJECTS.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comment'))
    ordering = '-pub_date'
    paginate_by = PAGINATE_VALUE


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = AddCommentForm
    queryset = POSTS_RELATED_OBJECTS

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if not post.is_published and post.author != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related(
            'author',
            'post'
        ).filter(post__id=self.kwargs['pk'])
        return context


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_VALUE

    def get_queryset(self):
        category = get_object_or_404(
            Category.objects.all(),
            slug=self.kwargs['slug'],
            is_published=True
        )
        return POSTS_RELATED_OBJECTS.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__id=category.id
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comment')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.all(),
            is_published=True,
            slug=self.kwargs['slug']
        )
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ('title', 'text', 'category', 'location', 'image')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['pk'])


class AddCommentView(LoginRequiredMixin, CreateView):
    related_post = None
    model = Comment
    form_class = AddCommentForm

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(
            Post.objects.all(), id=kwargs['pk']
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.related_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.related_post.id})


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/create.html'
    fields = ('text',)

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Comment.objects.all(),
                                 post__id=self.kwargs['pk'],
                                 id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['comment_id'],
                                 post__id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['pk']})


class UserProfileView(ListView):
    template_name = 'blog/profile.html'
    author = None
    model = Post
    paginate_by = PAGINATE_VALUE

    def get_queryset(self):
        self.author = get_object_or_404(
            User.objects.all(),
            username=self.kwargs['username']
        )
        if str(self.request.user) == self.author.username:
            return POSTS_RELATED_OBJECTS.filter(
                author__id=self.author.id
            ).order_by(
                '-pub_date'
            ).annotate(
                comment_count=Count('comment')
            )
        return POSTS_RELATED_OBJECTS.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            author__id=self.author.id
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comment')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    fields = ('username', 'email', 'first_name', 'last_name')

    def dispatch(self, request, *args, **kwargs):
        user_profile = get_object_or_404(User.objects.all(),
                                         username=kwargs['username'])
        if user_profile != request.user:
            return redirect('blog:profile', username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.kwargs['username']})
