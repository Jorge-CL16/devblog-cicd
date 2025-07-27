from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models import blog_storage, BlogPost

# Crear un Blueprint para organizar las rutas
main = Blueprint('main', __name__)

# ================================
# RUTAS PARA PÁGINAS WEB (HTML)
# ================================

@main.route('/')
def index():
    """
    Página principal - Lista todos los posts del blog
    """
    posts = blog_storage.get_all_posts()
    return render_template('index.html', posts=posts, title='DevBlog - Mi Blog Personal')

@main.route('/post/<int:post_id>')
def view_post(post_id):
    """
    Vista individual de un post
    Args:
        post_id: ID del post a mostrar (viene de la URL)
    """
    post = blog_storage.get_post_by_id(post_id)
    if not post:
        return render_template('404.html'), 404
    return render_template('post.html', post=post, title=f'{post.title} - DevBlog')

@main.route('/create', methods=['GET', 'POST'])
def create_post():
    """
    Crear nuevo post - Maneja tanto GET (mostrar formulario) como POST (procesar formulario)
    """
    if request.method == 'GET':
        return render_template('create_post.html', title='Crear Nuevo Post - DevBlog')

    elif request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', 'Anónimo').strip()

        errors = []
        if not title:
            errors.append('El título es requerido')
        if not content:
            errors.append('El contenido es requerido')
        if len(title) > 200:
            errors.append('El título no puede tener más de 200 caracteres')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_post.html', 
                                   title='Crear Nuevo Post - DevBlog',
                                   form_data={'title': title, 'content': content, 'author': author})

        try:
            new_post = BlogPost(title=title, content=content, author=author)
            created_post = blog_storage.create_post(new_post)
            flash('¡Post creado exitosamente!', 'success')
            return redirect(url_for('main.view_post', post_id=created_post.id))
        except Exception as e:
            flash(f'Error al crear el post: {str(e)}', 'error')
            return render_template('create_post.html', 
                                   title='Crear Nuevo Post - DevBlog',
                                   form_data={'title': title, 'content': content, 'author': author})

@main.route('/search')
def search():
    """
    Búsqueda de posts
    """
    query = request.args.get('q', '').strip()
    if query:
        results = blog_storage.search_posts(query)
        message = f'Resultados para: "{query}"' if results else f'No se encontraron resultados para: "{query}"'
    else:
        results = []
        message = 'Ingresa un término de búsqueda'
    return render_template('search.html', 
                           posts=results, 
                           query=query, 
                           message=message,
                           title=f'Búsqueda: {query}' if query else 'Búsqueda - DevBlog')

# ================================
# API REST ENDPOINTS (JSON)
# ================================

@main.route('/api/posts', methods=['GET'])
def api_get_posts():
    posts = blog_storage.get_all_posts()
    return jsonify({
        'success': True,
        'data': [post.to_dict() for post in posts],
        'count': len(posts)
    })

@main.route('/api/posts', methods=['POST'])
def api_create_post():
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type debe ser application/json'
        }), 400

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({
            'success': False,
            'error': 'JSON malformado'
        }), 400

    if not data:
        return jsonify({
            'success': False,
            'error': 'No se proporcionaron datos JSON válidos'
        }), 400

    try:
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        author = data.get('author', 'API User').strip()

        if not title or not content:
            return jsonify({
                'success': False,
                'error': 'Título y contenido son requeridos'
            }), 400

        new_post = BlogPost(title=title, content=content, author=author)
        created_post = blog_storage.create_post(new_post)

        return jsonify({
            'success': True,
            'data': created_post.to_dict(),
            'message': 'Post creado exitosamente'
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@main.route('/api/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
    post = blog_storage.get_post_by_id(post_id)
    if not post:
        return jsonify({
            'success': False,
            'error': 'Post no encontrado'
        }), 404
    return jsonify({
        'success': True,
        'data': post.to_dict()
    })

@main.route('/api/posts/<int:post_id>', methods=['PUT'])
def api_update_post(post_id):
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos JSON válidos'
            }), 400

        updated_post = blog_storage.update_post(
            post_id,
            title=data.get('title'),
            content=data.get('content')
        )
        if not updated_post:
            return jsonify({
                'success': False,
                'error': 'Post no encontrado'
            }), 404

        return jsonify({
            'success': True,
            'data': updated_post.to_dict(),
            'message': 'Post actualizado exitosamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@main.route('/api/posts/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    success = blog_storage.delete_post(post_id)
    if not success:
        return jsonify({
            'success': False,
            'error': 'Post no encontrado'
        }), 404
    return jsonify({
        'success': True,
        'message': 'Post eliminado exitosamente'
    })

@main.route('/api/search', methods=['GET'])
def api_search_posts():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({
            'success': False,
            'error': 'Parámetro de búsqueda "q" es requerido'
        }), 400
    results = blog_storage.search_posts(query)
    return jsonify({
        'success': True,
        'data': [post.to_dict() for post in results],
        'query': query,
        'count': len(results)
    })
