from django.urls import path

from .views import (PostsListView, PostDetailView,
                    AddPostView, EditPostView,
                    PostDeleteView)

app_name = 'posts'
urlpatterns = [
    path('', PostsListView.as_view(), name='list'),

    path('add/', AddPostView.as_view(), name='add'),
    path('<slug:slug>/edit/', EditPostView.as_view(), name='edit'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]
