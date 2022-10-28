from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline  
from .models import Post, User, Comment, Like


class CommentInline(admin.StackedInline):
    model = Comment


"""
Like모델은 GenericForeignKey를 사용했으니
GenericStackedInline를 사용해야 에러가 나지 않는다
"""
class LikeInline(GenericStackedInline):
    model = Like

# UserAdmin의 필드셋을 수정
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname",)}),)


class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
        LikeInline,
    )

class CommentAdmin(admin.ModelAdmin):
    inlines = (
        LikeInline,
    )

# 기본으로 제공하는 UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
# 따로 작성하지 않으면 기본으로 ModelAdmin이 사용된다
admin.site.register(Like)
