import pytest
from app import create_app
from app.models import blog_storage

@pytest.fixture
def app():
    """
    Fixture que crea una instancia de la aplicación para testing
    ¿Qué es un fixture?
    - Función que prepara datos/objetos para las pruebas
    - Se ejecuta antes de cada test que lo necesite
    - Garantiza un estado limpio para cada prueba
    """
    # Crear aplicación en modo testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para testing
    return app

@pytest.fixture
def client(app):
    """
    Fixture que crea un cliente de testing para hacer peticiones HTTP
    ¿Para qué sirve?
    - Simula un navegador web
    - Permite hacer GET, POST, PUT, DELETE
    - No necesita servidor real corriendo
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Fixture para testing de comandos CLI (si los tuviéramos)
    """
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def reset_storage():
    """
    Fixture que resetea el almacenamiento antes de cada test
    ¿Por qué autouse=True?
    - Se ejecuta automáticamente antes de cada test
    - Garantiza que cada test empiece con datos limpios
    - Evita que los tests se afecten entre sí
    """
    # Limpiar todos los posts
    blog_storage._posts.clear()
    blog_storage._next_id = 1
    # Recrear posts de ejemplo para tests consistentes
    blog_storage._create_sample_posts()
    yield  # Aquí se ejecuta el test
    # Cleanup después del test (si fuera necesario)
    pass
