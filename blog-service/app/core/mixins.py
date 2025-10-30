"""
Mixins útiles para Views y ViewSets
"""
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response


class CacheMixin:
    """
    Mixin para agregar cache a los métodos de un ViewSet.
    
    Uso:
        class MyViewSet(CacheMixin, viewsets.ReadOnlyModelViewSet):
            cache_timeout = 60
            cache_actions = ['list', 'retrieve']
    """
    cache_timeout = 60
    cache_actions = ['list', 'retrieve']

    def get_cache_timeout(self):
        """Override para retornar timeout dinámico."""
        return self.cache_timeout

    def dispatch(self, request, *args, **kwargs):
        """
        Aplica cache según cache_actions.
        """
        if self.action in self.cache_actions:
            timeout = self.get_cache_timeout()
            decorator = cache_page(timeout)
            # Aplicar decorador solo a métodos especificados
            original_dispatch = super().dispatch
            wrapper = decorator(original_dispatch)
            return wrapper(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class SoftDeleteMixin:
    """
    Mixin para soft delete de objetos.
    
    Agrega campo is_deleted y métodos para soft delete.
    """
    def perform_destroy(self, instance):
        """
        En lugar de borrar, marca como eliminado.
        """
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        """
        Filtra objetos no eliminados.
        """
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False)


class ActionResponseMixin:
    """
    Mixin para respuestas personalizadas en acciones.
    """
    def custom_response(self, data, status_code=status.HTTP_200_OK, message=None):
        """
        Crea una respuesta personalizada con mensaje opcional.
        """
        response_data = {'data': data}
        if message:
            response_data['message'] = message
        return Response(response_data, status=status_code)

    def success_response(self, data, message="Success"):
        """
        Respuesta de éxito estándar.
        """
        return self.custom_response(data, message=message, status_code=status.HTTP_200_OK)

    def created_response(self, data, message="Created"):
        """
        Respuesta de creación exitosa.
        """
        return self.custom_response(data, message=message, status_code=status.HTTP_201_CREATED)

    def error_response(self, message="Error occurred", status_code=status.HTTP_400_BAD_REQUEST):
        """
        Respuesta de error.
        """
        return Response({'error': message}, status=status_code)

