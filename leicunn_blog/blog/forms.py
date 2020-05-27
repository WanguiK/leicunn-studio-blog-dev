from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from blog.models import *


class AuthorCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Author
        fields = ('username', 'email', 'position', 'location', 'image', 'website', 'twitter', 'instagram', 'linkedin', 'description',)


class AuthorChangeForm(UserChangeForm):

    first_name = forms.CharField(max_length=20, help_text="Jane")

    last_name = forms.CharField(max_length=20, help_text="Doe")

    email = forms.EmailField(max_length=100, help_text="janedoe@example.com")

    position = forms.CharField(max_length=50, help_text="i.e. Editor")

    location = forms.CharField(max_length=50, help_text="City, Country")

    image = forms.ModelChoiceField(queryset=Media.objects.order_by('-created').filter(post=None, type="Profile"), empty_label=None)

    website = forms.URLField(max_length=100, help_text="http://www.example.com")

    twitter = forms.URLField(max_length=100, help_text="https://www.twitter.com")

    instagram = forms.URLField(max_length=100, help_text="https://www.instagram.com")

    linkedin = forms.URLField(max_length=100, help_text="https://www.linkedin.com")

    description = forms.CharField(max_length=280, help_text="A tweet-sized summary about you ...")
    
    article = forms.CharField(help_text="An article about you, your skillset and achievement etc.")

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'email', 'position', 'location', 'image', 'website', 'twitter', 'instagram', 'linkedin', 'description', 'article')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'description', 'slug']


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
        # fields = ['content', 'name', 'email', 'website', 'parent']

    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     self.fields['parent'].queryset = Comment.objects.filter(status="Show", replies=None)
