# Auth Service - Django REST API con JWT

Servicio de autenticación basado en Django REST Framework con JWT (JSON Web Tokens).

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Puertos 8000, 5432 y 6379 disponibles

## 🚀 Inicio Rápido

### 1. Construir y levantar los contenedores

```bash
docker-compose up -d --build
```

Esto levantará:
- **PostgreSQL** en el puerto 5432
- **Redis** en el puerto 6379
- **Auth Service** (Django) en el puerto 8000

### 2. Crear las migraciones

```bash
docker exec -it auth_service python manage.py makemigrations
docker exec -it auth_service python manage.py migrate
```

### 3. Crear un superusuario (opcional)

```bash
docker exec -it auth_service python manage.py createsuperuser
```

### 4. Verificar la conexión

```bash
docker exec -it auth_service python test_connection.py
```

## 🔗 Endpoints Disponibles

Base URL: `http://localhost:8000/api/`

### Autenticación JWT

- **POST** `/api/token/` - Obtener token JWT (login)
- **POST** `/api/token/refresh/` - Refrescar token JWT
- **POST** `/api/register/` - Registrar nuevo usuario
- **POST** `/api/login/` - Login personalizado con respuesta completa
- **GET** `/api/me/` - Obtener información del usuario actual (requiere autenticación)
- **POST** `/api/logout/` - Logout (invalidar token)

### Admin

- **GET** `/admin/` - Panel de administración de Django

## 📝 Ejemplos de Uso

### Registro de Usuario

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123"
  }'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Acceder a endpoint protegido

```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Refrescar token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker-compose logs -f auth
```

### Entrar al contenedor
```bash
docker exec -it auth_service bash
```

### Detener contenedores
```bash
docker-compose down
```

### Detener y eliminar volúmenes (reset completo)
```bash
docker-compose down -v
```

### Reconstruir después de cambios
```bash
docker-compose down
docker-compose up -d --build
```

## 📁 Estructura del Proyecto

```
auth-service/
├── auth_service/          # Configuración del proyecto Django
│   ├── settings.py       # Configuración principal
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── users/                 # App de usuarios
│   ├── models.py         # Modelo de usuario personalizado
│   ├── views.py          # Endpoints de API
│   ├── serializers.py    # Serializers de DRF
│   └── urls.py           # URLs de la app users
├── Dockerfile            # Configuración Docker
├── requirements.txt      # Dependencias Python
├── manage.py            # Script de gestión Django
└── test_connection.py  # Script para probar conexiones
```

## ⚙️ Configuración

### Variables de Entorno

Configuradas en `docker-compose.yml`:

- `DEBUG`: Modo debug (1 o 0)
- `DB_HOST`: Host de PostgreSQL
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de PostgreSQL
- `DB_PASS`: Contraseña de PostgreSQL
- `REDIS_HOST`: Host de Redis
- `REDIS_PORT`: Puerto de Redis

### Características

- ✅ Usuario personalizado basado en email
- ✅ Autenticación JWT con `djangorestframework-simplejwt`
- ✅ Cache con Redis
- ✅ CORS configurado para frontend
- ✅ Validación de contraseñas
- ✅ Endpoints de registro, login, logout y perfil

## 🗄️ Base de Datos

### Modelo de Usuario

El proyecto usa un modelo de usuario personalizado con:
- Email (único y requerido)
- First name / Last name
- is_active: Estado del usuario
- is_admin: Permisos de administrador
- Password: Guardado con hash

### Migraciones

Las migraciones se crean automáticamente con `makemigrations` y se aplican con `migrate`.

## 🔒 Seguridad

- Passwords hasheados con bcrypt
- Tokens JWT con expiración configurable
- CSRF protection habilitado
- CORS configurado solo para orígenes permitidos
- Validación de contraseñas con longitud mínima

## 📚 Tecnologías

- Django 5.0
- Django REST Framework 3.15
- djangorestframework-simplejwt 5.3
- PostgreSQL 15
- Redis 7
- Gunicorn (servidor WSGI)
- django-cors-headers
- psycopg2-binary

## 🐛 Solución de Problemas

### Error de conexión a la base de datos

```bash
# Verificar que PostgreSQL está corriendo
docker ps | grep postgres

# Ver logs de PostgreSQL
docker-compose logs postgres
```

### Error de migraciones

```bash
# Eliminar migraciones
docker exec -it auth_service rm -rf users/migrations/0*.py

# Recrear migraciones
docker exec -it auth_service python manage.py makemigrations
docker exec -it auth_service python manage.py migrate
```

### Puerto ya en uso

Si el puerto 8000 está ocupado, modifica el puerto en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Cambiar 8001 por el puerto que prefieras
```

### Reconstruir completamente

```bash
docker-compose down -v
docker-compose up -d --build
docker exec -it auth_service python manage.py makemigrations
docker exec -it auth_service python manage.py migrate
```

CAPTURAS DE POSTMAN:
Register:
<img width="1742" height="905" alt="Captura de pantalla 2025-10-27 094801" src="https://github.com/user-attachments/assets/0ea86e9f-f46c-4340-bc59-e1065b53612a" />

Login:
<img width="1730" height="859" alt="Captura de pantalla 2025-10-27 094826" src="https://github.com/user-attachments/assets/1f8c21dc-5563-4d6d-9497-8de4710086a5" />

Refresh token:
<img width="1727" height="883" alt="Captura de pantalla 2025-10-27 094841" src="https://github.com/user-attachments/assets/699f34b7-31d7-4b1f-a8d6-22fdd6a0f86a" />

Contenedores docker:
<img width="1497" height="219" alt="Captura de pantalla 2025-10-27 100131" src="https://github.com/user-attachments/assets/1a252b1a-6129-4f02-bdd6-dd8030b0b65d" />
<img width="1330" height="123" alt="Captura de pantalla 2025-10-27 100255" src="https://github.com/user-attachments/assets/fc516d64-8d02-49b1-a696-83a1e0210a1e" />
