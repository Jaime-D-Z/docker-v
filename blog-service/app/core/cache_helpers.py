from django.core.cache import cache
from functools import wraps


def cache_result(prefix='cache', timeout=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Crear clave de cache basada en args y kwargs
            key_parts = [prefix]
            if args:
                key_parts.extend(str(arg) for arg in args)
            if kwargs:
                sorted_kwargs = sorted(kwargs.items())
                key_parts.extend(f"{k}={v}" for k, v in sorted_kwargs)
            
            cache_key = ":".join(key_parts)
            
            # Intentar obtener del cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Ejecutar función y guardar resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator


def invalidate_cache(pattern):
    """
    Invalidar cache basado en un patrón.
    
    Args:
        pattern: Patrón para buscar claves (ej: 'posts:*', 'categories:*')
    
    Ejemplo:
        invalidate_cache('posts:*')
    """
    try:
        redis_conn = cache.get_master_client()
        keys = redis_conn.keys(pattern)
        if keys:
            redis_conn.delete(*keys)
            return len(keys)
    except Exception as e:
        print(f"Error invalidando cache: {e}")
        return 0


def get_cache_stats():
    """
    Obtener estadísticas del cache (solo para Redis).
    
    Returns:
        dict: Estadísticas del cache o None si no hay Redis
    """
    try:
        redis_conn = cache.get_master_client()
        info = redis_conn.info()
        return {
            'total_keys': redis_conn.dbsize(),
            'memory_used': info.get('used_memory_human', 'N/A'),
            'hits': info.get('keyspace_hits', 0),
            'misses': info.get('keyspace_misses', 0),
        }
    except Exception:
        return None


def clear_all_cache():
    """
    Limpiar todo el cache.
    
    Returns:
        bool: True si se limpió correctamente
    """
    try:
        cache.clear()
        return True
    except Exception as e:
        print(f"Error limpiando cache: {e}")
        return False

