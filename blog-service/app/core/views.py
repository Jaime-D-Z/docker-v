import logging
from django.http import JsonResponse
from django.db import connection
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def healthz(request):
    """
    Endpoint de healthcheck que verifica:
    - Conexión a PostgreSQL
    - Conexión a Redis
    """
    status_code = 200
    health_status = {
        'status': 'healthy',
        'checks': {}
    }

    # Verificar PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['checks']['database'] = 'ok'
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        health_status['checks']['database'] = 'error'
        status_code = 503

    # Verificar Redis
    try:
        redis_conn = get_redis_connection('default')
        redis_conn.ping()
        health_status['checks']['redis'] = 'ok'
    except Exception as e:
        logger.error(f"Redis check failed: {e}")
        health_status['checks']['redis'] = 'error'
        status_code = 503

    if 'error' in [v for v in health_status['checks'].values()]:
        health_status['status'] = 'unhealthy'

    return JsonResponse(health_status, status=status_code)
