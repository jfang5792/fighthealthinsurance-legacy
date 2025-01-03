"""
Django settings for pigscanfly project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import re
import traceback
from functools import cached_property

from configurations import Configuration
from fighthealthinsurance.combined_storage import CombinedStorage
import minio as m
from django.core.files.storage import Storage
from minio_storage.storage import MinioStorage
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fighthealthinsurance.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv("ENVIRONMENT", "Dev"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Base(Configuration):
    COOKIE_CONSENT_ENABLED = True
    COOKIE_CONSENT_LOG_ENABLED = True
    LOGIN_URL = "login"
    LOGIN_REDIRECT_URL = "/"
    THUMBNAIL_DEBUG = True

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-4b6t3cnic_(g*0cexqe8w)=1&vyb#(erhad#7@y4sv)jzb2kaf"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    MEDIA_ROOT = "media"
    MEDIA_URL = "/media/"

    LOCALISH_STORAGE_LOCATION = "localish_data"
    EXTERNAL_STORAGE_LOCATION = "/external_data"
    EXTERNAL_STORAGE_LOCATION_B = "external_data_b"

    NEWSLETTER_THUMBNAIL = "sorl-thumbnail"

    ALLOWED_HOSTS: list[str] = ["*"]

    # Application definition

    SITE_ID = 1

    TEMPLATE_CONTEXT_PROCESSORS = ["django.template.context_processors.request"]

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "fighthealthinsurance",
        "sorl.thumbnail",
        "easy_thumbnails",
        "cookie_consent",
        "compressor",
        "compressor_toolkit",
        "django_extensions",
        "static_thumbnails",
        "memoize",
        "django_recaptcha",
        "rest_framework",
        "corsheaders",
        "django_prometheus",
    ]

    COMPRESS_JS_FILTERS = [
        "compressor.filters.jsmin.JSMinFilter",
        "compressor.filters.yuglify.YUglifyJSFilter",
    ]

    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    )
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False
    COMPRESS_YUGLIFY_BINARY = "yuglify"
    COMPRESS_YUGLIFY_JS_ARGUMENTS = "--mangle"
    COMPRESS_PRECOMPILERS = (
        ("module", "compressor_toolkit.precompilers.ES6Compiler"),
        ("css", "compressor_toolkit.precompilers.SCSSCompiler"),
    )

    MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "cookie_consent.middleware.CleanCookiesMiddleware",
        "django_user_agents.middleware.UserAgentMiddleware",
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]

    GOOGLE_ANALYTICS = {
        "google_analytics_id": "G-2EDT623L0V",
    }

    ROOT_URLCONF = "fighthealthinsurance.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "fighthealthinsurance.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    # MEDIA FILE SETTINGS

    MEDIA_URL = "media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # CORS settings
    CORS_URLS_REGEX = r"^/ziggy/.*$"
    # CORS_ALLOWED_ORIGINS_REGEXES = [
    #    "https://fhi-react.vercel.app",
    #    "http://localhost:\d+",
    #    "https://localhost:\d+",
    #    "http://127.0.0.1:\d+",
    # ]
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_PRIVATE_NETWORK = True
    CORS_ALLOW_CREDENTIALS = True

    PROMETHEUS_METRIC_NAMESPACE = "fhi"

    # STRIPE SETTINGS
    @property
    def STRIPE_API_SECRET_KEY(self):
        return os.getenv(
            "STRIPE_TEST_SECRET_KEY",
            "",
        )

    @property
    def STRIPE_API_PUBLISHABLE_KEY(self):
        return os.getenv(
            "STRIPE_TEST_PUBLISHABLE_KEY",
            "pk_test_51MXFu6FI0Ls3lz8tKOwolhL765Pc6WUkeZGTrOqri8ibbWJzRwLqJGRmyY8r6he09aMmGsULImRfIbErgjxvEVTO00vgERwX4P",
        )

    @cached_property
    def EXTERNAL_STORAGE(self) -> Storage:
        from django.core.files.storage import FileSystemStorage

        return FileSystemStorage(location=self.EXTERNAL_STORAGE_LOCATION)

    @cached_property
    def EXTERNAL_STORAGE_B(self) -> Storage:
        from django.core.files.storage import FileSystemStorage

        return FileSystemStorage(location=self.EXTERNAL_STORAGE_LOCATION_B)

    @cached_property
    def LOCALISH_STORAGE(self) -> Storage:
        from django.core.files.storage import FileSystemStorage

        return FileSystemStorage(location=self.LOCALISH_STORAGE_LOCATION)

    @cached_property
    def COMBINED_STORAGE(self) -> Storage:
        return CombinedStorage(
            self.LOCALISH_STORAGE, self.EXTERNAL_STORAGE, self.EXTERNAL_STORAGE_B
        )

    # Ignore some 404 errors
    IGNORABLE_404_URLS = [
        re.compile(r"\.(php|cgi)$"),
        re.compile(r"^/phpmyadmin/"),
        re.compile(r"^/apple-touch-icon.*\.png$"),
        re.compile(r"^/favicon\.ico$"),
        re.compile(r"^/robots\.txt$"),
    ]


class Dev(Base):
    DEBUG = True
    RECAPTCHA_TESTING = True
    os.environ["RECAPTCHA_TESTING"] = "True"
    # RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")
    # RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")
    SILENCED_SYSTEM_CHECKS = [
        "captcha.recaptcha_test_key_error",
        "django_recaptcha.recaptcha_test_key_error",
    ]

    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "TEST": {
                "NAME": BASE_DIR / "test.db.sqlite3",
            },
        },
    }


class Test(Dev):
    # This is a hack since the actors start up without the django test interface around them
    dt = str(int(time.time()))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / f"test{dt}.db.sqlite3",
            "TIMEOUT": 10,
            "TEST": {
                "NAME": BASE_DIR / f"test{dt}.db.sqlite3",
            },
        },
    }


class Prod(Base):
    DEBUG = False

    @property
    def SECRET_KEY(self):
        return os.getenv("SECRET_KEY", "")

    @property
    def STRIPE_API_SECRET_KEY(self):
        return os.getenv("STRIPE_LIVE_SECRET_KEY", "")

    @property
    def STRIPE_API_PUBLISHABLE_KEY(self):
        return os.getenv("STRIPE_LIVE_PUBLISHABLE_KEY", "")

    @property
    def DATABASES(self):
        engine = "django_prometheus.db.backends.mysql"
        return {
            "default": {
                "ENGINE": engine,
                "NAME": os.getenv("DBNAME"),
                "USER": os.getenv("DBUSER"),
                "PASSWORD": os.getenv("DBPASSWORD"),
                "HOST": os.getenv("DBHOST"),
                "ATOMIC_REQUESTS": False,
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "use_unicode": True,
                },
            }
        }

    EXTERNAL_STORAGE_LOCATION = "/external_data"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "pigscanfly.ca")
    EMAIL_USE_TLS = True
    EMAIL_PORT = 25
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "support")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = "support42@fighthealthinsurance.com"
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "")
    RECAPTCHA_REQUIRED_SCORE = 0.85
    RECAPTCHA_TESTING = False
    os.environ["RECAPTCHA_TESTING"] = "False"
    ADMINS = [("Holden Karau", "holden.karau@gmail.com")]
    SERVER_EMAIL = "support@pigscanfly.ca"
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "filters": [],
            },
            "mail_admins": {
                "level": "ERROR",
                "filters": [],
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }

    MINIO_STORAGE_ACCESS_KEY = os.getenv("EX_MINIO_ACCESS", None)
    MINIO_STORAGE_SECRET_KEY = os.getenv("EX_MINIO_SECRET", None)
    MINIO_STORAGE_REGION = os.getenv("EX_MINIO_REGION", None)
    MINIO_STORAGE_ENDPOINT = os.getenv("EX_MINIO_HOST_ENDPOINT", None)
    MINIO_CERT_CHECK = os.getenv("EX_MINIO_CERT_CHECK", "True") == "True"
    MINIO_STORAGE_USE_HTTPS = os.getenv("EX_MINIO_USE_HTTPS", "True") == "True"
    MINIO_STORAGE_MEDIA_BUCKET_NAME = os.getenv("EX_MINIO_BUCKET")

    @cached_property
    def EXTERNAL_STORAGE_B(self):
        try:
            if (
                    self.MINIO_STORAGE_ENDPOINT is not None and
                    self.MINIO_STORAGE_ACCESS_KEY is not None and
                    self.MINIO_STORAGE_SECRET_KEY is not None and
                    self.MINIO_STORAGE_MEDIA_BUCKET_NAME is not None):
                minio_client = m.Minio(
                    self.MINIO_STORAGE_ENDPOINT,
                    access_key=self.MINIO_STORAGE_ACCESS_KEY,
                    secret_key=self.MINIO_STORAGE_SECRET_KEY,
                    region=self.MINIO_STORAGE_REGION,
                    secure=self.MINIO_STORAGE_USE_HTTPS,
                )
                minio = MinioStorage(
                    minio_client,
                    bucket_name=self.MINIO_STORAGE_MEDIA_BUCKET_NAME,
                    auto_create_bucket=True,
                )
                return minio
            else:
                raise Exception("No storage endpoint configured")
        except Exception as e:
            print(
                f"Failed to setup minio storage to {self.MINIO_STORAGE_ENDPOINT} -- {e}"
            )
            print(traceback.format_exc())
            return None
