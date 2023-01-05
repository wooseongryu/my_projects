from .models import Post

def validate_post():
    posts = Post.objects.all()
    for post in posts:
        if len(post.title) < 5:
            print(post.id,'번 글의 제목이 5자 미만입니다.')
            post.title += '12345'
            post.save()
