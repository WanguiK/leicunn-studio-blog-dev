from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.models import Tag

from blog.forms import *
from blog.models import *


@login_required
def dashboard(request):
    context = {
        'pagename': "Dashboard"
    }
    return render(request, 'dashboard/dashboard.html', context)


class UpdateAuthor(UpdateView):
    model = get_user_model()
    form_class = AuthorChangeForm
    login_required = True
    template_name = 'dashboard/updateprofile.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateAuthor, self).get_context_data(**kwargs)
        context['author'] = self.model.objects.get(username=self.request.user)
        context['pagename'] = 'User Profile'
        return context


# class CategoryCreate(PermissionRequiredMixin, CreateView):
class CategoryCreate(CreateView):
    form_class = CategoryForm
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreate, self).get_context_data(**kwargs)
        context['pagename'] = 'Categories | Subjects'
        table = Category.objects.all()
        context['categoriesTable'] = table
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('category')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)


# class PostCreate(PermissionRequiredMixin, CreateView):
class PostCreate(CreateView):
    model = Post
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/newpost.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        context['pagename'] = 'New Post'
        return context

    def form_valid(self, form):
        newpost = form.save(commit=False)
        form.instance.author = self.request.user

        if form.instance.slug == None or form.instance.slug == '':
            form.instance.slug = slugify(form.instance.title)
        else:
            form.instance.slug = form.instance.slug

        newpost.save()
        form.save_m2m()
        return super(PostCreate, self).form_valid(form)


# @login_required
# def PostCreate(request):
#     posts = Post.objects.order_by('-updated')
    
#     form = PostForm(request.POST)

#     if form.is_valid():
#         newpost = form.save(commit=False)
#         newpost.slug = slugify(newpost.title)
#         newpost.save()
#         form.save_m2m()

#     context = {
#         'posts' : posts,
#         'form' : form,
#     }
#     return render(request, 'dashboard/newpost.html', context)


@login_required
def view_posts(request):
    posts = Post.objects.order_by('-updated')
    tags = Tag.objects.all()
    context = {
        'posts' : posts,
        'pagename' : "All Posts",
        'tags' : tags,
    }
    return render(request, 'dashboard/posts.html', context)