import os
class Config:
    # Clave secreta para sesiones y formularios
    # En producción, esto debería ser una variable de entorno
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-inproduction'
    # Configuración para el modo debug
    # True = muestra errores detallados, recarga automática
    # False = modo producción, más seguro
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    # Puerto donde correrá la aplicación
    PORT = int(os.environ.get('PORT', 5000))
    # Host - 0.0.0.0 permite conexiones externas (necesario para Docker)
    HOST = os.environ.get('HOST', '0.0.0.0')