from django.shortcuts import render
from .models import Post

def post_list(request):
    object_list = Post.objects.all()
    return render(request, 'board/post_list.html', {'object_list': object_list})
