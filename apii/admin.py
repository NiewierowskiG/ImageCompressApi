from django.contrib import admin
from .models import OriginalImage, User, Tier, CompressedImage

admin.site.register(OriginalImage)
admin.site.register(User)
admin.site.register(Tier)
admin.site.register(CompressedImage)

