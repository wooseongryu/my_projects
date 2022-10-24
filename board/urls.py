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
    # profile
    path(
        'users/<int:user_id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'users/<int:user_id>/posts/',
        views.UserPostListView.as_view(),
        name='user-post-list'
    ),
]
