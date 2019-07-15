from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'author')


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Comment', required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'content',
        'rows': '4',
    }))
    image = forms.ImageField(required=False)

    class Meta:
        model = Comment
        fields = ('content', 'image')
