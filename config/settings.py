"""
SETTINGS.PY - Configurações do Django para produção (Railway, Vercel)

- INSTALLED_APPS: registra apps do projeto e bibliotecas externas
- DATABASES: SQLite para teste ou PostgreSQL para produção
- DEBUG: False em produção
- CORS: permite front acessar API
- CSRF_TRUSTED_ORIGINS: evita erro 403 no /admin
- ALLOWED_HOSTS: domínios permitidos
"""

from pathlib import Path
import os
import dj_database_url  # >>> NOVO <<<

# -------------------------------
# BASE DIR
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# SECRET KEY
# -------------------------------
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-streamflix-2024-mudar-em-producao'
)

# -------------------------------
# DEBUG
# -------------------------------
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# -------------------------------
# HOSTS PERMITIDOS
# -------------------------------
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',    # Railway
    '.herokuapp.com',  # Heroku, se necessário
    '.onrender.com',   # Render, se necessário
]

# -------------------------------
# APPS
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'movies',
    'reviews',
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# URL CONFIG
# -------------------------------
ROOT_URLCONF = 'config.urls'

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------------
# WSGI
# -------------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# -------------------------------
# DATABASE
# -------------------------------
# Usa PostgreSQL no Railway e SQLite local como fallback
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=True
    )
}

# -------------------------------
# PASSWORD VALIDATORS
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# -------------------------------
# LOCALIZAÇÃO
# -------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -------------------------------
# AUTO FIELD
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# CORS
# -------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# -------------------------------
# CSRF
# -------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-a155e.up.railway.app',
]

# -------------------------------
# REST FRAMEWORK
# -------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
