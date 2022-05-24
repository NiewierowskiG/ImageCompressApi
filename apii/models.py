from django.db import models
from django.conf import settings
from datetime import datetime
import random
import string


def generate_url():
    while True:
        new_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if not TemporaryUrl.objects.filter(tmp_url=new_url).exists():
            return new_url


def file_location_original(instance, filename):
    time_now = datetime.now()
    return '/'.join(['images', instance.author.user.username, time_now.strftime("%d-%m-%Y"), filename])


def file_location_compressed(instance, filename):
    time_now = datetime.now()
    return '/'.join(['images', instance.original.author.user.username, time_now.strftime("%d-%m-%Y"),
                     str(instance.px)+"px"+filename])


class Tier(models.Model):
    name = models.CharField(max_length=50)
    can_link_200px_height = models.BooleanField()
    can_link_400px_height = models.BooleanField()
    can_link_custom_height = models.BooleanField()
    custom_height_px = models.PositiveIntegerField(null=True)
    can_link_original_image = models.BooleanField()
    can_create_tmp_url = models.BooleanField()

    def __str__(self):
        return self.name


class User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class OriginalImage(models.Model):
    img = models.ImageField(blank=True, upload_to=file_location_original)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.img.name


class CompressedImage(models.Model):
    img = models.ImageField(upload_to=file_location_compressed)
    original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE)
    px = models.PositiveIntegerField()

    def __str__(self):
        return self.img.name


class TemporaryUrl(models.Model):
    main_url = models.CharField(max_length=250)
    tmp_url = models.CharField(max_length=100, default=generate_url)
    expires = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
