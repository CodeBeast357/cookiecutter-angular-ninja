from django.db import models  # type: ignore

from django.db.models.signals import pre_delete
from django.dispatch import receiver
import logging

LOGGER = logging.getLogger(__name__)


class ReaderAccount(models.Model):
    """Account login information for a snowflake database."""
    source_company_key = models.CharField(max_length=100, null=True)
    source_company_database = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    account_url = models.CharField(max_length=100)
    status_code = models.IntegerField()
    comment = models.CharField(max_length=524288)
    warehouse_created = models.BooleanField(default=False)
    current_share = models.CharField(max_length=100, null=True)

class SourceAccount(models.Model):
    """Account login information for a snowflake database."""
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    account_url = models.CharField(max_length=100)


@receiver(pre_delete, sender=ReaderAccount, dispatch_uid='reader_account_delete_signal')
def delete_snowflake_account(sender, instance, using, **kwargs):
    # Avoid circular imports by only importing this once the function is called and
    # only for this function locally - import will be GC'd once function is over.
    from generic_api.utils.snowflake import get_source_runner

    LOGGER.info("Deleting snowflake account for %s", instance.name)
    source_runner = get_source_runner()
    reader_destroy_sql = f"DROP MANAGED ACCOUNT {instance.name}"
    results = source_runner.execute(reader_destroy_sql)
    LOGGER.info(results)