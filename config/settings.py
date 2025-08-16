from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="dev-insecure")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")]
CSRF_TRUSTED_ORIGINS = [h.strip() for h in env("CSRF_TRUSTED_ORIGINS", default="127.0.0.1,localhost").split(",")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "avisos",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "avisos.context_processors.ui_flags",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

#si env("DATABASE_NAME") no existe usar una en la ruta local
if not env("DATABASE_NAME", default=None):
    env("DATABASE_NAME", default=BASE_DIR / "db.sqlite3")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env("DATABASE_NAME"),  
        'OPTIONS': {
            'timeout': 20,  # Opcional: aumenta el timeout para evitar "database is locked"
        }
    }
}

AUTH_USER_MODEL = "avisos.User"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"
LOGIN_URL = "login"

LANGUAGE_CODE = "es-ar"
TIME_ZONE = env("TIME_ZONE", default="America/Argentina/Buenos_Aires")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS = [BASE_DIR / "static"]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 4},
    },
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER=env("GMAIL_USER")
EMAIL_HOST_PASSWORD=env("GMAIL_PASSWORD")

#print(f"DEBUG={DEBUG}, ALLOWED_HOSTS={ALLOWED_HOSTS}, TIME_ZONE={TIME_ZONE}, EMAIL_HOST_USER={EMAIL_HOST_USER}")
