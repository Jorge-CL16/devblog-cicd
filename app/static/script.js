/* ================================
FUNCIONES DE INICIALIZACIÓN
================================ */
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    console.log('DevBlog inicializado correctamente');
    initializeTooltips();
    initializeFormValidation();
    initializeSearchEnhancements();
    initializeAnimations();
}

/* ================================
TOOLTIPS Y UI ENHANCEMENTS
================================ */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* ================================
VALIDACIÓN DE FORMULARIOS
================================ */
function initializeFormValidation() {
    const createPostForm = document.querySelector('form[action*="create"]');
    if (createPostForm) {
        const titleInput = document.getElementById('title');
        const contentTextarea = document.getElementById('content');

        if (titleInput) {
            titleInput.addEventListener('input', function () {
                validateTitle(this);
                updateCharacterCount('title', 200);
            });
        }

        if (contentTextarea) {
            contentTextarea.addEventListener('input', function () {
                validateContent(this);
                updateWordCount('content');
            });
        }

        createPostForm.addEventListener('submit', function (e) {
            if (!validateForm()) {
                e.preventDefault();
                showAlert('Por favor corrige los errores antes de continuar', 'danger');
            }
        });
    }
}

function validateTitle(input) {
    const title = input.value.trim();
    const feedback = input.parentNode.querySelector('.invalid-feedback') || createFeedbackElement(input);

    if (title.length === 0) {
        setInputState(input, false, 'El título es requerido');
    } else if (title.length > 200) {
        setInputState(input, false, 'El título no puede tener más de 200 caracteres');
    } else if (title.length < 5) {
        setInputState(input, false, 'El título debe tener al menos 5 caracteres');
    } else {
        setInputState(input, true, '¡Título válido!');
    }
}

function validateContent(textarea) {
    const content = textarea.value.trim();
    if (content.length === 0) {
        setInputState(textarea, false, 'El contenido es requerido');
    } else if (content.length < 10) {
        setInputState(textarea, false, 'El contenido debe tener al menos 10 caracteres');
    } else {
        setInputState(textarea, true, '¡Contenido válido!');
    }
}

function setInputState(input, isValid, message) {
    input.classList.remove('is-valid', 'is-invalid');
    input.classList.add(isValid ? 'is-valid' : 'is-invalid');

    let feedback = input.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (!feedback) {
        feedback = createFeedbackElement(input);
    }

    feedback.className = isValid ? 'valid-feedback' : 'invalid-feedback';
    feedback.textContent = message;
}

function createFeedbackElement(input) {
    const feedback = document.createElement('div');
    input.parentNode.appendChild(feedback);
    return feedback;
}

function validateForm() {
    const titleInput = document.getElementById('title');
    const contentTextarea = document.getElementById('content');
    let isValid = true;

    if (titleInput) {
        validateTitle(titleInput);
        if (titleInput.classList.contains('is-invalid')) {
            isValid = false;
        }
    }

    if (contentTextarea) {
        validateContent(contentTextarea);
        if (contentTextarea.classList.contains('is-invalid')) {
            isValid = false;
        }
    }

    return isValid;
}

/* ================================
CONTADORES DE CARACTERES/PALABRAS
================================ */
function updateCharacterCount(inputId, maxLength) {
    const input = document.getElementById(inputId);
    const currentLength = input.value.length;
    let counter = document.getElementById(inputId + '-counter');

    if (!counter) {
        counter = document.createElement('small');
        counter.id = inputId + '-counter';
        counter.className = 'form-text';
        input.parentNode.appendChild(counter);
    }

    counter.textContent = `${currentLength}/${maxLength} caracteres`;
    counter.style.color = currentLength > maxLength ? '#dc3545' : '#6c757d';
}

function updateWordCount(textareaId) {
    const textarea = document.getElementById(textareaId);
    const words = textarea.value.trim().split(/\s+/).filter(word => word.length > 0);
    const wordCount = words.length;
    let counter = document.getElementById(textareaId + '-word-counter');

    if (!counter) {
        counter = document.createElement('small');
        counter.id = textareaId + '-word-counter';
        counter.className = 'form-text';
        textarea.parentNode.appendChild(counter);
    }

    const readingTime = Math.ceil(wordCount / 200);
    counter.textContent = `${wordCount} palabras • ~${readingTime} min de lectura`;
}

/* ================================
MEJORAS DE BÚSQUEDA
================================ */
function initializeSearchEnhancements() {
    const searchInputs = document.querySelectorAll('input[name="q"]');

    searchInputs.forEach(input => {
        input.addEventListener('input', function () {
            debounce(handleSearchInput, 300)(this);
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                this.value = '';
                this.blur();
            }
        });
    });
}

function handleSearchInput(input) {
    const query = input.value.trim();
    if (query.length > 2) {
        saveSearchQuery(query);
    }
}

function saveSearchQuery(query) {
    let searches = JSON.parse(localStorage.getItem('devblog-searches') || '[]');
    searches = [query, ...searches.filter(s => s !== query)].slice(0, 10);
    localStorage.setItem('devblog-searches', JSON.stringify(searches));
}

/* ================================
ANIMACIONES Y EFECTOS
================================ */
function initializeAnimations() {
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => {
        observer.observe(card);
    });
}

/* ================================
UTILIDADES
================================ */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.insertBefore(alert, alertContainer.firstChild);

    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('¡Copiado al portapapeles!', 'success');
    }).catch(() => {
        showAlert('Error al copiar al portapapeles', 'danger');
    });
}

/* ================================
FUNCIONES GLOBALES EXPORTADAS
================================ */
window.sharePost = function () {
    const title = document.querySelector('h1').textContent;
    const url = window.location.href;

    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch(console.error);
    } else {
        copyToClipboard(url);
    }
};

window.previewPost = function () {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const author = document.getElementById('author').value || 'Anónimo';

    if (!title || !content) {
        showAlert('Por favor completa el título y contenido antes de la vista previa.', 'warning');
        return;
    }

    const previewWindow = window.open('', '_blank', 'width=800,height=600');
    const previewContent = `
<!DOCTYPE html>
<html>
<head>
    <title>Vista Previa - ${title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .content p { margin-bottom: 1.5rem; line-height: 1.8; }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="card">
            <div class="card-body">
                <h1>${title}</h1>
                <div class="text-muted mb-3">
                    <small>Por: ${author} • ${new Date().toLocaleDateString()}</small>
                </div>
                <div class="content">
                    ${content.split('\n\n').map(p => p.trim() ? `<p>${p.replace(/\n/g, '<br>')}</p>` : '').join('')}
                </div>
            </div>
        </div>
        <div class="mt-3">
            <button class="btn btn-secondary" onclick="window.close()">Cerrar Vista Previa</button>
        </div>
    </div>
</body>
</html>
    `;
    previewWindow.document.write(previewContent);
    previewWindow.document.close();
};

console.log('📱 DevBlog JavaScript cargado correctamente');
