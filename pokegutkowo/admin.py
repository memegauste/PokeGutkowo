from django.contrib import admin

# Register your models here.
from pokegutkowo.models import Players, Post, Settings

admin.site.register(Players)
admin.site.register(Post)
admin.site.register(Settings)
