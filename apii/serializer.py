from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate_time(self, value):
        if 300 > int(value) or int(value) > 30000:
            raise ValidationError({"expires": "Link expire time must be between 300 and 30000 seconds"})
        return value

