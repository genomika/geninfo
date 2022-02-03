import dj_database_url

from .base import *  # noqa


DEBUG = True


STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"


db_from_env = dj_database_url.config()
DATABASES["default"].update(db_from_env)
DATABASES["default"]["CONN_MAX_AGE"] = 500
if "OPTIONS" in DATABASES["default"] and "sslmode" in DATABASES["default"]["OPTIONS"]:
    del DATABASES["default"]["OPTIONS"]["sslmode"]


DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
