from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from allauth.account.views import PasswordChangeView
from braces.views import LoginRequiredMixin
from .models import Post, User, Comment, Like
from .forms import PostForm, ProfileForm, CommentForm
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
        context['post_content_type_id'] = ContentType.objects.get(model='post').id
        context['comment_content_type_id'] = ContentType.objects.get(model='comment').id
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

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

class PostDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'post'

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

class ProcessLikeView(LoginAndVerificationRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # get_or_create는 아래 조건에 해당하는게 있으면 가져오고 가져온걸 like에 저장하고 created=False가 된다
        # 아래 조건에 해당하는게 없으면 오브젝트를 생성하고 like에 저장하고 created=True가 된다
        like, created = Like.objects.get_or_create(
            user = self.request.user,
            content_type_id = self.kwargs.get('content_type_id'),
            object_id = self.kwargs.get('object_id')
        )
        if not created:
            like.delete()
        # 좋아요는 여러곳에서 쓰일 수 있으니 self.request.META['HTTP_REFERER']는 항상 이 뷰로 요청을 보낸 페이지의 주소를 가지고 있다
        return redirect(self.request.META['HTTP_REFERER'])


class SearchView(ListView):
    model = Post
    context_object_name = 'search_results'
    template_name = 'board/search_results.html'
    paginate_by = 20

    def get_queryset(self):
        # search url로 직접 접근하면 null이 전달되어 에러가 날 수 있으므로 검색어가 전달되지 않았을 땐 ''전달
        query = self.request.GET.get('query', '')
        return Post.objects.filter(
            Q(title__contains=query)
            | Q(content__contains=query)
        )

    # 검색어를 템플릿으로 전달해 뭘 검색했는지 보여줄 것
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
