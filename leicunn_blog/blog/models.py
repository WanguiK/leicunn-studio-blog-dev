from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager




class Author(AbstractUser):
    username = models.CharField("Username", max_length=50, unique=True, db_index=True, primary_key=True)

    position = models.CharField("Position", max_length=100, null=True)

    location = models.CharField("Location", max_length=50, null=True)

    image = models.ImageField("Profile Picture", upload_to='profile/', blank=True, null=False)

    website = models.URLField(default="https://www.leicunnstudio.com", blank=False, max_length=100)

    twitter = models.URLField("Twitter", default="https://www.twitter.com", blank=False, max_length=100)

    instagram = models.URLField("Instagram", default="https://www.instagram.com", blank=False, max_length=100)

    linkedin = models.URLField("Linkedin", default="https://www.linkedin.com", blank=False, max_length=100)

    description = models.CharField("About Me", max_length=280, default="Write A Personal Statement", help_text="* Required: 280 Characters", blank=False)

    article = models.TextField('Write An Article About Yourself', blank=False, help_text='* Required', default="I am a writer at Leicunn Studio Blog.")

    def get_absolute_url(self):
        return reverse('updateauthor', args=[self.pk])

    def __str__(self):
        return self.username


class Category(models.Model):
    category = models.CharField(
        max_length=100, help_text='Less than 100 characters')

    description = models.TextField("Description", max_length=280, help_text="* required. Describe the content of the content in this category", blank=False)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('category')

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.category)
        else:
            self.slug = self.slug
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    title = models.CharField('The Title',max_length=120, help_text='* Required. Maximum 120 Characters', blank=False)

    summary = models.CharField(max_length=280, help_text="* Required. Write a tweet sized TL;DR summary", blank=False)

    article = models.TextField('Write The Article', blank=False, help_text='* Required')

    tags = TaggableManager(help_text="A comma-separated list of tags for the post")

    POST_STATUS = (
        ('Draft', 'Draft'),
        ('In Review', 'In Review'),
        ('Published', 'Published'),
        ('Rejected', 'Rejected'),
        ('Archived', 'Archived')
    )
    status = models.CharField(
        max_length=9,
        choices=POST_STATUS,
        blank=False,
        default='d',
        help_text='* Required'
    )

    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, blank=False)

    cover = models.ImageField('Cover Image', upload_to='cover/', help_text="Select a cover image preferably 1280 by 720 pixels", null=False)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['updated']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('posts')

    # def save(self, *args, **kwargs):
    #     if self.slug == None or self.slug == '':
    #         self.slug = slugify(self.title)
    #     else:
    #         self.slug = self.slug
    #     super(Post, self).save(*args, **kwargs)