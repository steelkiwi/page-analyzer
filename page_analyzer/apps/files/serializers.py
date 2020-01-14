from rest_framework import serializers

from files.models import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    thumbnail = serializers.URLField(source="thumbnail.url", read_only=True)

    class Meta:
        model = Avatar
        fields = ("id", "file", "thumbnail")
