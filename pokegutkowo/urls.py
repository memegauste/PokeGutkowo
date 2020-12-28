"""PokeGutkowo app urls."""
# Django
from django.urls import path

# Project
from pokegutkowo.views import PlayersView
from pokegutkowo.views import PostsView
from pokegutkowo.views import SettingsView

urlpatterns = [
    path('players/', PlayersView.as_view(), name='players_view'),
    path('posts/', PostsView.as_view(), name='posts_view'),
    path('settings/', SettingsView.as_view(), name='settings_view'),
]
