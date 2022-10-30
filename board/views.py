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
from .models import Post, User, Comment
from .forms import PostForm, ProfileForm, CommentForm
from .functions import confirmation_required_redirect
from .mixins import LoginAndOwnershipRequiredMixin, LoginAndVerificationRequiredMixin


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    page_kwargs = 'page'

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostWriteView(LoginAndVerificationRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    # user모델과 자동으로 연동시킴
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

class PostUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'
    pk_url_kwarg ='page_id'

    raise_exception = True

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

class PostDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'post'

    raise_exception = True

    def get_success_url(self):
        return reverse('post-list')

# PasswordChangeView 오버라이드
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('post-list')


class ProfileView(DetailView):
    model = User
    template_name = 'user/profile.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['user_posts'] = Post.objects.filter(author__slug=slug)[:5]
        context['user_comments'] = Comment.objects.filter(author__slug=slug)[:5]
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'user/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 20
    page_kwarg = 'page'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Post.objects.filter(author__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, slug=self.kwargs.get('slug'))
        return context

class UserCommentList(ListView):
    model = Comment
    template_name = 'user/user_comment_list.html'
    context_object_name = 'user_comments'
    paginate_by = 20
    page_kwarg = 'page'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Comment.objects.filter(author__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, slug=self.kwargs.get('slug'))
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user/profile_set_form.html'

    # id를 따로 받지 않았으니 id를 전달할 수 있게 오버라이드 한다
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'slug':self.object.slug})

class CommentCreateView(LoginAndVerificationRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id': self.kwargs.get('post_id')})

class CommentUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_update_form.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id': self.object.post.id})

class CommentDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete_form.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id': self.object.post.id})

