"""
Django settings for financeiro project - DESENVOLVIMENTO LOCAL

IMPORTANTE: Este arquivo é para ambiente de DESENVOLVIMENTO.
Para produção no PythonAnywhere, use settings_2.py (renomeie para settings.py)
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA - PRODUÇÃO
# ==============================================================================

SECRET_KEY = 'django-insecure-dev-key-mude-em-producao-12345'

# DEBUG ativo em desenvolvimento
DEBUG = True

# ALLOWED_HOSTS para desenvolvimento local
ALLOWED_HOSTS = []

# Exemplo de uso com variável de ambiente no PythonAnywhere:
# No arquivo .bashrc ou direto no WSGI:
# export ALLOWED_HOSTS='seuusername.pythonanywhere.com,www.seudominio.com.br'


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "login",
    "dashboard",
    "contas_pagar",
    "contas_receber",
    "empresa",
    "investimento",
    "assinatura",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'financeiro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'financeiro.wsgi.application'


# ==============================================================================
# DATABASE - PRODUÇÃO
# ==============================================================================

# OPÇÃO 1: SQLite (mais simples, recomendado para pequenos projetos)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# OPÇÃO 2: MySQL no PythonAnywhere (descomente se quiser usar)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'seuusername$financeiro',  # <- ALTERE aqui!
#         'USER': 'seuusername',              # <- ALTERE aqui!
#         'PASSWORD': 'sua-senha-mysql',      # <- ALTERE aqui!
#         'HOST': 'seuusername.mysql.pythonanywhere-services.com',  # <- ALTERE aqui!
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ==============================================================================
# STATIC FILES (CSS, JavaScript, Images) - DESENVOLVIMENTO
# ==============================================================================

STATIC_URL = '/static/'

# Para desenvolvimento, o Django serve arquivos estáticos automaticamente
# STATIC_ROOT é usado apenas em produção (collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Arquivos estáticos adicionais (PWA: manifest.json, service-worker.js, icons, etc)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# ==============================================================================
# MEDIA FILES (Uploads de usuários) - Se usar no futuro
# ==============================================================================

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# SEGURANÇA ADICIONAL - DESENVOLVIMENTO
# ==============================================================================

# Em desenvolvimento, cookies não precisam ser secure
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Proteção contra clickjacking
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Força HTTPS - Desabilitado em desenvolvimento
SECURE_SSL_REDIRECT = False


# ==============================================================================
# AUTENTICAÇÃO
# ==============================================================================

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"


# ==============================================================================
# ADMIN CUSTOMIZATION (Jazzmin)
# ==============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "Financeiro - Admin",
    "site_header": "Administração do Sistema Financeiro",
    "welcome_sign": "Bem-vindo ao Painel Administrativo",
    "copyright": "Sistema Financeiro © 2026",
    "show_ui_builder": True,  # Ativo em desenvolvimento
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "footer_fixed": False,
}


# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
