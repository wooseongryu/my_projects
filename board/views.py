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
from .models import Post
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
