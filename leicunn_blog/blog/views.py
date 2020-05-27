from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, CreateView, FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.models import Tag
from django.conf import settings
import random
import json
from django.db.models import Q
from django.views import generic
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
        #this is what related_name is for
        media = Media.objects.filter(type="Profile", post=None, profilepic=None)
        context['media'] = media
        return context


# class CategoryCreate(PermissionRequiredMixin, CreateView):
class CategoryCreate(CreateView):
    form_class = CategoryForm
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreate, self).get_context_data(**kwargs)
        # context['count'] = Category.objects.annotate(number_of_posts=Count('post'))
        context['pagename'] = 'Categories | Subjects'
        context['jumbo'] = 'Add New Category'
        context['jumbomessage'] = 'This is where you view and add pages (categories) to the blog. Categories also appear on the menu (navigation)'
        table = Category.objects.annotate(number_of_posts=Count('post'))
        # table = Category.objects.all()
        context['categories'] = table
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('category')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)


@login_required
def delete_category(request, pk):
    cat = Category.objects.get(pk=pk)
    if request.method == 'POST':
        cat.delete()
        catObjs = Category.objects.all().values('category', 'description', 'slug', 'author')
        categories = list(catObjs) 
        return JsonResponse(categories, safe=False)
    else:
        return render(request, 'dashboard/category.html', {'categories':Category.objects.all()})


# # class EditPost(PermissionRequiredMixin, UpdateView):
class EditCategory(UpdateView):
    model = Category
    login_required = True
    # permission_required = 'blog.can_add_post' and 'blog.can_change_post'
    template_name = 'dashboard/category.html'
    fields = ['category', 'description', 'slug']

    def get_context_data(self, **kwargs):
        context = super(EditCategory, self).get_context_data(**kwargs)
        context['pagename'] = 'Edit Category'
        context['jumbo'] = 'Edit Category'
        context['jumbomessage'] = 'Edit the selected category.'
        table = Category.objects.all()
        context['categories'] = table
        return context


def get_media():
    unusedMedia = Media.objects.filter(post=None).filter(profilepic=None)
    usedMedia = Media.objects.exclude(post=None, profilepic=None)
    context = {
        'unusedmedia': unusedMedia,
        'usedmedia': usedMedia
    }
    return context


class MediaUpload(CreateView):
    form_class = MediaForm
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaUpload, self).get_context_data(**kwargs)
        context['jumbo'] = 'Manage Media'
        context['pagename'] = 'Media'
        context['card'] = 'Upload New Media'
        context['jumbomessage'] = 'Select new media to upload for use in blog posts or as a profile picture and manage existing media.'
        context.update(get_media())
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('media')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MediaUpload, self).form_valid(form)


class EditMedia(UpdateView):
    model = Media
    login_required = True
    # permission_required = 'blog.can_add_post' and 'blog.can_change_post'
    template_name = 'dashboard/media.html'
    fields = ['description', 'slug', 'type', 'image']

    def get_context_data(self, **kwargs):
        context = super(EditMedia, self).get_context_data(**kwargs)

        context['jumbo'] = 'Manage Media'
        context['pagename'] = 'Edit Media'
        context['card'] = 'Edit Existing Media'
        context['jumbomessage'] = 'Edit aspects of existing media.'
        context.update(get_media())
        return context


@login_required
def delete_media(request, pk):
    media = Media.objects.get(pk=pk)
    unMedia = Media.objects.filter(post=None).filter(profilepic=None).values('description', 'image')
    uMedia = Media.objects.exclude(post=None).exclude(profilepic=None).values('description', 'image')
    if request.method == 'POST':
        media.delete()
        unusedmedia = list(unMedia)
        usedmedia = list(uMedia)
        data = json.dumps({
            'unusedmedia': unusedmedia,
            'usedmedia': usedmedia,
        })
        return JsonResponse(data, safe=False)
    else:
        context = get_media()
        return render(request, 'dashboard/media.html', context)


def get_available_covers():
    context = {
        'media': Media.objects.filter(type="Cover", post=None)
    }
    return context


# class PostCreate(PermissionRequiredMixin, CreateView):
class PostCreate(CreateView):
    model = Post
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/newpost.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        context['pagename'] = 'New Blog Post'
        context['jumbo'] = 'Add New Post'
        context['jumbomessage'] = 'Create a new blog post and share to social media.'
        context.update(get_available_covers())
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


@login_required
def view_posts(request):
    posts = Post.objects.order_by('-updated')
    context = {
        'posts' : posts,
        'pagename' : "All Posts"
    }
    return render(request, 'dashboard/posts.html', context)


@login_required
def delete_posts(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        postObjs = Post.objects.order_by('-updated').values('id', 'author', 'title', 'category', 'tags', 'updated', 'slug')
        posts = list(postObjs) 
        return JsonResponse(posts, safe=False)
    else:
        return render(request, 'dashboard/posts.html', {'posts':Post.objects.order_by('-updated')})


# class EditPost(PermissionRequiredMixin, UpdateView):
class EditPost(UpdateView):
    model = Post
    login_required = True
    # permission_required = 'blog.can_add_post' and 'blog.can_change_post'
    template_name = 'dashboard/newpost.html'
    form_class = EditForm

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['pagename'] = 'Edit Blog Post'
        context['jumbo'] = 'Edit Blog Post'
        context['jumbomessage'] = 'Edit the selected blog post.'
        id = self.object.pk
        cover = Post.objects.values_list('cover', flat=True).get(pk=id)
        image = Media.objects.values_list('image', flat=True).get(pk=cover)
        image = "{0}{1}".format(settings.MEDIA_URL, image)
        context['image'] = image
        context.update(get_available_covers())
        return context


# class QuoteCreate(PermissionRequiredMixin, CreateView):
class QuoteCreate(CreateView):
    model = Quote
    form_class = QuoteForm
    login_required = True
    # permission_required = 'blog.can_add_post'
    template_name = 'dashboard/quotes.html'

    def get_context_data(self, **kwargs):
        context = super(QuoteCreate, self).get_context_data(**kwargs)
        context['pagename'] = 'Quotes'
        context['jumbo'] = 'Add New Quote'
        context['jumbomessage'] = 'This is where you view and add quotes to the blog. The most recent quote will be displayed as quote of the week.'
        table = Quote.objects.all()
        context['quote'] = table
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('quote')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuoteCreate, self).form_valid(form)


# class EditQuote(PermissionRequiredMixin, UpdateView):
class EditQuote(UpdateView):
    model = Quote
    login_required = True
    # permission_required = 'blog.can_add_post' and 'blog.can_change_post'
    template_name = 'dashboard/quotes.html'
    form_class = QuoteForm

    def get_context_data(self, **kwargs):
        context = super(EditQuote, self).get_context_data(**kwargs)
        context['pagename'] = 'Edit Quote'
        context['jumbo'] = 'Edit Quote'
        context['jumbomessage'] = 'Edit the selected quote.'
        table = Quote.objects.all()
        context['quote'] = table
        return context


@login_required
def delete_quote(request, pk):
    q = Quote.objects.get(pk=pk)
    if request.method == 'POST':
        q.delete()
        qObjs = Quote.objects.all().values('quote', 'owner', 'created', 'author')
        quote = list(qObjs) 
        return JsonResponse(quote, safe=False)
    else:
        return render(request, 'dashboard/quotes.html', {'quote':Quote.objects.all()})


def load_menu():
    cat_count = Category.objects.all().count()
    half = None

    if cat_count % 2 == 0:
        half = cat_count / 2
        left = Category.objects.all()[:half]
        right = Category.objects.all()[half:cat_count]
    else:
        half = cat_count / 2 + 1
        left = Category.objects.all()[:half]
        right = Category.objects.all()[half:cat_count]

    context = {
        'left_menu': left,
        'right_menu': right
    }
    return context


def load_bookmarks():
    categories = Category.objects.all()
    tags = Post.tags.most_common()[:13]

    context = {
        'common_tags': tags,
        'categories': categories
    }
    return context


def get_prev_next(pk):
    query = Post.objects.filter(status__exact='Published')
    p = query.get(pk=pk)
    f = query.first()
    l = query.last()
    nextt = None
    previous = None
    context = None

    try:
        if p == f:
            nextt = p.get_previous_by_updated()
            previous = nextt.get_previous_by_updated()
        elif p == l:
            previous = p.get_next_by_updated()
            nextt = previous.get_next_by_updated()
        else:
            nextt = p.get_next_by_updated()
            previous = p.get_previous_by_updated()
    except Exception:
        pass

    context = {
        'next': nextt,
        'previous': previous
    }

    return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    context_object_name = 'post'
    template_name = 'blog/read.html'

    def get_success_url(self):
        return reverse('read', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        pk = self.object.pk
        # context['comments'] = Comment.objects.filter(status__exact="Show", post=pk)
        context['comments'] = Comment.objects.filter(post=pk)
        # context['query'] = Comment.objects.filter(status="Show", replies=None, post=pk).values('pk')
        context['query'] = Comment.objects.filter(post=pk).values('pk')
        context.update(load_menu())
        context.update(load_bookmarks())
        context.update(get_prev_next(pk))
        context['form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        postInstance = Post.objects.get(slug = self.kwargs['slug'])
        num = random.randint(1, 10)
        image = "/media/profiles/p"+str(num)+".png"
        form.instance.image = image
        form.instance.post = postInstance
        form.save()
        return super(PostDetailView, self).form_valid(form)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tagArticles = Post.objects.filter(tags=tag, status__exact = 'Published')
    page = request.GET.get('page', 1)
    paginator = Paginator(tagArticles, 3)

    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    context = {
        'tag': tag,
        'posts': numbers
    }
    context.update(load_menu())
    context.update(load_bookmarks())
    return render(request, 'blog/tag.html', context)


class CategoryArticleView(generic.ListView):
    template_name = 'blog/bookmark.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(category__slug = self.kwargs['slug'], status__exact = 'Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug = self.kwargs['slug'])
        context.update(load_menu())
        context.update(load_bookmarks())
        return context


def index(request):
    published = Post.objects.filter(status__exact = 'Published')[:15]
    more = Post.objects.filter(status__exact = 'Published')[15:]
    page = request.GET.get('page', 1)
    paginator = Paginator(more, 3)

    today =  datetime.now()
    yestarday = datetime.now() - timedelta(days=1)

    quote = Quote.objects.first()

    try:
        morePosts = paginator.page(page)
    except PageNotAnInteger:
        morePosts = paginator.page(1)
    except EmptyPage:
        morePosts = paginator.page(paginator.num_pages)

    context = {
        'posts' : published,
        'more' : morePosts,
        'today' : today,
        'yestarday' : yestarday,
        'quote' : quote
    }
    context.update(load_bookmarks())
    return render(request, 'blog/index.html', context)


class SearchResultsView(generic.ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        return Post.objects.filter(Q(article__icontains=query) | Q(summary__icontains=query) | Q(title__icontains=query), status__exact = 'Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        context.update(load_menu())
        context.update(load_bookmarks())
        return context


class CommentManage(FormMixin, generic.ListView):
    model = Comment
    form_class = CommentForm
    context_object_name = 'comments'
    template_name = 'dashboard/comment.html'

    def get_success_url(self):
        return reverse('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Comments'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(CommentManage, self).form_valid(form)


# class EditQuote(PermissionRequiredMixin, UpdateView):
# class EditComment(UpdateView):
#     model = Comment
#     login_required = True
#     # permission_required = 'blog.can_add_post' and 'blog.can_change_post'
#     template_name = 'dashboard/comment.html'
#     form_class = CommentForm

#     def get_context_data(self, **kwargs):
#         context = super(EditComment, self).get_context_data(**kwargs)
#         context['pagename'] = 'Edit Quote'
#         context['jumbo'] = 'Edit Quote'
#         context['jumbomessage'] = 'Edit the selected quote.'
#         table = Quote.objects.all()
#         context['quote'] = table
#         return context


@login_required
def edit_comment(request, pk):
    c = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=c)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return reverse('comments')
        cObjs = Comment.objects.all().values()
        comments = list(cObjs)
        return JsonResponse(comments, safe=False)
    else:
        return render(request, 'dashboard/comment.html', {'comments':Comment.objects.all()})


# def book_update(request, pk, template_name='books/book_form.html'):
#     book= get_object_or_404(Book, pk=pk)
#     form = BookForm(request.POST or None, instance=book)
#     if form.is_valid():
#         form.save()
#         return redirect('book_list')
#     return render(request, template_name, {'form':form})


@login_required
def delete_comment(request, pk):
    c = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        c.delete()
        cObjs = Comment.objects.all().values()
        comments = list(cObjs)
        return JsonResponse(comments, safe=False)
    else:
        return render(request, 'dashboard/comment.html', {'comments':Comment.objects.all()})