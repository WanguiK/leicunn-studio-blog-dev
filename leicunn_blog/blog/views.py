from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse

from blog.forms import AuthorChangeForm, CategoryForm
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


# class UpdateAuthor(UpdateView):
#     model = get_user_model()
#     form_class = AuthorChangeForm
#     login_required = True
#     template_name = 'dashboard/updateprofile.html'

#     def get(self, request, **kwargs):
#         self.object = Author.objects.get(pk=self.request.user)
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         context = self.get_context_data(object=self.object, form=form)
#         return self.render_to_response(context)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def get_context_data(self, **kwargs):
#         context = super(UpdateAuthor, self).get_context_data(**kwargs)
#         context['pagename'] = 'User Profile'
#         return context


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


# class UpdateAuthor(UpdateView):
#     model = get_user_model()
#     form_class = AuthorEditForm
#     login_required = True
#     template_name = 'user/login.html'

#     def get_context_data(self, **kwargs):
#         context = super(UpdateAuthor, self).get_context_data(**kwargs)
#         context['pagename'] = 'Update Profile'
#         return context