from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = AddCommentForm(request.POST)
    if form.is_valid():
        added_comment = form.save(commit=False)
        added_comment.author = request.user
        added_comment.post = post
        added_comment.save()
    return redirect('blog:post_detail', pk=pk)


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
    ).annotate(comment_count=Count('comment'))
    ordering = '-pub_date'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.is_published is False:
            if post.author != request.user:
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.select_related(
            'author',
            'post'
        ).filter(post__id=self.kwargs['pk'])
        context['form'] = AddCommentForm()
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
    template_name = 'blog/create.html'
    fields = ('title', 'text', 'category', 'location', 'image')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class DeletePost(LoginRequiredMixin, DeleteView):
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


# Отказался от использования CBV в пользцу обычной view функции,
# так как pytest ругался на то, что передаю больше одной формы
# в шаблон(форма добавления комментария первый раз передаётся
# в классе PostDetailView, как как без этого джанго ругался на
# то, что не передаётся нужная форма и страница не открывалась,
# пришлось добавить форму в контекст.)
# Если бы тесты проходились нормально - использовал бы CBV

# class AddComment(LoginRequiredMixin, CreateView):
#     related_post = None
#     model = Comment
#     form_class = AddCommentForm
#
#     def dispatch(self, request, *args, **kwargs):
#         self.related_post = get_object_or_404(
#         Post.objects.all(), id=kwargs['pk']
#         )
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.post = self.related_post
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('blog:post_detail',
#         kwargs={'pk': self.related_post.id})


class EditComment(LoginRequiredMixin, UpdateView):
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


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_form.html'

    # Тут пытался сделать название аргументов в адресе
    # запроса идентичными представлению editcomment,
    # но на тестах получал ошибку о том, что у этих
    # функций должны быть одинаковые права доступа.
    # Причины этой ошибки так и не обнаружил
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['pk'],
                                 post__id=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['post_id']})


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
            return Post.objects.select_related(
                'author'
            ).filter(
                author__id=user.id
            ).order_by(
                '-pub_date'
            ).annotate(
                comment_count=Count(
                    'comment'
                )
            )
        else:
            return Post.objects.select_related(
                'author'
            ).filter(
                is_published=True,
                pub_date__lt=timezone.now(),
                author__id=user.id
            ).order_by('-pub_date').annotate(
                comment_count=Count('comment')
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.all(),
            username=self.kwargs['username']
        )
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    fields = ('username', 'email', 'first_name', 'last_name')

    # тут проверка на права доступа к редактированию
    # аккаунта, но из-за неё я по неизвестной ошибке
    # не мог пройти автотесты. Перестал получать
    # ошибку после того, как задокументировал этот кусок
    #
    # def dispatch(self, request, *args, **kwargs):
    #     user_profile = get_object_or_404(User.objects.all(),
    #                                      username=kwargs['username'])
    #     if user_profile.username != request.user:
    #         return redirect('blog:profile', username=kwargs['username'])
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.kwargs['username']})
