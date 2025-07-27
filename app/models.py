from datetime import datetime
from typing import List, Dict, Optional


class BlogPost:
    def __init__(self, title: str, content: str, author: str = "Admin"):
        """
        Constructor del post
        """
        self.id = None  # Se asignará automáticamente
        self.title = title.strip()  # Elimina espacios extra
        self.content = content.strip()
        self.author = author.strip()
        self.created_at = datetime.now()
        # Fecha de creación automática
        self.updated_at = datetime.now()  # Fecha de última actualización

    def to_dict(self) -> Dict:
        """
        Convierte el post a diccionario para JSON/API
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            # Resumen para la lista de posts (primeros 150 caracteres)
            'summary': self.content[:150] + '...' if len(self.content) > 150
            else self.content
        }

    def update(self, title: str = None, content: str = None):
        """
        Actualiza el post con nuevos datos
        """
        if title:
            self.title = title.strip()
        if content:
            self.content = content.strip()
            self.updated_at = datetime.now()  # Actualiza timestamp


class BlogStorage:
    """
    Clase para manejar el almacenamiento de posts
    En producción real usarías PostgreSQL, MySQL, etc.
    """

    def __init__(self):
        """Inicializa el almacenamiento con algunos posts de ejemplo"""
        self._posts: List[BlogPost] = []
        self._next_id = 1
        # Crear algunos posts de ejemplo para que el blog no esté vacío
        self._create_sample_posts()

    def _create_sample_posts(self):
        """Crea posts de ejemplo para demostración"""
        sample_posts = [
            {
                'title': '¡Bienvenido a DevBlog!',
                'content': '''Este es mi primer post en DevBlog, una 
                aplicación creada para aprender DevOps y CI/CD.

                En este blog compartiré mi experiencia aprendiendo:
                - Desarrollo web con Flask
                - Containerización con Docker 
                - Testing automatizado
                - CI/CD con GitHub Actions
                - Despliegue en la nube

                ¡Espero que disfrutes leyendo tanto como yo disfruto 
                escribiendo!''',
                'author': 'DevOps Student'
            },
            {
                'title': 'Mi experiencia con Docker',
                'content': '''Docker ha sido una revelación en mi 
                aprendizaje de DevOps. 

                La capacidad de empaquetar una aplicación con todas sus 
                dependencias en un contenedor portable es increíble.
                Ya no más "en mi máquina funciona" 

                Algunos beneficios que he descubierto:
                - Consistencia entre entornos
                - Fácil escalabilidad
                - Aislamiento de aplicaciones
                - Despliegues más confiables

                ¿Cuál ha sido tu experiencia con Docker?''',
                                'author': 'DevOps Student'
            }
        ]
        
        for post_data in sample_posts:
            post = BlogPost(
                title=post_data['title'],
                content=post_data['content'],
                author=post_data['author']
            )
            self.create_post(post)

    def create_post(self, post: BlogPost) -> BlogPost:
        """
        Crea un nuevo post
        Args:
            post: Instancia de BlogPost
        Returns:
            El post creado con ID asignado
        """
        post.id = self._next_id
        self._next_id += 1
        self._posts.append(post)
        return post

    def get_all_posts(self) -> List[BlogPost]:
        """
        Obtiene todos los posts ordenados por fecha (más recientes primero)
        Returns:
            Lista de posts ordenada
        """
        return sorted(self._posts, key=lambda x: x.created_at, reverse=True)

    def get_post_by_id(self, post_id: int) -> Optional[BlogPost]:
        """
        Busca un post por su ID
        Args:
            post_id: ID del post a buscar
        Returns:
            El post si existe, None si no existe
        """
        for post in self._posts:
            if post.id == post_id:
                return post
        return None

    def update_post(self, post_id: int, title: str = None, content: str = None) -> Optional[BlogPost]:
        """
        Actualiza un post existente
        Args:
            post_id: ID del post a actualizar
            title: Nuevo título (opcional)
            content: Nuevo contenido (opcional)
        Returns:
            El post actualizado o None si no existe
        """
        post = self.get_post_by_id(post_id)
        if post:
            post.update(title, content)
            return post
        return None

    def delete_post(self, post_id: int) -> bool:
        """
        Elimina un post
        Args:
            post_id: ID del post a eliminar
        Returns:
            True si se eliminó, False si no existía
        """
        post = self.get_post_by_id(post_id)
        if post:
            self._posts.remove(post)
            return True
        return False

    def search_posts(self, query: str) -> List[BlogPost]:
        """
        Busca posts que contengan la query en título o contenido
        Args:
            query: Término de búsqueda
        Returns:
            Lista de posts que coinciden con la búsqueda
        """
        query = query.lower().strip()
        if not query:
            return self.get_all_posts()
        
        results = []
        for post in self._posts:
            # Busca en título y contenido (case-insensitive)
            if (query in post.title.lower() or
                query in post.content.lower()):
                results.append(post)
        
        # Ordena por relevancia (título primero, luego por fecha)
        results.sort(key=lambda x: (
            query not in x.title.lower(),  # Título tiene prioridad
            -x.created_at.timestamp()  # Luego por fecha reciente
        ))
        return results


# Instancia global del almacenamiento
# En una aplicación real, esto sería inyectado como dependencia
blog_storage = BlogStorage()