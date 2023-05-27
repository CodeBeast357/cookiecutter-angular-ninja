from django.contrib import admin  # type: ignore
from .models import (
    ReaderAccount,
    SourceAccount,
)

class ReaderAccountAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "source_company_key",
        "source_company_database",
        "account_url",
        "username",
        "role",
        "warehouse",
        "status_code"
    ]

class SourceAccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_url",
        "username",
        "role",
        "warehouse",
    ]

admin.site.register(ReaderAccount, ReaderAccountAdmin)
admin.site.register(SourceAccount, SourceAccountAdmin)
