from django.db import models
from django.conf import settings


class Tier(models.Model):
    name = models.CharField(max_length=50)
    can_link_200px_height = models.BooleanField()
    can_link_400px_height = models.BooleanField()
    can_link_custom_height = models.BooleanField()
    can_link_original_image = models.BooleanField()


class User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)


class OriginalImage(models.Model):
    img = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class CompressedImage(models.Model):
    img = models.ImageField()
    original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE)
