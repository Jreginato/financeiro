"""
Django settings for financeiro project - PRODUÇÃO (PythonAnywhere)

IMPORTANTE: Este arquivo é para ambiente de PRODUÇÃO no PythonAnywhere.
Para desenvolvimento local, use settings.py

Para usar este arquivo no PythonAnywhere:
1. No arquivo wsgi.py, altere:
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financeiro.settings_2')
   
2. Configure as variáveis abaixo conforme seu ambiente
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA - PRODUÇÃO
# ==============================================================================

# ATENÇÃO: Configure a SECRET_KEY
# OPÇÃO 1: Defina a variável de ambiente DJANGO_SECRET_KEY (recomendado)
# OPÇÃO 2: Edite diretamente aqui (menos seguro)
# Use: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'ALTERE-ESTA-CHAVE-PARA-UMA-CHAVE-SECRETA-UNICA-E-ALEATORIA'
)

# DEBUG deve ser False em produção!
DEBUG = False

# ATENÇÃO: Configure o ALLOWED_HOSTS
# OPÇÃO 1: Defina a variável de ambiente ALLOWED_HOSTS
# OPÇÃO 2: Edite diretamente aqui (menos flexível)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'jreginato.pythonanywhere.com').split(',')

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
    "contas_pagar",
    "contas_receber",
    "empresa"
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
# STATIC FILES (CSS, JavaScript, Images) - PRODUÇÃO
# ==============================================================================

STATIC_URL = '/static/'

# IMPORTANTE: No PythonAnywhere, após fazer deploy:
# 1. Execute: python manage.py collectstatic --settings=financeiro.settings_2
# 2. Configure o mapeamento estático na aba "Web":
#    URL: /static/
#    Directory: /home/seuusername/financeiro/staticfiles
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Se tiver arquivos estáticos adicionais fora dos apps
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]


# ==============================================================================
# MEDIA FILES (Uploads de usuários) - Se usar no futuro
# ==============================================================================

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# SEGURANÇA ADICIONAL - PRODUÇÃO
# ==============================================================================

# Cookies de sessão seguros
SESSION_COOKIE_SECURE = True  # Apenas HTTPS
CSRF_COOKIE_SECURE = True     # Apenas HTTPS

# Proteção contra clickjacking
X_FRAME_OPTIONS = 'DENY'

# Força HTTPS
SECURE_SSL_REDIRECT = False  # PythonAnywhere já faz isso, deixe False

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proteção contra XSS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# ==============================================================================
# AUTENTICAÇÃO
# ==============================================================================

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "contas_pagar_lista"


# ==============================================================================
# ADMIN CUSTOMIZATION (Jazzmin)
# ==============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "Financeiro - Admin",
    "site_header": "Administração do Sistema Financeiro",
    "welcome_sign": "Bem-vindo ao Painel Administrativo",
    "copyright": "Sistema Financeiro © 2026",
    "show_ui_builder": False,  # Desabilitado em produção
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "footer_fixed": False,
}


# ==============================================================================
# LOGGING - PRODUÇÃO
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
