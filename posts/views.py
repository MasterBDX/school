from django.shortcuts import render
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView,)
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Post
from .forms import AddPostForm
from .mixins import OwnUserObjectMixin, OUOAndAdminMixin


class PostsListView(ListView):
    context_object_name = 'posts'
    queryset = Post.objects.active()
    template_name = 'posts/posts_list_view.html'
    paginate_by = 5
    

class PostDetailView(DetailView):
    queryset = Post.objects.active()
    context_object_name = 'post'
    template_name = 'posts/post_detail_view.html'


class AddPostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    success_message = _('Post has been added')
    success_url = reverse_lazy('main:posts-dashboard')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.author = user
        self.object.save()
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, OwnUserObjectMixin, SuccessMessageMixin, UpdateView):
    queryset = Post.objects.all()
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('main:posts-dashboard')
    success_message = _('Post has been modified')


class PostDeleteView(LoginRequiredMixin, OUOAndAdminMixin, SuccessMessageMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('main:posts-dashboard')
    success_message = _('Post has been deleted')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
