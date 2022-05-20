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
            thumbnail200px = create_thumbnail(200, original_img.img.file.name, original_img.img.name)
            CompressedImage.objects.create(img=thumbnail200px, original=original_img, px=200)
            return Response(context, status=status.HTTP_201_CREATED)
