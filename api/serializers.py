from rest_framework import serializers

from blog.models import Post,Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class BlogSerializers(serializers.ModelSerializer):
    category = CategorySerializers(many=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'category')
