from .base import Base, BASE_DIR


class Dev(Base):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-p23nt6)t$rkazp!%6$ce26nunet%46valma##pxh&7we!0phs!"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    # Database
    # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
