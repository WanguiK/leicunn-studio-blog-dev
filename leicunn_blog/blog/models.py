from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
import os


class Author(AbstractUser):
    username = models.CharField("Username", max_length=50, unique=True, db_index=True, primary_key=True)

    position = models.CharField("Position", max_length=100, null=True)

    location = models.CharField("Location", max_length=50, null=True)

    image = models.ForeignKey('Media', on_delete=models.PROTECT, related_name="profilepic", blank=False, null=True)

    cover = models.ForeignKey('Media', on_delete=models.PROTECT, related_name="authorcover", blank=False, null=True)

    website = models.URLField(default="https://www.leicunnstudio.com", blank=False, max_length=100)

    twitter = models.URLField("Twitter", default="https://www.twitter.com", blank=False, max_length=100)

    instagram = models.URLField("Instagram", default="https://www.instagram.com", blank=False, max_length=100)

    linkedin = models.URLField("Linkedin", default="https://www.linkedin.com", blank=False, max_length=100)

    description = models.CharField("About Me", max_length=280, default="Write A Personal Statement", help_text="* Required: 280 Characters", blank=False)

    article = models.TextField('Write An Article About Yourself', blank=False, help_text='* Required', default="I am a writer at Leicunn Studio Blog.")

    tags = models.TextField(blank=False, help_text="A comma-separated or space-separated list of tags for the post", default='author')

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.get_full_name()
        if self.slug == None or self.slug == '':
            self.slug = slugify(name)
        else:
            self.slug = self.slug
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('updateauthor', args=[self.pk])

    def __str__(self):
        return self.username


class Category(models.Model):
    category = models.CharField(max_length=100, help_text='Less than 100 characters')

    description = models.TextField("Description", max_length=280, help_text="* required. Describe the content of the content in this category", blank=False)

    author = models.ForeignKey(
        get_user_model(),
        default="Anonymous",
        on_delete=models.SET_DEFAULT
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


class Media(models.Model):
    description = models.CharField('Media Description', max_length=120, help_text='* Required. Maximum 120 Characters', blank=False)

    slug = models.SlugField(unique=True)

    MEDIA_TYPE = (
        ('Profile', 'Profile'),
        ('Cover', 'Cover'),
        ('Author Cover', 'Author Cover')
    )
    type = models.CharField(
        'Media Type',
        max_length=12,
        choices=MEDIA_TYPE,
        blank=False,
        default='Cover',
        help_text='* Required'
    )

    image = models.ImageField('Image', upload_to='images/', blank=True, null=False)

    created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        get_user_model(),
        default="Anonymous",
        on_delete=models.SET_DEFAULT
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.pk}'

    def get_absolute_url(self):
        return reverse_lazy('media')

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage = self.image.storage
        path = self.image.path
        # Delete the model before the file
        super(Media, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


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
        default='Draft',
        help_text='* Required'
    )

    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, blank=False, default='1')

    cover = models.ForeignKey('Media', on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        get_user_model(),
        default="Anonymous",
        on_delete=models.SET_DEFAULT
    )

    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('posts')


class Quote(models.Model):
    quote = models.CharField(max_length=180, help_text="* Required", blank=False)

    owner = models.CharField('Said By', max_length=100, help_text="* Required", blank=True, null=False)

    created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        get_user_model(),
        default="Anonymous",
        on_delete=models.SET_DEFAULT
    )

    def save(self, *args, **kwargs):
        if self.owner == None or self.owner == '':
            self.owner = "Anonymous"
        else:
            self.owner = self.owner
        super(Quote, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        return reverse('quote')


class Comment(models.Model):
    content = models.TextField('Comment', blank=False, help_text='Comment * Required', max_length=500)

    name = models.CharField('Name', max_length=60, blank=False, help_text='Name * Required')

    email = models.EmailField('E-mail Address', max_length=100, blank=False, help_text="E-mail Address * Required")

    image = models.CharField("Image", max_length=23, blank=True)

    website = models.URLField("Website", help_text='Website (Optional)', blank=True, max_length=100)

    COMMENT_STATUS = (
        ('Show', 'Show'),
        ('Hide', 'Hide')
    )
    status = models.CharField(
        max_length=4,
        choices=COMMENT_STATUS,
        blank=True,
        default='Hide'
    )

    created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=False, related_name='comments')

    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='replies')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('comments')


class Opinions(models.Model):
    content = models.TextField('Comment', blank=False, help_text='Comment * Required', max_length=500)

    name = models.CharField('Name', max_length=60, blank=False, help_text='Name * Required')

    email = models.EmailField('E-mail Address', max_length=100, blank=False, help_text="E-mail Address * Required")

    image = models.CharField("Image", max_length=23, blank=True)

    website = models.URLField("Website", help_text='Website (Optional)', blank=True, max_length=100)

    COMMENT_STATUS = (
        ('Show', 'Show'),
        ('Hide', 'Hide')
    )
    status = models.CharField(
        max_length=4,
        choices=COMMENT_STATUS,
        blank=True,
        default='Hide'
    )

    created = models.DateTimeField(auto_now_add=True)

    AUTHOR_STATUS = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    is_author = models.CharField(
        max_length=3,
        choices=AUTHOR_STATUS,
        default='No',
        blank=True
    )

    post = models.ForeignKey('Author', on_delete=models.CASCADE, blank=False, related_name='comments')

    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='replies')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('opinions')