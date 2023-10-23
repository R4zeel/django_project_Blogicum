from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView
                                  )
from django.urls import reverse, reverse_lazy

from .models import (Post,
                     Category,
                     User,
                     Comment)
from .forms import (CreatePostForm,
                    AddCommentForm,
                    EditPostForm)


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    queryset = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    ordering = '-pub_date'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related(
            'author',
            'post'
        )
        context['form'] = AddCommentForm
        return context


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(
            Category.objects.all(),
            slug=self.kwargs['slug']
        )
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = EditPostForm


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post


class AddComment(LoginRequiredMixin, CreateView):
    related_post = None
    model = Comment
    form_class = AddCommentForm

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(Post.objects.all(), id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.related_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.related_post.id})


class EditComment(LoginRequiredMixin, UpdateView):
    model = Comment


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_detail.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        related_post = get_object_or_404(Post.objects.all(), id=self.kwargs['post_id'])
        return get_object_or_404(Comment, post__id=related_post.id, id=self.kwargs['pk'])


class UserProfile(ListView):
    template_name = 'blog/profile.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(
            User.objects.all(),
            username=self.kwargs['username']
        )
        if str(self.request.user) == user.username:
            return Post.objects.select_related('author').filter(author__id=user.id)
        else:
            return Post.objects.select_related(
                'author'
            ).filter(
                is_published=True,
                pub_date__lt=timezone.now(),
                author__id=user.id
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.all(),
            username=self.kwargs['username']
        )
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    user_profile = None
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    fields = ('username', 'email', 'first_name', 'last_name')

    def dispatch(self, request, *args, **kwargs):
        self.user_profile = get_object_or_404(User.objects.all(), username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.user_profile.username})
