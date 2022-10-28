from email.policy import default
from enum import unique
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
from .validators import validate_length, validate_no_special_charactors

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={"unique": '해당 닉네임은 이미 사용중입니다!'},
        validators = [validate_no_special_charactors],
    )

    slug = models.SlugField(
        unique=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.nickname == None:
            self.nickname = uuid.uuid1()
        self.slug = slugify(self.nickname, allow_unicode=True)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.nickname)


class Post(models.Model):
    title = models.CharField(max_length=100, validators=[validate_length])
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-dt_created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    dt_created = models.DateField(auto_now_add=True)
    dt_updated = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-dt_created']

    def __str__(self):
        return self.content


class Like(models.Model):
    dt_created = models.DateField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey()

    def __str__(self):
        return f"({self.user}, {self.liked_object})"
