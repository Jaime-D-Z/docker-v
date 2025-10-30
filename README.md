# Laboratorio de Microservicios (Django + React)

## Arquitectura inicial
- auth-service/      → Autenticación y tokens JWT
- blog-service/      → Publicaciones, autores y categorías
- email-service/     → Notificaciones y formularios
- frontend/          → Interfaz React
- reverse-proxy/     → Balanceo / Gateway local

Servicios base:
- PostgreSQL (5432)
- Redis (6379)