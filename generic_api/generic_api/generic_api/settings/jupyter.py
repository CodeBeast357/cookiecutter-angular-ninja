import os

from generic_api.settings.base import *

print("Loaded local settings.")

INSTALLED_APPS += ("django_extensions",)
NOTEBOOK_DEFAULT_URL = '/lab'  # Using JupyterLab


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ad_hoc_analytics_database",
        "USER": "postgres", # TODO: Pull this from configmap and os.environ
        "PASSWORD": "1f2d1e2e67df",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    "--allow-root",
]
IPYTHON_KERNEL_DISPLAY_NAME = 'Ad Hoc Analytics API Kernel'
