"""{{ cookiecutter.python_slug }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging
import asyncio
import json
from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from ninja import NinjaAPI
from {{ cookiecutter.python_slug }}.models import (
    ReaderAccount,
    SourceAccount,
)
from celery import shared_task

from django.conf.urls.static import static  # type: ignore
from django.conf import settings  # type: ignore
from django.views.generic import TemplateView  # type: ignore
from {{ cookiecutter.python_slug }}.crud.utils import add_model_crud_route
from ninja.security import HttpBasicAuth
from django.contrib.auth.models import User
from typing import List, Dict

from {{ cookiecutter.python_slug }}.schemas import (
    StatusSchema,
    DatabasesSchema,
    ManagedAccount,
    ReaderAccountSchema,
    DeleteManagedAccount,
    CreateManagedAccount,
    CreateManagedAccountWarehouse,
)
from {{ cookiecutter.python_slug }}.utils.snowflake import (
    get_source_runner,
    get_reader_runner,
)
import requests
import datetime
import random
import string

LOGGER = logging.getLogger(__name__)

# get random password pf length 8 with letters, digits, and symbols
RANDOM_PASS_CHARS = string.ascii_letters + string.digits + '@#$%&'

import time
UPTIME_START = time.time()

api = NinjaAPI()

# HACKY STATUS< DO THIS RIGHT

from django.db import connections
from django.db.utils import OperationalError


@shared_task
def async_create_managed_account_database(id):
    """Update a reader account database from the source data."""
    LOGGER.info("We definitely updated the account database for account %s", id)
    source = SourceAccount.objects.get(username="ARTEMIS_SERVICE")
    source_runner = get_source_runner()
    # Run som sql on source runner to create new share database
    reader = ReaderAccount.objects.get(id=id)
    reader_runner = get_reader_runner(reader.name)
    # Run some sql on reader runner to update database and names.
    # Run any custom SQL transforms for this customer.
    LOGGER.info("Runners created - starting to create databases.")
    share_db_name = f"{reader.source_company_database}_SHARED_{datetime.datetime.now().strftime('%m%d%Y')}"
    reader_db_name = f"{reader.name}_ADHOC_DB"
    source_account_id = source.account_url.split('//')[-1].split('.')[0].upper()


    # SOURCE SIDE PROVISIONING
    source_runner.execute(f"CREATE DATABASE IF NOT EXISTS {share_db_name} CLONE {reader.source_company_database};")
    schemas = source_runner.execute(f"SHOW SCHEMAS IN DATABASE {reader.source_company_database}")
    schema_names = [schema[1] for schema in schemas if schema[1] not in ("INFORMATION_SCHEMA", "PUBLIC")]
    share_tables = [
        "MEDICAL_CLAIM_LINE_DENORMALIZED",
        "MEMBER_MONTH_DENORMALIZED",
        "RX_CLAIM_DENORMALIZED",
    ]

    source_runner.execute(f'CREATE SHARE IF NOT EXISTS "{share_db_name}" COMMENT="";')
    source_runner.execute(f'GRANT USAGE ON DATABASE "{share_db_name}" TO SHARE "{share_db_name}";')
    for schema in schema_names:
        source_runner.execute(f'GRANT USAGE ON SCHEMA "{share_db_name}"."{schema}" TO SHARE "{share_db_name}";')
        for target_table in share_tables:
            source_runner.execute(f'GRANT SELECT ON VIEW "{share_db_name}"."{schema}"."{target_table}" TO SHARE "{share_db_name}";')
    source_runner.execute(f"ALTER SHARE {share_db_name} ADD ACCOUNTS = {reader.account_url.split('//')[-1].split('.')[0].upper()};")

    # READER SIDE PROVISIONING
    reader_runner.execute(f"DROP DATABASE IF EXISTS {reader_db_name};")
    reader_runner.execute(f'CREATE DATABASE {reader_db_name} FROM SHARE "{source_account_id}"."{share_db_name}" COMMENT="Creating new database from new prod share";')
    reader_runner.execute(f'GRANT IMPORTED PRIVILEGES ON DATABASE "{reader_db_name}" TO ROLE "ACCOUNTADMIN";')
    reader_runner.execute(f'GRANT IMPORTED PRIVILEGES ON DATABASE "{reader_db_name}" TO ROLE "PUBLIC";')
    reader_runner.execute(f'GRANT IMPORTED PRIVILEGES ON DATABASE "{reader_db_name}" TO ROLE "SECURITYADMIN";')
    reader_runner.execute(f'GRANT IMPORTED PRIVILEGES ON DATABASE "{reader_db_name}" TO ROLE "SYSADMIN";')
    reader_runner.execute(f'GRANT IMPORTED PRIVILEGES ON DATABASE "{reader_db_name}" TO ROLE "USERADMIN";')
    reader.current_share = share_db_name
    reader.comment = f"Last updated on {datetime.datetime.now()} from {reader.source_company_database} copy {share_db_name}"
    reader.save()
    return reader


@api.get('/status', response=StatusSchema)
def return_status(request):
    total_uptime = time.time() - UPTIME_START
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        database_connected = False
    else:
        database_connected = True

    return {'uptime': total_uptime, 'database_connected': database_connected}


@api.get('/get-available-databases/', response=List[str])
def return_databases(request):
    """Get a list of valid prod zeus databases that can be shared."""
    source_runner = get_source_runner()
    tuple_results = source_runner.execute("SHOW DATABASES STARTS WITH 'PROD_LIVE_ZEUS'")
    shareable_dbs = [db for db in tuple_results if 'MEMBER_DATA' not in db[1]]
    shareable_dbs = [db for db in shareable_dbs if '_PREVIOUS' not in db[1]]
    shareable_dbs = [db[1] for db in shareable_dbs if '_SHARED_' not in db[1]]
    return shareable_dbs


@api.get('/get-managed-accounts/', response=Dict[str, ManagedAccount])
def return_managed_accounts(request):
    """Get a list of managed accounts"""
    LOGGER.info("Getting managed accounts.")
    source_runner = get_source_runner()
    managed_accounts = source_runner.execute("SHOW MANAGED ACCOUNTS")

    dict_results = {r[0]: {
        'name': r[0],
        'cloud': r[1],
        'region': r[2],
        'locator': r[3],
        'created_on': r[4],
        'url': r[5],
        'is_reader': r[6],
        'comment': r[7],
        'status_code': None
    } for r in managed_accounts}
    for key, val in dict_results.items():
        result = requests.get(val.get('url'))
        dict_results[key]['status_code'] = result.status_code
    return dict_results


@api.post('/create-ad-hoc-account/', response=ReaderAccountSchema)
def create_managed_account(request, payload: CreateManagedAccount):
    """Get a list of managed accounts"""
    LOGGER.info("Creating managed account: %s", payload.name)
    source_runner = get_source_runner()
    account_name = f"AD_HOC_{payload.name.upper()}"
    admin_name = f"{account_name.upper()}_ADMIN"
    admin_password = ''.join(random.choice(RANDOM_PASS_CHARS) for i in range(22))
    reader_create_sql = f"CREATE MANAGED ACCOUNT {account_name} ADMIN_NAME = '{admin_name}', ADMIN_PASSWORD='{admin_password}', TYPE = READER, COMMENT='{account_name}'"
    managed_account = source_runner.execute(reader_create_sql)
    result = managed_account[0][0]
    login_url = json.loads(result).get('loginUrl')
    try: 
        new_account = ReaderAccount(
            source_company_key = "",
            source_company_database = payload.database,
            name=account_name,
            username=admin_name,
            password=admin_password,
            role="ACCOUNTADMIN", 
            warehouse="AD_HOC_WAREHOUSE",
            account_url=login_url,
            status_code = 403,
            comment=f"Name: {account_name}, username: {admin_name}",
            )
        new_account.save()
    # Clean up the account in snowflake if we have an error, then raise the error
    # so we don't leave artifacts on errors.
    except Exception:
        reader_destroy_sql = f"DROP MANAGED ACCOUNT {account_name}"
        source_runner.execute(reader_destroy_sql)
        raise
    return new_account



@api.post('/create-ad-hoc-account-warehouse/', response=ManagedAccount)
def create_managed_account_warehouse(request, payload: CreateManagedAccountWarehouse):
    """Configure a reader account with the appropriate default values."""
    reader = ReaderAccount.objects.get(id=payload.id)
    reader_runner = get_reader_runner(reader.name)
    warehouse_sql = f"CREATE OR REPLACE WAREHOUSE {reader.warehouse} WITH WAREHOUSE_SIZE = 'SMALL' WAREHOUSE_TYPE = 'STANDARD' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 2 SCALING_POLICY = 'STANDARD';"
    usage_sql = f"GRANT MONITOR,OPERATE,USAGE ON WAREHOUSE {reader.warehouse} TO ROLE PUBLIC ;"
    warehouse_result = reader_runner.execute(warehouse_sql)
    usage_result = reader_runner.execute(usage_sql)
    reader.warehouse_created = True
    reader.save()
    return reader



@api.post('/update-account-database/', response=ManagedAccount)
def update_managed_account_database(request, payload: CreateManagedAccountWarehouse):
    """Update a reader account database from the source data."""
    reader = ReaderAccount.objects.get(id=payload.id)
    task = async_create_managed_account_database.delay(payload.id)
    reader.comment = f"Database update in progress - started task {task.task_id} at {datetime.datetime.now()}"
    reader.save()
    return reader


@api.post('/update-account-availability/', response=ManagedAccount)
def update_account_availability(request, payload: CreateManagedAccountWarehouse):
    """Update a reader account database from the source data."""
    LOGGER.info("We definitely updated the database availability for account %s", payload.id)
    # source_runner = get_source_runner()
    # Run som sql on source runner to create new share database
    reader = ReaderAccount.objects.get(id=payload.id)
    res = requests.get(reader.account_url)
    reader.status_code = res.status_code
    reader.save()
    # reader_runner = get_reader_runner(reader.name)
    # Run some sql on reader runner to update database and names.
    # Run any custom SQL transforms for this customer.

    return reader

### Add standard crud models, do this somewhere else and make this a function call? ###
# NOTE: This has to happen before the urlpatterns are created or the urls won't be populated
# in the API properly.
add_model_crud_route(api, "reader_accounts", ReaderAccount)
add_model_crud_route(api, "source_accounts", SourceAccount)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





### Kill this if it's not local - this is ghetto and just creates a user for the django admin interface for now.
try:
    # FOR TESTING PURPOSES FOR NOW
    from django.contrib.auth import get_user_model
    User = get_user_model()  # get the currently active user model,
    User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@localhost', 'admin')
    # DELETE THIS WHEN WE HAVE REAL ADMIN PERSISTENCE
except:
    pass
