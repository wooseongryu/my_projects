from django.urls import path
from . import views

urlpatterns = [
    path(
        'list/',
        views.post_list,
        name='post-list'
    ),
    # path(
    #     'write/',
    #     views.post_write.as_view(),
    #     name='post-write'
    # ),
    # path(
    #     'post/<int:page_id>/',
    #     views.post_detail.as_view(),
    #     name='post-detail'
    # ),
    # path(
    #     'post/<int:page_id>/edit/',
    #     views.post_update.as_view(),
    #     name='post-update'
    # ),
    # path(
    #     'post/<int:page_id>/delete/',
    #     views.post_delete.as_view(),
    #     name='post-delete'
    # ),
]
