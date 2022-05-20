import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from .models import CompressedImage


def check_tier_permissions(original_img, author, url):
    tmp_context = {}
    if author.tier.can_link_200px_height:
        tmp_context['200px'] = create_thumbnail(200, original_img, url)
    if author.tier.can_link_400px_height:
        tmp_context['400px'] = create_thumbnail(400, original_img, url)
    if author.tier.can_link_original_image:
        tmp_context['original'] = f"{url}{original_img.img.url}"
    if author.tier.can_link_custom_height and author.tier.custom_height_px > 0:
        tmp_context['custom'] = create_thumbnail(author.tier.custom_height_px,
                                                 original_img, url)
    return tmp_context


def create_thumbnail(height, original_img, url):
    img_tmp = Image.open(original_img.img.file.name)
    width = int(height / img_tmp.height * img_tmp.width)
    img_tmp.thumbnail((width, height), Image.ANTIALIAS)
    output = BytesIO()
    img_tmp.save(output, format="PNG", quality=75)
    output.seek(0)
    thumbnail = InMemoryUploadedFile(output, 'ImageField', original_img.img.name, 'image/png',
                                     sys.getsizeof(output), None)
    tmp = CompressedImage.objects.create(img=thumbnail, original=original_img, px=height)
    return f"{url}{tmp.img.url}"
