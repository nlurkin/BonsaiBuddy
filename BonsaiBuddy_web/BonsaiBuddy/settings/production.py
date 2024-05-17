import os
import urllib

import mongoengine

from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG") == "TRUE"

EXTERNAL_HOSTNAME = os.environ.get("EXTERNAL_HOSTNAME")
if EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(EXTERNAL_HOSTNAME)

MIDDLEWARE = [
    "BonsaiBuddy.middleware.HealthCheckMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

MONGO_USER = os.environ["DJANGO_MONGO_USER"]
MONGO_PASS = urllib.parse.quote(os.environ["DJANGO_MONGO_PASS"])
MONGO_HOST = os.environ["DJANGO_MONGO_HOST"]
MONGO_NAME = os.environ["DJANGO_MONGO_NAME"]
MONGO_DATABASE_HOST = "mongodb+srv://%s:%s@%s/%s?ssl=true" % (
    MONGO_USER,
    MONGO_PASS,
    MONGO_HOST,
    MONGO_NAME,
)
mongoengine.connect(host=MONGO_DATABASE_HOST, alias="mongo")

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
