from ninja import Schema


class StatusSchema(Schema):
    uptime: int
    database_connected: bool
