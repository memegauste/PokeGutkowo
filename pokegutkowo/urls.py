"""PokeGutkowo app urls."""
from django.urls import path

from pokegutkowo.views import PlayersView

urlpatterns = [
    path('players/', PlayersView.as_view(), 'players_view'),
    path('posts/', PlayersView.as_view(), 'players_view'),
    path('players/', PlayersView.as_view(), 'players_view'),
]