# Dockerfile
# ================================
# ETAPA 1: IMAGEN BASE
# ================================
# Usar Python 3.11 slim como imagen base
# ¿Por qué Python 3.11-slim?
# - Versión estable y moderna de Python
# - "slim" = imagen más pequeña (sin herramientas innecesarias)
# - Reduce el tamaño final del contenedor
FROM python:3.11-slim
# ================================
# ETAPA 2: METADATOS
# ================================
# Información sobre la imagen (buenas prácticas)
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="DevBlog - Aplicación de blog para aprender DevOps"
LABEL version="1.0"
# ================================
# ETAPA 3: CONFIGURACIÓN DEL SISTEMA
# ================================
# Establecer variables de entorno
# PYTHONUNBUFFERED=1: Hace que Python muestre logs en tiempo real
# PYTHONDONTWRITEBYTECODE=1: Evita crear archivos .pyc (optimización)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Establecer el directorio de trabajo dentro del contenedor
# Todo el código de la aplicación estará en /app
WORKDIR /app
# ================================
# ETAPA 4: INSTALACIÓN DE DEPENDENCIAS
# ================================
# Copiar requirements.txt PRIMERO (optimización de Docker layers)
# ¿Por qué copiar requirements.txt antes que el resto del código?
# - Docker usa capas (layers) para optimizar builds
# - Si solo cambia el código, no necesita reinstalar dependencias
# - Esto hace los builds mucho más rápidos
COPY requirements.txt .
# Actualizar pip y instalar dependencias
# --no-cache-dir: No guarda cache de pip (imagen más pequeña)
# --upgrade: Asegura que pip esté actualizado
RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt
# ================================
# ETAPA 5: COPIAR CÓDIGO DE LA APLICACIÓN
# ================================
# Copiar todo el código de la aplicación al contenedor
# El . significa "todo en el directorio actual"
# Se copia al directorio /app (definido en WORKDIR)
COPY . .
# ================================
# ETAPA 6: CONFIGURACIÓN DE USUARIO
# ================================
# Crear un usuario no-root para seguridad
# ¿Por qué no usar root?
# - Principio de menor privilegio
# - Si alguien compromete el contenedor, no tiene acceso root
# - Buena práctica de seguridad
RUN adduser --disabled-password --gecos '' appuser && \
chown -R appuser:appuser /app
USER appuser
# ================================
# ETAPA 7: CONFIGURACIÓN DE RED
# ================================
# Exponer el puerto 5000 (puerto por defecto de Flask)
# Esto es documentativo - le dice a otros desarrolladores qué puerto usar
# No abre automáticamente el puerto (eso se hace al ejecutar el contenedor)
EXPOSE 5000
# ================================
# ETAPA 8: COMANDO DE INICIO
# ================================
# Comando que se ejecuta cuando inicia el contenedor
# Inicia la aplicación Flask
CMD ["python", "app.py"]