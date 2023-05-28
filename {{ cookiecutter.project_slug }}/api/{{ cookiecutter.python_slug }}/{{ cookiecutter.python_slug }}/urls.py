"""{{ cookiecutter.python_slug }} URL Configuration"""

import logging
import asyncio
import json
from celery import shared_task
from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from ninja import NinjaAPI
from {{ cookiecutter.python_slug }}.models import (
    BlogPost,
)
from {{ cookiecutter.python_slug }}.schemas import (
    StatusSchema,
)

from django.conf.urls.static import static  # type: ignore
from django.conf import settings  # type: ignore
from django.views.generic import TemplateView  # type: ignore
from {{ cookiecutter.python_slug }}.crud.utils import add_model_crud_route
from ninja.security import HttpBasicAuth
from django.contrib.auth.models import User
from typing import List, Dict
import requests
import datetime
import random
import string

LOGGER = logging.getLogger(__name__)

import time
UPTIME_START = time.time()

api = NinjaAPI()

# HACKY STATUS< DO THIS RIGHT

from django.db import connections
from django.db.utils import OperationalError


@shared_task
def celery_long_running_task(input_str) -> bool:
    """Update a reader account database from the source data."""
    LOGGER.info("We did something: %s", input_str)
    time.sleep(120)
    return True


@api.get('/long-running-task/', response=str)
def submit_long_running(request) -> str:
    input_str = "This is something that takes a while!"
    task = celery_long_running_task.delay(input_str)
    LOGGER.info("Submitted task with input %s with task ID %s", input_str, task.task_id)
    return task.task_id


@api.get('/async-task/', response=bool)
async def async_task_thing(request) -> bool:
    # This is an example of an async coroutine where the current loop can
    # do other work while it's waiting for this operation to finish.  The
    # more you can do async, the more a single event loop can do.
    LOGGER.info("Waiting async for a coroutine...")
    await asyncio.sleep(3)
    LOGGER.info("Finished waiting async for a coroutine!")
    return True


@api.get('/status', response=StatusSchema)
def return_status(request) -> StatusSchema:
    total_uptime = time.time() - UPTIME_START
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        database_connected = False
    else:
        database_connected = True

    result = {'uptime': total_uptime, 'database_connected': database_connected}
    return result


### Add standard crud models, do this somewhere else and make this a function call? ###
# NOTE: This has to happen before the urlpatterns are created or the urls won't be populated
# in the API properly.
add_model_crud_route(api, "blog_posts", BlogPost)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


### Kill this if it's not local - this is stupid and just creates a user for the django admin interface for now.
try:
    # FOR TESTING PURPOSES FOR NOW
    from django.contrib.auth import get_user_model
    User = get_user_model()  # get the currently active user model,
    User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@localhost', 'admin')
    # DELETE THIS WHEN WE HAVE REAL ADMIN PERSISTENCE
except:
    pass
