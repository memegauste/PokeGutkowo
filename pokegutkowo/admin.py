"""Admin file."""
# Django
from django.contrib import admin
from django.db import models

from django_ckeditor_5.widgets import CKEditor5Widget

# Project
# Register your models here.
from pokegutkowo.models import Player
from pokegutkowo.models import Post
from pokegutkowo.models import Settings


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Players admin.."""

    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget},
    }


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """Model admin."""

    pass
