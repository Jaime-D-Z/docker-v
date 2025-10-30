from django.core.management.base import BaseCommand
from categories.models import Category
from authors.models import Author
from posts.models import Post
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample blog data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Number of categories to create (default: 5)',
        )
        parser.add_argument(
            '--authors',
            type=int,
            default=3,
            help='Number of authors to create (default: 3)',
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=30,
            help='Number of posts to create (default: 30)',
        )

    def handle(self, *args, **options):
        num_categories = options['categories']
        num_authors = options['authors']
        num_posts = options['posts']

        self.stdout.write('Starting blog seeding...')

        # Create categories
        categories = []
        categories_names = [
            'Tecnología', 'Programación', 'Django', 'Python', 'JavaScript',
            'Web Development', 'Mobile Apps', 'DevOps', 'Cloud Computing', 'AI & Machine Learning'
        ]
        
        for i in range(num_categories):
            name = categories_names[i % len(categories_names)]
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'is_active': True}
            )
            categories.append(cat)
        
        self.stdout.write(self.style.SUCCESS(f'Created/Retrieved {len(categories)} categories'))

        # Create authors
        authors = []
        authors_data = [
            {'name': 'María García', 'email': 'maria@example.com'},
            {'name': 'Juan Pérez', 'email': 'juan@example.com'},
            {'name': 'Ana López', 'email': 'ana@example.com'},
            {'name': 'Carlos Rodríguez', 'email': 'carlos@example.com'},
            {'name': 'Laura Martínez', 'email': 'laura@example.com'},
        ]

        for i in range(min(num_authors, len(authors_data))):
            data = authors_data[i]
            author, created = Author.objects.get_or_create(
                email=data['email'],
                defaults={'display_name': data['name']}
            )
            authors.append(author)

        self.stdout.write(self.style.SUCCESS(f'Created/Retrieved {len(authors)} authors'))

        # Create posts
        posts_data = [
            {
                'title': 'Introducción a Django REST Framework',
                'body': 'Django REST Framework es una poderosa herramienta para construir APIs RESTful con Django. En este artículo exploramos los conceptos básicos y cómo comenzar.',
            },
            {
                'title': 'Optimizando consultas con select_related y prefetch_related',
                'body': 'Cuando trabajas con modelos relacionados en Django, es importante optimizar tus consultas para evitar el problema N+1. Aprende cómo usar select_related y prefetch_related.',
            },
            {
                'title': 'Implementando caché con Redis en Django',
                'body': 'Redis es una herramienta excelente para mejorar el rendimiento de tu aplicación Django. Descubre cómo implementar caché efectiva con django-redis.',
            },
            {
                'title': 'Autenticación JWT en aplicaciones modernas',
                'body': 'Los tokens JWT son una forma segura y escalable de manejar autenticación en aplicaciones web modernas. Te mostramos cómo implementarlos correctamente.',
            },
            {
                'title': 'Desarrollo con Docker: Guía completa',
                'body': 'Docker revolucionó el desarrollo de software. Aprende cómo containerizar tus aplicaciones Django y desplegar fácilmente en cualquier ambiente.',
            },
            {
                'title': 'Python vs JavaScript: ¿Cuál elegir?',
                'body': 'Ambos lenguajes son poderosos pero diferentes. Analizamos las fortalezas de cada uno y cuándo usar cada uno según tu proyecto.',
            },
            {
                'title': 'Microservicios: Arquitectura moderna',
                'body': 'Los microservicios ofrecen escalabilidad y mantenibilidad. Explora los patrones de diseño y mejores prácticas para implementar esta arquitectura.',
            },
            {
                'title': 'Testing en Django: TDD práctico',
                'body': 'El Test-Driven Development te ayuda a escribir código más robusto. Aprende a escribir tests efectivos para tus aplicaciones Django.',
            },
            {
                'title': 'Construyendo APIs RESTful con Python',
                'body': 'APIs RESTful son la base de aplicaciones modernas. Conoce los principios y mejores prácticas para diseñar APIs escalables y mantenibles.',
            },
            {
                'title': 'Manejo de errores y logging en producción',
                'body': 'Un buen sistema de logging es crucial para mantener aplicaciones en producción. Aprende a implementar logging estructurado en Django.',
            },
        ]

        posts_created = 0
        statuses = ['published', 'draft']
        
        for i in range(num_posts):
            # Select random author and category
            author = random.choice(authors)
            category = random.choice(categories)
            
            # Choose from sample posts or generate generic ones
            if i < len(posts_data):
                title = posts_data[i]['title']
                body = posts_data[i]['body']
            else:
                title = f'Post de ejemplo #{i+1}'
                body = f'Contenido del post #{i+1}. Este es un post de prueba con contenido generado automáticamente para poblar la base de datos del blog.'
            
            # Randomly set status (80% published, 20% draft)
            status = random.choices(statuses, weights=[80, 20])[0]
            
            # Set published_at if published
            published_at = None
            if status == 'published':
                days_ago = random.randint(0, 60)
                published_at = timezone.now() - timedelta(days=days_ago)
            
            Post.objects.create(
                title=title,
                body=body,
                author=author,
                category=category,
                status=status,
                published_at=published_at,
                views=random.randint(0, 1000) if status == 'published' else 0
            )
            posts_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {posts_created} posts'))

        # Summary
        published_count = Post.objects.filter(status='published').count()
        draft_count = Post.objects.filter(status='draft').count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Blog seeding completed successfully!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Categories: {len(categories)}')
        self.stdout.write(f'Authors: {len(authors)}')
        self.stdout.write(f'Total Posts: {posts_created}')
        self.stdout.write(f'  - Published: {published_count}')
        self.stdout.write(f'  - Drafts: {draft_count}')
        self.stdout.write('='*50)

