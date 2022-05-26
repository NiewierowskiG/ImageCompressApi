from io import StringIO
import base64
from io import BytesIO

from PIL import Image
from django.test import TestCase
from django.contrib.auth.models import User
from djangoProject2 import settings
from .models import Tier, Author, OriginalImage
from .comress import check_tier_permissions
from .management.commands.create_database import create_tiers
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

tier_list = (
    "Basic",
    "Premium",
    "Enterprise"
)


def check_image_size(path, px):
    image = Image.open(path[1:])
    if image.height == px:
        return True
    return False


def check_images_context(context, tier):
    if tier.can_link_200px_height:
        if not check_image_size(context['200px'], 200):
            return False
    if tier.can_link_400px_height:
        if not check_image_size(context['400px'], 400):
            return False
    if tier.can_link_custom_height:
        if not check_image_size(context['custompx'], tier.custom_height_px):
            return False
    return True


def create_original_img(img, user, tier_name):
    tier = Tier.objects.get(name=tier_name)
    author = Author.objects.create(tier=tier, user=user)
    original_img = OriginalImage.objects.create(img=img, author=author)
    return tier, author, original_img


class TierTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@test.pl", "TestTest123")
        self.image = SimpleUploadedFile(name='test.jpg', content=open("media/images/test/test.jpg", 'rb').read(),
                                        content_type='image/jpeg')
        create_tiers()

    def test_basic_tiers(self):
        for tier_name in tier_list:
            tier, author, original_img = create_original_img(self.image, self.user, tier_name)
            context = check_tier_permissions(original_img, author, "")
            self.assertTrue(check_images_context(context, tier))
