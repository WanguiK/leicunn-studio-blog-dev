from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request, HttpRequest
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, CreateView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template import Context
# from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.models import Tag
from django.conf import settings
import random
import json
from django.views import View
from django.db.models import Q
from django.views import generic
from blog.forms import *
from blog.models import *


class UpdateAuthor(UpdateView):
    model = get_user_model()
    form_class = AuthorChangeForm
    login_required = True
    template_name = 'dashboard/updateprofile.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateAuthor, self).get_context_data(**kwargs)
        context['author'] = self.model.objects.get(username=self.request.user)
        context['pagename'] = 'User Profile'
        # Count the comments and opinions from user
        comments = Comment.objects.filter(author=self.request.user).count()
        opinions = Opinion.objects.filter(is_author='Yes').count()
        numComments = comments + opinions
        # Count posts from the user
        numPosts = Post.objects.filter(author=self.request.user).count()
        context['comments'] = numComments
        context['posts'] = numPosts
        context['opinionform'] = OpinionForm()
        context.update(get_author_media())
        return context


@login_required #Author create own opinion
def author_add_opinion(request):
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            current = request.user
            image = str(current.image.image.url)

            opinion.name = str(current.get_full_name())
            opinion.email = str(current.email)
            opinion.image = image
            opinion.website = str(current.website)
            opinion.is_author = 'Yes'
            opinion.post = current
            opinion.save()
            title = str(current.first_name) + " added an opinion"
            notif = {
                'identity': opinion.pk,
                'title': title,
                'message': opinion.content,
                'notif_type': 'Opinion',
                'link': '/opinions/#comment'+str(opinion.pk),
                'author': current
            }
            create_notification(1, **notif)
            return redirect('opinions')
    else:
        form = OpinionForm()
    return redirect('opinions')


def get_author_media():
    profilemedia = Media.objects.filter(type="Profile", profilepic=None)
    covermedia = Media.objects.filter(type="Author Cover", authorcover=None)
    context = {
        'profilemedia': profilemedia,
        'covermedia': covermedia
    }
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
    fields = ['category', 'description', 'slug', 'show']

    def get_context_data(self, **kwargs):
        context = super(EditCategory, self).get_context_data(**kwargs)
        context['pagename'] = 'Edit Category'
        context['jumbo'] = 'Edit Category'
        context['jumbomessage'] = 'Edit the selected category.'
        table = Category.objects.all()
        context['categories'] = table
        return context


def get_media():
    unusedMedia = Media.objects.filter(post=None).filter(profilepic=None).filter(authorcover=None)
    usedMedia = Media.objects.exclude(post=None, profilepic=None, authorcover=None)
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
    unMedia = Media.objects.filter(post=None).filter(profilepic=None).filter(authorcover=None).values('description', 'image')
    uMedia = Media.objects.exclude(post=None).exclude(profilepic=None).exclude(authorcover=None).values('description', 'image')
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
        title = str(newpost.author.first_name) + " published a post"
        notif = {
            'identity': newpost.pk,
            'title': title,
            'message': newpost.title,
            'notif_type': 'Post',
            'link': '/allposts/#post'+str(newpost.pk),
            'author': newpost.author
        }
        create_notification(1, **notif)
        return super(PostCreate, self).form_valid(form)


@login_required
def view_posts(request):
    posts = Post.objects.order_by('-updated').prefetch_related('comments')
    form = CommentForm()
    context = {
        'posts' : posts,
        'pagename' : "All Posts",
        'form': form
    }
    print("\n\n"+str(posts)+"\n\n")
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


@login_required
def get_post(request, pk):
    p = Post.objects.filter(pk=pk).values('title', 'summary')
    context = {}
    if request.method == 'GET':
        post = list(p)
        context = {
            'data': post
        }
    return JsonResponse(context)


@login_required #Author create comment
def author_add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            current = request.user
            image = str(current.image.image.url)
            post = Post.objects.get(pk=pk)

            comment.name = str(current.get_full_name())
            comment.email = str(current.email)
            comment.image = image
            comment.website = str(current.website)
            comment.author = current
            comment.post = post
            comment.save()
            title = str(current.first_name) + " added a comment"
            notif = {
                'identity': comment.pk,
                'title': title,
                'message': comment.content,
                'notif_type': 'Comment',
                'link': '/comments/#comment'+str(comment.pk),
                'author': current
            }
            create_notification(1, **notif)
            return redirect('comments')
    else:
        form = CommentForm()
    return redirect('comments')


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
    menu_display = Category.objects.filter(show='Yes')
    cat_count = menu_display.count()
    half = None

    if cat_count % 2 == 0:
        half = cat_count / 2
        left = menu_display[:half]
        right = menu_display[half:cat_count]
    else:
        half = cat_count / 2 + 1
        left = menu_display[:half]
        right = menu_display[half:cat_count]

    context = {
        'left_menu': left,
        'right_menu': right
    }
    return context


def load_bookmarks():
    categories = Category.objects.filter(show='Yes')
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


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        context['comments'] = Comment.objects.filter(status__exact="Show", post=pk)
        # context['comments'] = Comment.objects.filter(post=pk)
        context['query'] = Comment.objects.filter(status__exact="Show", post=pk)
        # context['query'] = Comment.objects.filter(post=pk).values('pk')
        context.update(load_menu())
        context.update(load_bookmarks())
        context.update(get_prev_next(pk))
        context['form'] = CommentForm()
        return context


def add_comment(request, pk):
    slug = Post.objects.only('slug').get(pk=pk).slug
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            num = random.randint(1, 10)
            image = "/media/profiles/p"+str(num)+".png"
            comment.image = image
            comment.save()
            title = comment.name.split(' ')[0]+" commented"
            notif = {
                'identity': comment.pk,
                'title': title,
                'message': comment.content,
                'notif_type': 'Comment',
                'link': '/comments/#comment'+str(comment.pk)
            }
            create_notification(0, **notif)
            return redirect('read', slug=slug)
    else:
        form = CommentForm()
    return redirect('read', slug=slug)


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'post'
    template_name = 'blog/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        work = Post.objects.filter(author=self.object.pk)[:2]
        tag = self.object.tags.split()
        opinions = Opinion.objects.filter(status__exact="Show", post=self.object)
        form = OpinionForm()
        context['form'] = form
        context['work'] = work
        context['tag'] = tag
        context['opinions'] = opinions
        context['query'] = Opinion.objects.filter(post=self.object).values('pk')
        context.update(load_menu())
        context.update(load_bookmarks())
        return context


def create_opinion(request, pk):
    slug = Author.objects.only('slug').get(pk=pk).slug
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            num = random.randint(1, 10)
            image = "/media/profiles/p"+str(num)+".png"
            opinion.image = image
            opinion.save()
            title = opinion.name.split(' ')[0]+" sent a message"
            notif = {
                'identity': opinion.pk,
                'title': title,
                'message': opinion.content,
                'notif_type': 'Opinion',
                'link': '/opinions/#comment'+str(opinion.pk)
            }
            create_notification(0, **notif)
            return redirect('author', slug=slug)
    else:
        form = OpinionForm()
    return redirect('author', slug=slug)


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


class CommentManage(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'dashboard/comment.html'
    # paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Comments'
        context['jumbo'] = 'Reply To A Comment'
        context['form'] = CommentForm()
        return context


@login_required
def get_comment(request, pk):
    c = Comment.objects.filter(pk=pk).values('content', 'name')
    context = {}
    if request.method == 'GET':
        comment = list(c)
        context = {
            'data': comment
        }
    print(context)
    return JsonResponse(context)


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


@login_required
def reply(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            current = request.user
            image = str(current.image.image.url)
            parent = Comment.objects.get(pk=pk)
            post_id = Comment.objects.only('post').get(pk=pk).post_id
            post = Post.objects.get(pk=post_id)

            comment.name = str(current.get_full_name())
            comment.email = str(current.email)
            comment.image = image
            comment.website = str(current.website)
            comment.author = current
            comment.post = post
            comment.parent = parent
            comment.save()
            title = str(current.first_name) + " replied to a comment"
            notif = {
                'identity': comment.pk,
                'title': title,
                'message': comment.content,
                'notif_type': 'Comment',
                'link': '/comments/#comment'+str(comment.pk),
                'author': current
            }
            create_notification(1, **notif)
            return redirect('comments')
    else:
        form = CommentForm()
    return redirect('comments')


@login_required
def get_edit_comment(request, pk):
    reply = ''
    c = Comment.objects.filter(pk=pk).values('pk', 'content', 'name', 'email', 'website', 'status', 'parent', 'post', 'author', 'image')
    post = Comment.objects.only('post').get(pk=pk).post_id
    title = list(Post.objects.filter(pk=post).values('title'))

    if Comment.objects.filter(pk=pk).values('parent') != None:
        p = Comment.objects.only('parent').get(pk=pk).parent_id
        reply = list(Comment.objects.filter(pk=p).values('content', 'name'))

    context = {}
    if request.method == 'GET':
        comment = list(c) + title
        context = {
            'data': comment,
            'reply': reply
        }
    return JsonResponse(context)


@login_required
def edit_comment(request, pk):
    c = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=c)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('comments'))
        cObjs = Comment.objects.all().values()
        comments = list(cObjs)
        return JsonResponse(comments, safe=False)
    else:
        return render(request, 'dashboard/comment.html', {'comments': Comment.objects.all()})

# Opinion
class OpinionManage(ListView):
    model = Opinion
    context_object_name = 'opinions'
    template_name = 'dashboard/opinion.html'
    # paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Opinions'
        context['sectionname'] = 'Opinions | Messages'
        context['jumbo'] = 'Reply To A Comment'
        context['form'] = OpinionForm()
        return context


@login_required
def get_opinion(request, pk):
    o = Opinion.objects.filter(pk=pk).values('content', 'name')
    context = {}
    if request.method == 'GET':
        opinion= list(o)
        context = {
            'data': opinion
        }
    return JsonResponse(context)


@login_required
def delete_opinion(request, pk):
    o = Opinion.objects.get(pk=pk)
    if request.method == 'POST':
        o.delete()
        opObjs = Opinion.objects.all().values()
        opinions = list(opObjs)
        return JsonResponse(opinions, safe=False)
    else:
        return render(request, 'dashboard/opinion.html', {'opinions':Opinion.objects.all()})


@login_required
def reply_opinion(request, pk):
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            current = request.user
            image = str(current.image.image.url)
            parent = Opinion.objects.get(pk=pk)
            post_id = Opinion.objects.only('post').get(pk=pk).post_id
            post = get_user_model().objects.get(pk=post_id)
            opinion.name = str(current.get_full_name())
            opinion.email = str(current.email)
            opinion.image = image
            opinion.website = str(current.website)
            opinion.is_author = 'Yes'
            opinion.post = post
            opinion.parent = parent
            opinion.save()
            title = str(current.first_name) + " replied to a message"
            notif = {
                'identity': opinion.pk,
                'title': title,
                'message': opinion.content,
                'notif_type': 'Opinion',
                'link': '/opinions/#comment'+str(opinion.pk),
                'author': current
            }
            create_notification(1, **notif)
            return redirect('opinions')
    else:
        form = OpinionForm()
    return redirect('opinions')


@login_required
def get_edit_opinion(request, pk):
    reply = ''
    o = Opinion.objects.filter(pk=pk).values('pk', 'content', 'name', 'email', 'website', 'status', 'parent', 'post', 'is_author', 'image')

    post = Opinion.objects.only('post').get(pk=pk).post_id
    fname = get_user_model().objects.only('first_name').get(pk=post).first_name
    lname = get_user_model().objects.only('last_name').get(pk=post).last_name
    authorr = fname + " " + lname
    title = "Know Our Authors: " + authorr

    if Opinion.objects.filter(pk=pk).values('parent') != None:
        p = Opinion.objects.only('parent').get(pk=pk).parent_id
        reply = list(Opinion.objects.filter(pk=p).values('content', 'name'))

    context = {}
    if request.method == 'GET':
        opinion = list(o)
        context = {
            'data': opinion,
            'reply': reply,
            'title': title
        }
    return JsonResponse(context)


@login_required
def edit_opinion(request, pk):
    o = Opinion.objects.get(pk=pk)
    form = OpinionForm(request.POST or None, instance=o)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('opinions'))
        opObjs = Opinion.objects.all().values()
        opinion = list(opObjs)
        return JsonResponse(opinion, safe=False)
    else:
        return render(request, 'dashboard/opinion.html', {'opinion': Opinion.objects.all()})


def create_notification(check, **data):
    checker = check
    n = None
    try:
        if checker == 0:
            n = Notification(
                identity = data['identity'],
                title = data['title'],
                message = data['message'],
                notif_type = data['notif_type'],
                link = data['link']
            )
        elif checker == 1:
            n = Notification(
                identity = data['identity'],
                title = data['title'],
                message = data['message'],
                notif_type = data['notif_type'],
                link = data['link'],
                author = data['author']
            )
        n.save()
    except Exception as e:
        print("\n\nSave Notification ERROR: "+str(e)+"\n\n")


@login_required
def dashboard(request):
    notifications = Notification.objects.all()
    count = Notification.objects.filter(seen=0).count()
    now = datetime.now()
    print(now)
    context = {
        'pagename': "Dashboard",
        'notifications': notifications,
        'new': count,
        'time_now': now
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def delete_notification(request):
    notif = request.POST['pk']
    n = Notification.objects.get(pk=notif)
    if request.method == 'POST':
        n.delete()
        nObjs = Notification.objects.all().values()
        notifications = list(nObjs)
        return JsonResponse(notifications, safe=False)
    else:
        return render(request, 'dashboard/dashboard.html', {'notifications':Notification.objects.all()})


@login_required
def read_status_notif(request):
    notif = request.POST['pk']
    new = request.POST['status']
    n = Notification.objects.get(pk=notif)
    if request.method == 'POST':
        n.seen = new
        n.save()
        nObjs = Notification.objects.all().values()
        notifications = list(nObjs)
        return JsonResponse(notifications, safe=False)
    else:
        return render(request, 'dashboard/dashboard.html', {'notifications': Notification.objects.all()})


# @login_required
def sendRegisterMail(email, name, uname):
    form = PasswordResetForm({'email': email})

    subject = 'Welcome To Leicunn Studio Blog'
    from_email = 'no-reply@leicunnstudio.com'
    to = email
    context = {
        'firstname': name,
        'username': uname
    }
    email_template_name = render_to_string('mail/mail.html', context)
    template_name = render_to_string('mail/mail.html', context)

    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = '127.0.0.1'
        request.META['SITE_ID'] = 'Leicunn Studio Blog'
        # request.META['SERVER_PORT'] = '443'
        request.META['SERVER_PORT'] = '80'
        send_mail(subject, template_name, from_email, [to], fail_silently=False, html_message=email_template_name)
        form.save(
            request = request,
            use_https = False,
            from_email = from_email,
            html_email_template_name = 'registration/password_reset_email.html',
            email_template_name = 'registration/password_reset_email.html'
        )


def generate_username(fname, lname):
    uname = fname + lname[0:3]
    username = uname.lower()
    return username


class Register(CreateView):
    model = get_user_model()
    form_class = AuthorCreationForm
    login_required = True
    template_name = 'dashboard/register.html'

    def get_success_url(self):
        return reverse('register')

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['pagename'] = 'Create User'
        context['jumbo'] = 'Create New Accounts'
        context['jumbomessage'] = 'Create new authors for your blog'
        context['users'] = Author.objects.exclude(username=self.request.user).values('pk', 'first_name', 'last_name', 'username', 'slug', 'email', 'website', 'twitter', 'instagram', 'linkedin')
        context.update(get_author_media())
        return context

    def form_valid(self, form):
        emailAddress = str(form.cleaned_data['email'])
        first_name = str(form.cleaned_data['first_name'])
        last_name = str(form.cleaned_data['last_name'])
        username = str(generate_username(first_name, last_name))
        newUser = form.save(commit = False)
        newUser.username = username
        newUser.is_superuser = False
        newUser.is_staff = True
        newUser.is_active = True
        newUser.save()
        sendRegisterMail(emailAddress, first_name, username)
        return super(Register, self).form_valid(form)


@login_required
def delete_author(request, slug):
    u = Author.objects.get(slug=slug)
    if request.method == 'POST':
        u.delete()
        uObjs = Author.objects.exclude(username=request.user).values('first_name', 'last_name', 'username', 'slug', 'email', 'website', 'twitter', 'instagram', 'linkedin')
        users = list(uObjs)
        return JsonResponse(users, safe=False)
    else:
        userss = Author.objects.exclude(username=request.user).values('first_name', 'last_name', 'username', 'slug', 'email', 'website', 'twitter', 'instagram', 'linkedin')
        return render(request, 'dashboard/quotes.html', {'users':userss})


def error404(request, exception):
    return render(request, '404.html', status=404)


def error500(request):
    return render(request, '500.html', status=500)