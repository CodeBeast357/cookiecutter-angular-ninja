from ninja import Schema
import datetime
from generic_api.models import ReaderAccount
from ninja.orm import create_schema
from typing import Optional

class StatusSchema(Schema):
    uptime: int
    mysql_connected: bool

    
class DatabasesSchema(Schema):
    created_on: datetime.datetime
    name: str
    is_default: str
    is_current: str
    origin: str
    owner: str
    comment: str
    options: str
    retention_time: int


class ManagedAccount(Schema):
    source_company_key: str
    source_company_database: str
    name: str
    username: str
    role: str
    warehouse: str
    account_url: str
    status_code: int
    comment: str
    warehouse_created: bool
    current_share: Optional[str]

class DeleteManagedAccount(Schema):
    id: int

class CreateManagedAccount(Schema):
    name: str
    database: str

class CreateManagedAccountWarehouse(Schema):
    id: int

ReaderAccountSchema = create_schema(model=ReaderAccount, name=f"ReaderAccountSchema", exclude={'password'})
