import logging
import time
import configparser
from sqlalchemy import text

import snowflake.connector

from generic_api.models import (
    ReaderAccount,
    SourceAccount,
)

LOGGING_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"
NORMAL_LOGGING_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
logging.basicConfig(
    format=NORMAL_LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT, level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

class SnowRunner:
    def __init__(self, user, account, password, warehouse=None, role=None):
        self._user = user
        self._account = account
        self._password = password
        self.warehouse = warehouse
        self._ctx = None
        self.version = self.get_version()
        if warehouse is not None:
            self.set_warehouse(self.warehouse)
        if role is not None:
            self.use_role(role)
            
    def use_role(self, role):
        sql_command = f"USE ROLE {role};"
        result = self.execute(sql_command)
        LOGGER.info("Set role to %s", role)
        return result

    def set_warehouse(self, warehouse):
        self._warehouse = warehouse
        result = self.execute(f"USE WAREHOUSE {self.warehouse};")
        LOGGER.info("Warehouse set to %s", self.warehouse)
        return result
    
    def use_database(self, database):
        result = self.execute(f"USE DATABASE {database};")
        LOGGER.info("Set DATABASE to %s", database)
        return result

    @property
    def ctx(self):
        if self._ctx and not self._ctx.is_closed():
            return self._ctx
        self._ctx = snowflake.connector.connect(
            user=self._user, account=self._account, password=self._password
        )
        return self._ctx

    def execute(self, sql):
        """Run a query with a context managed snowflake connector."""
        LOGGER.info("Running sql: %s", sql)
        cursor = self.ctx.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


    def get_version(self):
        """Get the snowflake current version."""
        query_results = self.execute("SELECT current_version()")
        first_result = query_results[0]
        version = first_result[0]
        return version


def get_source_runner(username="ARTEMIS_SERVICE"):
    source = SourceAccount.objects.get(username=username)
    source_runner = SnowRunner(
        source.username,
        source.account_url,
        source.password,
        warehouse=source.warehouse,
        role=source.role
    )
    return source_runner

def get_reader_runner(runner_name):
    reader = ReaderAccount.objects.get(name=runner_name)
    reader_runner = SnowRunner(
        reader.username,
        reader.account_url.split('/')[-1].split('snowflake')[0].rstrip('.'),
        reader.password,
        role=reader.role,
    )
    return reader_runner