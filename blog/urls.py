from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogPostCreateView, BlogPostUpdateView, BlogDeleteView, \
    UserPostListView, CommentDeleteView, SearchView, CategoryCreateView, ContactView

urlpatterns = [
    path('',BlogListView.as_view(),name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('blogpost/<int:pk>/',BlogDetailView.as_view(),name='blog-detail'),
    path('blogcreate/new/',BlogPostCreateView.as_view(),name='create-blog'),
    path('blogupdate/<int:pk>/update', BlogPostUpdateView.as_view(), name='update-blog'),
    path('blogdelete/<int:pk>/delete', BlogDeleteView.as_view(), name='delete-blog'),
    path('about/',ContactView.as_view(),name='blog-about'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path("search/",SearchView.as_view(),name='search-blog'),
    path("category/create/",CategoryCreateView.as_view(),name='create-category'),
   
]

