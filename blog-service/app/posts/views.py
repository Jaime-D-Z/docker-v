from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y obtener posts.
    Cacheo en detalle: 60 segundos
    """
    queryset = Post.objects.filter(status='published').select_related('author', 'category')
    permission_classes = [AllowAny]
    search_fields = ['title', 'body']
    filterset_fields = ['category', 'author']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalle de un post con incremento de views"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(body__icontains=search)
            )
        return queryset

