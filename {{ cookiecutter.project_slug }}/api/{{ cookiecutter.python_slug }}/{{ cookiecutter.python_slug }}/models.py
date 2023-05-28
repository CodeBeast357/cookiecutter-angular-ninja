from django.db import models  # type: ignore

from django.db.models.signals import pre_delete
from django.dispatch import receiver
import logging

LOGGER = logging.getLogger(__name__)


class BlogPost(models.Model):
    """Account login information for a snowflake database."""

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=524288)
