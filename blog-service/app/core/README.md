# Core - Utilidades del Blog Service

Este módulo contiene utilidades compartidas para el Blog Service.

## 📁 Estructura

### `cache_helpers.py`
Utilidades para manejo de caché con Redis:
- `cache_result`: Decorador para cachear resultados de funciones
- `invalidate_cache`: Invalidar cache por patrón
- `get_cache_stats`: Obtener estadísticas del cache
- `clear_all_cache`: Limpiar todo el cache

### `pagination.py`
Clases de paginación personalizadas:
- `StandardResultsSetPagination`: 10 por página (por defecto)
- `LargeResultsSetPagination`: 25 por página
- `SmallResultsSetPagination`: 5 por página

### `mixins.py`
Mixins útiles para ViewSets:
- `CacheMixin`: Agrega cache automático a acciones
- `SoftDeleteMixin`: Soft delete de objetos
- `ActionResponseMixin`: Respuestas personalizadas

### `filters.py`
Filtros personalizados:
- `DateRangeFilter`: Filtro de rango de fechas
- `TextSearchFilter`: Filtro de búsqueda de texto
- `MultiFieldSearchFilter`: Búsqueda en múltiples campos

## 🔧 Uso

### Paginación
Ya está configurada en `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
}
```

### Caché en ViewSets
```python
from core.mixins import CacheMixin

class PostViewSet(CacheMixin, viewsets.ReadOnlyModelViewSet):
    cache_timeout = 60
    cache_actions = ['list', 'retrieve']
    # ...
```

### Cachear resultado de función
```python
from core.cache_helpers import cache_result

@cache_result(prefix='posts', timeout=120)
def get_popular_posts():
    return Post.objects.filter(views__gt=100)
```

### Filtros personalizados
```python
from core.filters import DateRangeFilter

class PostFilter(DateRangeFilter):
    class Meta:
        model = Post
        fields = ['category', 'author']
```

## 📊 Respuesta de Paginación

```json
{
  "count": 25,
  "page_size": 10,
  "total_pages": 3,
  "current_page": 1,
  "next": "http://localhost:8001/api/posts/?page=2",
  "previous": null,
  "results": [...]
}
```

