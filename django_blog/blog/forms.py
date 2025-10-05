from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag
from taggit.forms import TagWidget


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Comma-separated tags', widget=TagWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing = ', '.join(t.name for t in self.instance.tags.all())
            self.fields['tags'].initial = existing

    def save_tags(self, post: Post):
        tags_str = self.cleaned_data.get('tags', '')
        names = [t.strip() for t in tags_str.split(',') if t.strip()]
        tag_objs = []
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)
        post.tags.set(tag_objs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    # No tag save here; comments do not manage tags


