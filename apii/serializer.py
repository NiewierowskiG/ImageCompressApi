from rest_framework import serializers
from .models import OriginalImage, TemporaryUrl


class OriginalImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OriginalImage
        fields = ['img']


class TemporaryUlrSerializer(serializers.ModelSerializer):
    time = serializers.IntegerField(help_text="time to expire in seconds (between 300 and 30000)")

    class Meta:
        model = TemporaryUrl
        fields = ['main_url', 'time']

