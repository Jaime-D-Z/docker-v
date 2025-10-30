"""
Filtros personalizados para el Blog Service
"""
import django_filters
from django.db import models


class DateRangeFilter(django_filters.FilterSet):
    """
    Filtro de rango de fechas genérico.
    """
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    published_after = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_at', lookup_expr='lte')


class TextSearchFilter(django_filters.FilterSet):
    """
    Filtro de búsqueda de texto genérico.
    """
    search = django_filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        """
        Busca en múltiples campos de texto.
        Sobreescribe en clases hijas.
        """
        return queryset


def get_search_fields(model_class, field_names):
    """
    Helper para obtener campos de búsqueda dinámicamente.
    
    Args:
        model_class: Clase del modelo
        field_names: Lista de nombres de campos
    
    Returns:
        list: Lista de campos Q para búsqueda
    """
    search_fields = []
    for field_name in field_names:
        try:
            field = model_class._meta.get_field(field_name)
            if isinstance(field, (models.CharField, models.TextField)):
                search_fields.append(f'{field_name}__icontains')
        except Exception:
            pass
    return search_fields


class MultiFieldSearchFilter:
    """
    Filtro para búsqueda en múltiples campos.
    
    Uso:
        class MyViewSet(viewsets.ReadOnlyModelViewSet):
            search_fields = ['title', 'body', 'author__name']
            filter_backends = [MultiFieldSearchFilter]
    """
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search', None)
        if search:
            from django.db.models import Q
            q_objects = Q()
            for field in view.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(q_objects)
        return queryset

