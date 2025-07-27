import pytest
import json
from app.models import blog_storage

class TestAPIEndpoints:
    """
    Clase que agrupa todas las pruebas de la API REST (endpoints JSON)
    ¿Por qué probar la API por separado?
    - Diferentes tipos de respuesta (JSON vs HTML)
    - Diferentes casos de uso (apps móviles, integraciones)
    - Diferentes validaciones y manejo de errores
    """

    def test_get_all_posts_success(self, client):
        """
        Test: GET /api/posts devuelve todos los posts en formato JSON
        ¿Qué verifica?
        - Status code 200
        - Respuesta es JSON válido
        - Contiene estructura esperada
        - Incluye posts de ejemplo
        """
        response = client.get('/api/posts')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        # Verificar estructura de respuesta
        assert 'success' in data
        assert 'data' in data
        assert 'count' in data
        assert data['success'] is True
        assert data['count'] == 2  # 2 posts de ejemplo
        # Verificar que cada post tiene la estructura correcta
        for post in data['data']:
            assert 'id' in post
            assert 'title' in post
            assert 'content' in post
            assert 'author' in post
            assert 'created_at' in post
            assert 'summary' in post

    def test_get_single_post_success(self, client):
        """
        Test: GET /api/posts/<id> devuelve un post específico
        """
        response = client.get('/api/posts/1')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['id'] == 1
        assert 'Bienvenido a DevBlog' in data['data']['title']

    def test_get_single_post_not_found(self, client):
        """
        Test: GET /api/posts/<id> con ID inexistente devuelve 404
        CASO EDGE: ID que no existe
        """
        response = client.get('/api/posts/999')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
        assert 'no encontrado' in data['error'].lower()

    def test_create_post_success(self, client):
        """
        Test: POST /api/posts crea un nuevo post correctamente
        ¿Qué verifica?
        - Acepta JSON válido
        - Crea el post en el almacenamiento
        - Devuelve el post creado
        - Status code 201 (Created)
        """
        new_post = {
            'title': 'Post creado via API',
            'content': 'Este post fue creado usando la API REST.\n\nEs muy útil para integraciones.',
            'author': 'API Tester'
        }
        response = client.post('/api/posts',
                               data=json.dumps(new_post),
                               content_type='application/json')
        assert response.status_code == 201
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['title'] == new_post['title']
        assert data['data']['content'] == new_post['content']
        assert data['data']['author'] == new_post['author']
        assert 'id' in data['data']
        # Verificar que el post se guardó realmente
        assert len(blog_storage.get_all_posts()) == 3  # 2 ejemplo + 1 nuevo

    def test_create_post_missing_data(self, client):
        """
        Test: POST /api/posts sin datos requeridos devuelve error
        CASO EDGE: Datos faltantes
        """
        incomplete_post = {
            'title': 'Solo título',
            # Falta 'content'
        }
        response = client.post('/api/posts',
                               data=json.dumps(incomplete_post),
                               content_type='application/json')
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
        assert 'requeridos' in data['error'].lower()

    def test_create_post_no_json(self, client):
        """
        Test: POST /api/posts sin JSON devuelve error
        CASO EDGE: No se envía JSON
        """
        response = client.post('/api/posts')
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'json' in data['error'].lower()

    def test_create_post_invalid_json(self, client):
        """
        Test: POST /api/posts con JSON malformado devuelve error
        CASO EDGE: JSON inválido
        """
        response = client.post('/api/posts',
                               data='{"title": "incomplete json"',
                               content_type='application/json')
        assert response.status_code == 400

    def test_update_post_success(self, client):
        """
        Test: PUT /api/posts/<id> actualiza un post correctamente
        """
        update_data = {
            'title': 'Título actualizado',
            'content': 'Contenido actualizado via API'
        }
        response = client.put('/api/posts/1',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == update_data['title']
        assert data['data']['content'] == update_data['content']
        assert data['data']['id'] == 1
        # Verificar que se actualizó realmente
        updated_post = blog_storage.get_post_by_id(1)
        assert updated_post.title == update_data['title']

    def test_update_post_not_found(self, client):
        """
        Test: PUT /api/posts/<id> con ID inexistente devuelve 404
        CASO EDGE: Actualizar post que no existe
        """
        update_data = {'title': 'No importa'}
        response = client.put('/api/posts/999',
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    def test_delete_post_success(self, client):
        """
        Test: DELETE /api/posts/<id> elimina un post correctamente
        """
        # Verificar que el post existe antes
        assert blog_storage.get_post_by_id(1) is not None
        response = client.delete('/api/posts/1')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'eliminado' in data['message'].lower()
        # Verificar que se eliminó realmente
        assert blog_storage.get_post_by_id(1) is None
        assert len(blog_storage.get_all_posts()) == 1  # Solo queda 1

    def test_delete_post_not_found(self, client):
        """
        Test: DELETE /api/posts/<id> con ID inexistente devuelve 404
        CASO EDGE: Eliminar post que no existe
        """
        response = client.delete('/api/posts/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    def test_search_api_success(self, client):
        """
        Test: GET /api/search?q=término busca posts correctamente
        """
        response = client.get('/api/search?q=Docker')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'query' in data
        assert 'count' in data
        assert data['query'] == 'Docker'
        assert data['count'] >= 1
        # Verificar que los resultados contienen el término buscado
        for post in data['data']:
            assert ('docker' in post['title'].lower() or
                    'docker' in post['content'].lower())

    def test_search_api_no_query(self, client):
        """
        Test: GET /api/search sin parámetro q devuelve error
        CASO EDGE: Búsqueda sin término
        """
        response = client.get('/api/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'requerido' in data['error'].lower()

    def test_search_api_empty_query(self, client):
        """
        Test: GET /api/search?q= (vacío) devuelve error
        CASO EDGE: Término de búsqueda vacío
        """
        response = client.get('/api/search?q=')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_search_api_no_results(self, client):
        """
        Test: GET /api/search con término que no existe
        """
        response = client.get('/api/search?q=TerminoQueNoExiste')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['data']) == 0
# En tests/test_api.py, agregar nuevo test:
def test_health_endpoint(self, client):
    """Test: Health check endpoint works"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['version'] == '1.0.0'
    assert 'timestamp' in data