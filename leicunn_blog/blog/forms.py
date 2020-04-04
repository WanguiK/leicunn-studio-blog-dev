from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from blog.models import Author, Category


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

    image = forms.FileField()

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