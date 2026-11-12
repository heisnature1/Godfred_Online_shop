import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured('DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is False.')
    SECRET_KEY = 'django-insecure-local-development-key'

allowed_hosts_raw = os.environ.get('DJANGO_ALLOWED_HOSTS')
allowed_hosts = [h.strip() for h in (allowed_hosts_raw or '').split(',') if h.strip()]

# Render hostname (kept for backward compatibility with existing Render deploys)
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in allowed_hosts:
    allowed_hosts.append(render_hostname)

# Vercel hostnames. Each preview deployment gets its own hostname, so we pick up
# VERCEL_URL and VERCEL_PROJECT_PRODUCTION_URL from the environment automatically.
for _env in ('VERCEL_URL', 'VERCEL_PROJECT_PRODUCTION_URL'):
    _value = os.environ.get(_env)
    if _value:
        _value = _value.replace('https://', '').replace('http://', '').strip().rstrip('/')
        if _value and _value not in allowed_hosts:
            allowed_hosts.append(_value)

if allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts
else:
    ALLOWED_HOSTS = ['*'] if DEBUG else ['127.0.0.1', 'localhost']

# CSRF trusted origins must include every production/preview origin that posts to the site.
_csrf_trusted = []
for _host in ALLOWED_HOSTS:
    if _host in ('*', '127.0.0.1', 'localhost'):
        continue
    _csrf_trusted.append('https://' + _host)
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS')
if env_csrf:
    _csrf_trusted += [h.strip() for h in env_csrf.split(',') if h.strip()]
if _csrf_trusted:
    CSRF_TRUSTED_ORIGINS = _csrf_trusted

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'accounts',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopnow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_count',
                'dashboard.context_processors.dashboard_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopnow.wsgi.application'

database_url = os.environ.get('DATABASE_URL')
if database_url:
    # On serverless platforms (Vercel) each function invocation is short-lived,
    # so persistent connections must be disabled (conn_max_age=0). Django will
    # open a fresh connection per request and reuse it within a single request.
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=0,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ==============================================================================
# SECURITY & COOKIE CONFIGURATION (OWASP Top 10 Hardening)
# ==============================================================================
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'same-origin'

# Session and CSRF cookie protection
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# HTTPS / SSL enforcement in production
_ssl_env = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1')
SECURE_SSL_REDIRECT = (not DEBUG) and _ssl_env
SESSION_COOKIE_SECURE = (not DEBUG) and _ssl_env
CSRF_COOKIE_SECURE = (not DEBUG) and _ssl_env
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HTTP Strict Transport Security (HSTS)
_hsts_env = os.environ.get('DJANGO_SECURE_HSTS', 'False').lower() in ('true', '1')
if (not DEBUG) and _hsts_env:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_HSTS_SECONDS = 0

# Security Event Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}:{lineno}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'accounts.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
