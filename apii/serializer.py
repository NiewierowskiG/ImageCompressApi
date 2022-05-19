from rest_framework import serializers
from .models import OriginalImage


class OriginalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalImage
        fields = ['img']
