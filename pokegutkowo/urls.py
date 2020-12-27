"""PokeGutkowo app urls."""
from django.urls import path

from pokegutkowo.views import PlayersView, PostsView, SettingsView

urlpatterns = [
    path('players/', PlayersView.as_view(), name='players_view'),
    path('posts/', PostsView.as_view(), name='posts_view'),
    path('settings/', SettingsView.as_view(), name='settings_view'),
]
