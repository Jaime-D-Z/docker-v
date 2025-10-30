from rest_framework import serializers
from .models import Post


class AuthorNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    display_name = serializers.CharField()


class CategoryNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class PostListSerializer(serializers.ModelSerializer):
    """Serializer para la lista de posts (con excerpt)"""
    author = AuthorNestedSerializer(read_only=True)
    category = CategoryNestedSerializer(read_only=True)
    excerpt = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 'published_at', 'views']


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer para el detalle de un post (con body completo)"""
    author = AuthorNestedSerializer(read_only=True)
    category = CategoryNestedSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'author', 'category', 'published_at', 'views', 'created_at', 'updated_at']

