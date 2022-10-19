from django.urls import path
from . import views

urlpatterns = [
    path(
        'list/',
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
    # path(
    #     'post/<int:page_id>/delete/',
    #     views.post_delete.as_view(),
    #     name='post-delete'
    # ),
]
