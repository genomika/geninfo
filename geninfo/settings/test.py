import dj_database_url

from .base import *  # noqa


DEBUG = True

MEDIA_ROOT = base_dir_join("mediafiles")
MEDIA_URL = "/media/"


db_from_env = dj_database_url.config()
DATABASES["default"].update(db_from_env)
DATABASES["default"]["CONN_MAX_AGE"] = 500
