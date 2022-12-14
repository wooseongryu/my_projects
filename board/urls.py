from django.urls import path
from . import views

urlpatterns = [
    # posts
    path(
        '',
        views.PostListView.as_view(),
        name='post-list'
    ),
    path(
        'write/',
        views.PostWriteView.as_view(),
        name='post-write'
    ),
    path(
        'post/<int:page_id>/',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    path(
        'post/<int:page_id>/edit/',
        views.PostUpdateView.as_view(),
        name='post-update'
    ),
    path(
        'post/<int:page_id>/delete/',
        views.PostDeleteView.as_view(),
        name='post-delete'
    ),
    path(
        'search/',
        views.SearchView.as_view(),
        name='search'
    ),
    # comment
    path(
        'post/<int:post_id>/comments/create/',
        views.CommentCreateView.as_view(),
        name='comment-create'
    ),
    path(
        'comments/<int:comment_id>/comments/update/',
        views.CommentUpdateView.as_view(),
        name='comment-update'
    ),
    path(
        'comments/<int:comment_id>/comments/delete/',
        views.CommentDeleteView.as_view(),
        name='comment-delete'
    ),
    # profile
    path(
        'users/<slug>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'users/<slug>/posts/',
        views.UserPostListView.as_view(),
        name='user-post-list'
    ),
    path(
        # 프로필 설정은 현재 로그인된 유저로만
        # 접근하니 id를 따로 받지 않음
        'update-profile/',
        views.ProfileUpdateView.as_view(),
        name='profile-update'
    ),
    path(
        'users/<slug>/comments/',
        views.UserCommentList.as_view(),
        name='user-comment-list'
    ),
    # like
    path(
        'like/<int:content_type_id>/<int:object_id>/',
        views.ProcessLikeView.as_view(),
        name='process-like'
    ),
]
