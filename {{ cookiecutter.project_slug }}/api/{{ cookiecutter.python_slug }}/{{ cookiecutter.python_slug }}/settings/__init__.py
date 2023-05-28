import os
from {{cookiecutter.python_slug}}.settings.base import *


# Set default settings file
os.environ["DJANGO_SETTINGS_MODULE"] = "{{cookiecutter.python_slug}}.settings.base"


if os.environ.get("AD_HOC_ENVIRONMENT") == "jupyter":
    os.environ["DJANGO_SETTINGS_MODULE"] = "{{cookiecutter.python_slug}}.settings.jupyter"
    from {{cookiecutter.python_slug}}.settings.jupyter import *