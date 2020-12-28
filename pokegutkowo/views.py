"""DRF views."""
# 3rd-party
# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

# Project
from pokegutkowo.models import Player
from pokegutkowo.models import Post
from pokegutkowo.models import Settings
from pokegutkowo.serializers import PlayerSerializer
from pokegutkowo.serializers import PostSerializer
from pokegutkowo.serializers import SettingsSerializer


class PlayersView(ListAPIView):
    """Player ListAPI view."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PostsView(ListAPIView):
    """Post ListAPI view."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SettingsView(RetrieveAPIView):
    """Settings ListAPI view."""

    serializer_class = SettingsSerializer

    def retrieve(self, request, *args, **kwargs):
        """Return single instance of settings if exists."""
        instance = Settings.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
