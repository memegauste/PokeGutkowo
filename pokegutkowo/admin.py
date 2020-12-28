"""Admin file."""
# Django
from django.contrib import admin

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

    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """Model admin."""

    pass
