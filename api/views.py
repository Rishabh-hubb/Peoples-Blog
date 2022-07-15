from rest_framework import generics
from blog.models import Post

from .serializers import BlogSerializers

class BlogApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializers

class DetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializers
