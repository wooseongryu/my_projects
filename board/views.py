from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
