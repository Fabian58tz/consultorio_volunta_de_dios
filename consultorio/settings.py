
from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-oi_ca42)^&oux09of@l&ab=^2y2d@vd!f+=@lv!f4rt*qg=7l!'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-oi_ca42)^&oux09of@l&ab=^2y2d@vd!f+=@lv!f4rt*qg=7l!')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []

DEBUG = 'RENDER' not in os.environ

# Permitir el dominio que te asigne Render
ALLOWED_HOSTS = []
render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)
else:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'api_rest',
    'volunta_de_dios',
    'whitenoise.runserver_nostatic',
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

ROOT_URLCONF = 'consultorio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'consultorio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
    #}
#}
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}
#DATABASES = {
    #'default': {
       # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
       # 'NAME': 'base_proyectoppi',
       # 'USER': 'postgres',
        #'PASSWORD':'12345',
        #'HOST':'localhost',
        #'POST': '5432',
        #'ATOMIC_REQUESTS':True,
    #}
#}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
# Carpeta donde se reunirán los archivos en Render
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# WhiteNoise optimiza el almacenamiento de estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de URLs de redirección para autenticación
LOGIN_REDIRECT_URL = 'paguina_principal' # Redirige aquí después de un login exitoso
LOGOUT_REDIRECT_URL = 'login_page'       # Redirige aquí después de un logout exitoso

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    # Usar permisos por defecto: Solo usuarios autenticados pueden ver la API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Métodos de autenticación: Sesión (navegador) y Token (para apps móviles/externas)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    # Paginación profesional (para que no cargue 10,000 pacientes de golpe)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10  # Muestra 10 registros por página
}