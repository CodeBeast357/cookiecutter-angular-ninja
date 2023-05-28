from django.contrib import admin  # type: ignore
from .models import (
    BlogPost,
)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]

admin.site.register(BlogPost, BlogPostAdmin)
