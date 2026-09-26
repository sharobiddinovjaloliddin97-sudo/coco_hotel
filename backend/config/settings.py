"""
Django settings for config project.

Production-oriented configuration utilizing django-environ.
"""

from pathlib import Path
import environ
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
    CORS_ALLOWED_ORIGINS=(list, ['http://localhost:5173']),
    CSRF_TRUSTED_ORIGINS=(list, ['http://localhost:5173']),
)

# Read .env file if present in BASE_DIR (or project root)
environ.Env.read_env(BASE_DIR / '.env')
environ.Env.read_env(BASE_DIR.parent / '.env')

# Quick-start development settings - unsuitable for production
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-fallback-key-do-not-use-in-production')

DEBUG = env('DEBUG')
if not DEBUG and (SECRET_KEY.startswith('django-insecure-') or len(SECRET_KEY) < 50):
    raise ImproperlyConfigured('Set a strong SECRET_KEY of at least 50 characters for production.')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)

ALLOWED_HOSTS = env('ALLOWED_HOSTS')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    # Local apps
    'core',
    'rooms',
    'hotel',
    'bookings',
    'guest_requests',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Production PostgreSQL configuration powered by Neon. Requires DATABASE_URL in environment.

DATABASES = {
    'default': env.db('DATABASE_URL'),
}



# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': (
        'django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG
        else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    )},
}

# Media files (uploaded room images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS Configuration

CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)



# Django REST Framework Base Configuration

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'booking_submission': env('BOOKING_THROTTLE_RATE', default='5/minute'),
        'callback_submission': env('CALLBACK_THROTTLE_RATE', default='5/minute'),
        'contact_submission': env('CONTACT_THROTTLE_RATE', default='5/minute'),
    },
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer'
    )


# Public hotel photography is uploaded by authenticated Django Admin staff only.
MEDIA_STORAGE = env('MEDIA_STORAGE', default='local')
if MEDIA_STORAGE == 'supabase':
    SUPABASE_PUBLIC_MEDIA_URL = env('SUPABASE_PUBLIC_MEDIA_URL')
    STORAGES['default'] = {
        'BACKEND': 'core.storage.SupabaseMediaStorage',
        'OPTIONS': {
            'access_key': env('SUPABASE_S3_ACCESS_KEY_ID'),
            'secret_key': env('SUPABASE_S3_SECRET_ACCESS_KEY'),
            'endpoint_url': env('SUPABASE_S3_ENDPOINT_URL'),
            'region_name': env('SUPABASE_S3_REGION'),
            'bucket_name': env('SUPABASE_STORAGE_BUCKET'),
            'addressing_style': 'path',
            'signature_version': 's3v4',
            'default_acl': None,
            'file_overwrite': False,
            'querystring_auth': False,
        },
    }
elif MEDIA_STORAGE != 'local':
    raise ImproperlyConfigured('MEDIA_STORAGE must be local or supabase.')

# Optional shared rate-limit cache across production workers.
REDIS_URL = env('REDIS_URL', default='')
if REDIS_URL:
    CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'KEY_PREFIX': 'coco-hotel',
    }}

# Gemini AI API Key for Coco AI Concierge
GEMINI_API_KEY = env('GEMINI_API_KEY', default='')

