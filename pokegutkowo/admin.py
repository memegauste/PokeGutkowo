from django.contrib import admin

# Register your models here.
from pokegutkowo.models import Players, Post, Settings


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    """Players admin.."""


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """Model admin."""
    pass
