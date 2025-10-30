import os
import sys

# Agregar el directorio app al path para que Django pueda encontrar los módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás segura de que está instalado y "
            "¿Disponible en tu variable de entorno PYTHONPATH? ¿Lo hiciste? "
            "¿Olvidó activar un entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

