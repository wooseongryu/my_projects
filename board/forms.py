from django import forms
from .models import Post, User, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]

    def signup(self, request, user):
        user.nickname = self.cleaned_data["nickname"]
        user.save()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea,
        }
    
