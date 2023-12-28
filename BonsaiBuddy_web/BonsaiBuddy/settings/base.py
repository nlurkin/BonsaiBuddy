"""
Django settings for BonsaiBuddy project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.forms.renderers import TemplatesSetting

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'debug_toolbar',
    'TreeInfo.apps.TreeinfoConfig',
    'BonsaiAdmin.apps.BonsaiadminConfig',
    'BonsaiAdvice.apps.BonsaiadviceConfig',
    'BonsaiUsers.apps.BonsaiusersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'bootstrap5',
    'widget_tweaks',
    'rest_framework',
    'rest_framework_mongoengine',
]


class CustomFormRenderer(TemplatesSetting):
    form_template_name = "form_template.html"


# FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
FORM_RENDERER = "BonsaiBuddy.settings.base.CustomFormRenderer"

ROOT_URLCONF = 'BonsaiBuddy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "BonsaiBuddy/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'markdown': 'BonsaiBuddy.templatetags.markdown',
                'tablify': 'BonsaiBuddy.templatetags.tablify'
            }
        },
    },
]

WSGI_APPLICATION = 'BonsaiBuddy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "BonsaiBuddy" / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/TreeInfo'
LOGOUT_REDIRECT_URL = '/TreeInfo'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', "BonsaiUsers.auth.DjangoBackend"]

AUTH_USER_MODEL = "BonsaiUsers.User"
