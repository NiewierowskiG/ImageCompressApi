from django.contrib import admin
from .models import OriginalImage, Author, Tier, CompressedImage, TemporaryUrl

admin.site.register(OriginalImage)
admin.site.register(Author)
admin.site.register(Tier)
admin.site.register(CompressedImage)
admin.site.register(TemporaryUrl)
