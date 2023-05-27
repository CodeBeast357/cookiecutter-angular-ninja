import os
from generic_api.settings.base import *


# Set default settings file
os.environ["DJANGO_SETTINGS_MODULE"] = "generic_api.settings.base"


if os.environ.get("AD_HOC_ENVIRONMENT") == "jupyter":
    os.environ["DJANGO_SETTINGS_MODULE"] = "generic_api.settings.jupyter"
    from generic_api.settings.jupyter import *