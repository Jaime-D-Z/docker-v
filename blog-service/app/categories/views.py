from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer


@method_decorator(cache_page(120), name='dispatch')
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar categorías activas.
    Cacheo: 120 segundos
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

