"""Serializers file."""
# 3rd-party
from rest_framework import serializers

# Project
from pokegutkowo.models import Player
from pokegutkowo.models import Post
from pokegutkowo.models import Settings


class PlayerSerializer(serializers.ModelSerializer):
    """Player Serializer."""
    
    class Meta:  # noqa: D106
        model = Player
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Post Serializer."""

    author = serializers.StringRelatedField(source='author.nickname', read_only=True)

    class Meta:  # noqa: D106
        model = Post
        fields = ('title', 'context', 'author')


class SettingsSerializer(serializers.ModelSerializer):
    """Settings Serializer."""

    class Meta:  # noqa: D106
        model = Settings
        fields = '__all__'
