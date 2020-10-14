from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from blog.models import *


class AuthorCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=20, help_text="Jane")

    last_name = forms.CharField(max_length=20, help_text="Doe")

    email = forms.EmailField(max_length=100, help_text="janedoe@example.com")

    position = forms.CharField(max_length=50, help_text="i.e. Editor")

    location = forms.CharField(max_length=50, help_text="City, Country")

    image = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(type="Profile", profilepic=None), empty_label=None)

    cover = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(type="Author Cover", authorcover=None), empty_label=None)

    website = forms.URLField(max_length=100, help_text="http://www.example.com")

    class Meta(UserCreationForm):
        model = Author
        fields = ('first_name', 'last_name', 'email', 'position', 'location', 'image', 'website', 'cover', 'password1', 'password2')


class AuthorChangeForm(UserChangeForm):

    first_name = forms.CharField(max_length=20, help_text="Jane")

    last_name = forms.CharField(max_length=20, help_text="Doe")

    email = forms.EmailField(max_length=100, help_text="janedoe@example.com")

    position = forms.CharField(max_length=50, help_text="i.e. Editor")

    location = forms.CharField(max_length=50, help_text="City, Country")

    image = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(type="Profile", profilepic=None), empty_label=None)

    cover = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(type="Author Cover", authorcover=None), empty_label=None)

    website = forms.URLField(max_length=100, help_text="http://www.example.com")

    twitter = forms.URLField(max_length=100, help_text="https://www.twitter.com")

    instagram = forms.URLField(max_length=100, help_text="https://www.instagram.com")

    linkedin = forms.URLField(max_length=100, help_text="https://www.linkedin.com")

    description = forms.CharField(max_length=280, help_text="A tweet-sized summary about you ...")

    article = forms.CharField(help_text="An article about you, your skillset and achievement etc.")

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'email', 'position', 'location', 'image', 'website', 'twitter', 'instagram', 'linkedin', 'description', 'article', 'cover', 'tags')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'description', 'slug', 'show']


class MediaForm(ModelForm):

    image = forms.FileField()
    class Meta:
        model = Media
        fields = ['description', 'slug', 'type', 'image']


class PostForm(ModelForm):
    status = forms.ChoiceField(choices=Post.POST_STATUS, widget=forms.RadioSelect())

    cover = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(post=None, type="Cover"), empty_label=None)

    slug = forms.CharField(max_length=100, help_text="A 50 character unique link to the blog post")

    class Meta:
        model = Post
        fields = ['title', 'summary', 'article', 'tags', 'status', 'category', 'cover', 'slug']

    def clean_title(self):
        return self.cleaned_data['title'].title()


class EditForm(ModelForm):
    status = forms.ChoiceField(choices=Post.POST_STATUS, widget=forms.RadioSelect())

    cover = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(type="Cover"), empty_label=None)

    slug = forms.CharField(max_length=100, help_text="A 50 character unique link to the blog post")

    class Meta:
        model = Post
        fields = ['title', 'summary', 'article', 'tags', 'status', 'category', 'cover', 'slug']

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'owner']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'

    def clean_content(self):
        return self.cleaned_data['content']


class OpinionForm(ModelForm):

    class Meta:
        model = Opinion
        fields = '__all__'

    def clean_content(self):
        return self.cleaned_data['content']