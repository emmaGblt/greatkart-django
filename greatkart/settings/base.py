from django.contrib.messages import constants as messages
from pathlib import Path

from configurations import Configuration, values


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Base(Configuration):
    SECRET_KEY = values.Value(environ_required=True)

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "category",
        "accounts",
        "store",
        "carts",
        "orders",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "greatkart.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "category.context_processors.categories",
                    "carts.context_processors.cart_items_count",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "greatkart.wsgi.application"

    AUTH_USER_MODEL = "accounts.Account"

    # Password validation
    # https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/6.0/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images) configuration
    # https://docs.djangoproject.com/en/6.0/howto/static-files/

    STATIC_URL = "static/"
    STATIC_ROOT = BASE_DIR / "static"
    STATICFILES_DIRS = [
        "greatkart/static",
    ]

    # Media files configuration
    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"

    # Messages configuration
    MESSAGE_TAGS = {
        messages.ERROR: "danger",
    }

    # Email configuration
    # from dotenv import load_dotenv
    # import os

    # load_dotenv()

    # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" # Too much security on my Gmail address
    # EMAIL_HOST = "smtp.gmail.com"
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    # EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    # EMAIL_USE_TLS = True
    # EMAIL_USE_SSL = False
