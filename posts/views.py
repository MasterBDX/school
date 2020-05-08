from django.shortcuts import render
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView,)
from django.urls import reverse, reverse_lazy

from .models import Post
from .forms import AddPostForm


class PostsListView(ListView):
    context_object_name = 'posts'
    model = Post
    fields = '__all__'
    template_name = 'posts/posts_list_view.html'


class PostDetailView(DetailView):
    model = Post
    fields = '__all__'
    context_object_name = 'post'
    template_name = 'posts/post_detail_view.html'


class AddPostView(CreateView):
    form_class = AddPostForm
    template_name = 'posts/add_post.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.author = user
        self.object.save()
        return super().form_valid(form)


class EditPostView(UpdateView):
    queryset = Post.objects.all()
    form_class = AddPostForm
    template_name = 'posts/add_post.html'

    def get_success_url(self):
        from_dash = self.request.GET.get('from_dash')
        if from_dash == '1':
            url = reverse('main:posts-dahsboard')
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


class PostDeleteView(DeleteView):
    queryset = Post.objects.all()
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('main:posts-dashboard')
