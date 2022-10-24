from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from allauth.account.models import EmailAddress
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, User
from .forms import PostForm
from .functions import confirmation_required_redirect


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    ordering = ['-dt_created']
    paginate_by = 20
    page_kwargs = 'page'

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'post'

class PostWriteView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    # user모델과 자동으로 연동시킴
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'
    pk_url_kwarg ='page_id'

    raise_exception = True

    def test_func(self, user):
        post = self.get_object()
        return post.author == user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'post'

    raise_exception = True

    def test_func(self, user):
        post = self.get_object()
        return post.author == user

    def get_success_url(self):
        return reverse('post-list')

# PasswordChangeView 오버라이드
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('post-list')


class ProfileView(DetailView):
    model = User
    template_name = 'user/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_posts'] = Post.objects.filter(author__id=user_id)[:5]
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'user/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 20
    page_kwarg = 'page'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author__id=user_id).order_by('-dt_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return context
