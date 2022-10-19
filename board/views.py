from django.views.generic import ListView, DetailView
from .models import Post


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

