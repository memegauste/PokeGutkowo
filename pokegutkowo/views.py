"""DRF views."""
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from pokegutkowo.models import Player, Post, Settings
from pokegutkowo.serializers import (PlayerSerializer, PostSerializer,
                                     SettingsSerializer)


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
        instance = Settings.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
