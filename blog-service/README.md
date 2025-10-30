# Blog Service - Django REST API

Microservicio para gestión de blog con posts y categorías, incluyendo paginación, búsqueda y caché con Redis.

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- El proyecto auth-service debe estar corriendo
- Puertos 8001, 5432 y 6379 disponibles

## 🚀 Inicio Rápido

### 1. Levantar el servicio

Desde la raíz del proyecto (donde está `docker-compose.yml`):

```bash
docker-compose up -d --build blog
```

### 2. Aplicar migraciones

```bash
docker exec -it blog_service python manage.py makemigrations
docker exec -it blog_service python manage.py migrate
```

### 3. Poblar la base de datos con datos de ejemplo

```bash
docker exec -it blog_service python manage.py seed_blog
```

### 4. Verificar el servicio

```bash
# Healthcheck
curl http://localhost:8001/healthz

# Listar categorías
curl http://localhost:8001/api/categories/

# Listar posts
curl http://localhost:8001/api/posts/
```

## 🔗 Endpoints Disponibles

Base URL: `http://localhost:8001/api/`

### Categorías

- **GET** `/api/categories/` - Lista todas las categorías activas
  - Cache: 120 segundos

### Posts

- **GET** `/api/posts/` - Lista posts publicados con paginación
  - Query params: `?search=palabra&page=1`
  - Paginación: 10 resultados por página

- **GET** `/api/posts/{id}/` - Obtiene el detalle de un post
  - Cache: 60 segundos
  - Incrementa automáticamente el contador de views

### Health

- **GET** `/healthz` - Verifica estado de PostgreSQL y Redis

## 📝 Ejemplos de Uso

### Listar categorías

```bash
curl http://localhost:8001/api/categories/
```

**Respuesta:**
```json
[
  {"id": 1, "name": "Tecnología", "slug": "tecnologia"},
  {"id": 2, "name": "Programación", "slug": "programacion"}
]
```

### Listar posts con paginación

```bash
curl http://localhost:8001/api/posts/
```

**Respuesta:**
```json
{
  "count": 30,
  "next": "http://localhost:8001/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introducción a Django REST Framework",
      "slug": "introduccion-a-django-rest-framework",
      "excerpt": "Django REST Framework es una poderosa herramienta...",
      "author": {"id": 1, "display_name": "María García"},
      "category": {"id": 1, "name": "Programación"},
      "published_at": "2025-10-15T10:00:00Z",
      "views": 245
    }
  ]
}
```

### Buscar posts

```bash
curl "http://localhost:8001/api/posts/?search=Django"
```

Busca posts que contengan "Django" en el título o cuerpo.

### Obtener detalle de un post

```bash
curl http://localhost:8001/api/posts/1/
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Introducción a Django REST Framework",
  "slug": "introduccion-a-django-rest-framework",
  "body": "Contenido completo del post...",
  "author": {"id": 1, "display_name": "María García"},
  "category": {"id": 1, "name": "Programación"},
  "published_at": "2025-10-15T10:00:00Z",
  "views": 246,
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-10-15T12:30:00Z"
}
```

### Healthcheck

```bash
curl http://localhost:8001/healthz
```

**Respuesta (healthy):**
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker-compose logs -f blog
```

### Entrar al contenedor
```bash
docker exec -it blog_service bash
```

### Crear superusuario para admin
```bash
docker exec -it blog_service python manage.py createsuperuser
```

### Acceder al admin
```bash
# Abrir en navegador
http://localhost:8001/admin/
```

### Recrear seed con más datos
```bash
# Limpiar posts existentes (opcional)
docker exec -it blog_service python manage.py shell
>>> from posts.models import Post
>>> Post.objects.all().delete()
>>> exit()

# Crear más datos
docker exec -it blog_service python manage.py seed_blog --posts 50 --authors 5
```

### Detener servicio
```bash
docker-compose down blog
# o detener todo
docker-compose down
```

## 📁 Estructura del Proyecto

```
blog-service/
├── blog_service/           # Configuración Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py            # URLs principales
│   ├── views.py           # Vista de healthcheck
│   └── wsgi.py            # WSGI
├── core/                  # Utilidades compartidas
│   ├── cache_helpers.py   # Helpers de caché Redis
│   ├── pagination.py      # Clases de paginación
│   ├── mixins.py          # Mixins para ViewSets
│   └── filters.py         # Filtros personalizados
├── categories/            # App de categorías
│   ├── models.py         # Modelo Category
│   ├── views.py          # ViewSet con caché
│   └── serializers.py    # Serializers
├── authors/              # App de autores
│   └── models.py         # Modelo Author
├── posts/                # App de posts
│   ├── models.py         # Modelo Post
│   ├── views.py          # ViewSet con búsqueda
│   ├── serializers.py    # Serializers list y detail
│   └── management/
│       └── commands/
│           └── seed_blog.py  # Comando para poblar BD
├── Dockerfile            # Configuración Docker
├── requirements.txt      # Dependencias
├── manage.py             # Script Django
└── openapi.yaml         # Contrato OpenAPI
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

- ✅ Posts con estados (published/draft)
- ✅ Paginación automática (10 por página)
- ✅ Búsqueda en título y cuerpo
- ✅ Cache Redis en categorías (120s) y posts detail (60s)
- ✅ Contador de views
- ✅ Healthcheck de BD y Redis
- ✅ Logging estructurado en JSON

## 🗄️ Modelos

### Category

- `id`: Identificador único
- `name`: Nombre de la categoría
- `slug`: URL-friendly name
- `is_active`: Categoría activa o no

### Author

- `id`: Identificador único
- `display_name`: Nombre para mostrar
- `email`: Email único

### Post

- `id`: Identificador único
- `title`: Título del post
- `slug`: URL-friendly title
- `body`: Contenido del post
- `author`: Relación con Author (FK)
- `category`: Relación con Category (FK)
- `status`: published o draft
- `published_at`: Fecha de publicación
- `views`: Contador de visualizaciones
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

## 🔒 Seguridad

- Los endpoints son públicos por ahora
- Preparado para integrar autenticación JWT desde auth-service
- CSRF protection habilitado

## 📚 Tecnologías

- Django 5.0
- Django REST Framework 3.15
- PostgreSQL 15
- Redis 7
- django-filter
- python-slugify
- Gunicorn
- django-redis

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
# Recrear migraciones
docker exec -it blog_service python manage.py makemigrations
docker exec -it blog_service python manage.py migrate
```

### Puerto ya en uso

Si el puerto 8001 está ocupado, modifica en `docker-compose.yml`:

```yaml
ports:
  - "8002:8001"  # Cambiar por otro puerto
```

### Cache no funciona

Verifica que Redis está corriendo:

```bash
docker ps | grep redis
docker exec cache_redis redis-cli ping
# Debe responder: PONG
```

## 📊 Estadísticas del Seed

El comando `seed_blog` crea por defecto:

- **5 categorías**: Tecnología, Programación, Django, Python, JavaScript
- **3 autores**: Con nombres y emails únicos
- **30 posts**: 80% published, 20% draft
  - Contenido variado con títulos y cuerpos
  - Fechas de publicación distribuidas en los últimos 60 días
  - Views aleatorios (0-1000 para publicados)

### Personalizar seeds

```bash
# Más posts
python manage.py seed_blog --posts 100

# Más categorías
python manage.py seed_blog --categories 10

# Más autores
python manage.py seed_blog --authors 5

# Todo junto
python manage.py seed_blog --categories 10 --authors 5 --posts 100
```

## 🌐 Integración con Frontend

El archivo `openapi.yaml` contiene el contrato completo de la API para que el frontend pueda trabajar con ella.

CAPTURAS DE PANTALLA:

Terminal con contenedores:
<img width="1346" height="140" alt="Captura de pantalla 2025-10-27 123849" src="https://github.com/user-attachments/assets/dd9c7417-4974-4172-b0e6-40b917b08d1f" />


Health:
<img width="1387" height="693" alt="image" src="https://github.com/user-attachments/assets/bdf5c7b9-060f-4334-8e30-80379541f712" />

Categorías:
<img width="1389" height="871" alt="Captura de pantalla 2025-10-27 125335" src="https://github.com/user-attachments/assets/0b894ac6-12d5-4115-bdfa-c303dbd4ce3a" />

Post:
<img width="1490" height="926" alt="Captura de pantalla 2025-10-27 131202" src="https://github.com/user-attachments/assets/c7b52f11-632c-4cda-98bd-f0cdbab989d1" />

Detalle de post 2:
<img width="1366" height="844" alt="Captura de pantalla 2025-10-27 131037" src="https://github.com/user-attachments/assets/8ef9972c-dfd7-4912-bd93-3c008b332cf1" />

Buscando post por paginación:
<img width="1543" height="885" alt="Captura de pantalla 2025-10-27 131334" src="https://github.com/user-attachments/assets/e1e77824-3134-4595-937b-ef4daabb309a" />

