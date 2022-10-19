from django.views.generic import (
    ListView, 
    DetailView,
    CreateView
)
from django.urls import reverse
from .models import Post
from .forms import PostForm


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

class PostWriteView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'page_id':self.object.id})

