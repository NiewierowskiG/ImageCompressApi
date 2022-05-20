import sys
from io import BytesIO
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from rest_framework.generics import ListAPIView
from .serializer import OriginalImageSerializer
from .models import OriginalImage, User, CompressedImage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def create_thumbnail(height, original_img, filename):
    img_tmp = Image.open(original_img)
    width = int(height/img_tmp.height * img_tmp.width)
    img_tmp.thumbnail((width, height), Image.ANTIALIAS)
    output = BytesIO()
    img_tmp.save(output, format="PNG", quality=75)
    output.seek(0)
    thumbnail = InMemoryUploadedFile(output, 'ImageField', filename, 'image/png',
                                     sys.getsizeof(output), None)
    return thumbnail


class ImageViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OriginalImageSerializer

    def get_queryset(self):
        author = User.objects.get(user=self.request.user)
        return OriginalImage.objects.filter(author=author)

    def post(self, request):
        serializer = OriginalImageSerializer(data=request.data)
        print(self.request.user)
        if serializer.is_valid():
            context = {}
            author = User.objects.get(user=request.user)
            original_img = OriginalImage.objects.create(img=request.data['img'], author=author)
            if author.tier.can_link_200px_height:
                thumbnail200px = create_thumbnail(200, original_img.img.file.name, original_img.img.name)
                tmp = CompressedImage.objects.create(img=thumbnail200px, original=original_img, px=200)
                context['200px'] = f"{request.get_host()}{tmp.img.url}"
            if author.tier.can_link_200px_height:
                thumbnail400px = create_thumbnail(400, original_img.img.file.name, original_img.img.name)
                tmp = CompressedImage.objects.create(img=thumbnail400px, original=original_img, px=400)
                context['400px'] = f"{request.get_host()}{tmp.img.url}"
            if author.tier.can_link_original_image:
                context['original'] = f"{request.get_host()}{original_img.img.url}"
            if author.tier.can_link_custom_height and author.tier.custom_height_px > 0:
                thumbnail_custom = create_thumbnail(author.tier.custom_height_px, original_img.img.file.name,
                                                  original_img.img.name)
                tmp = CompressedImage.objects.create(img=thumbnail_custom, original=original_img,
                                                     px=author.tier.custom_height_px)
                context['custom'] = f"{request.get_host()}{tmp.img.url}"
            return Response(context, status=status.HTTP_201_CREATED)
