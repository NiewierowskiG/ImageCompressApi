import datetime

from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .serializer import OriginalImageSerializer
from .models import OriginalImage, User, TemporaryUrl
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .comress import check_tier_permissions


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
            author = User.objects.get(user=request.user)
            original_img = OriginalImage.objects.create(img=request.data['img'], author=author)
            context = check_tier_permissions(original_img, author, request.get_host())
            return Response(context, status=status.HTTP_201_CREATED)


@login_required()
@api_view(['GET'])
def get_temporary_url(request, url, time):
    author = User.objects.get(user=request.user)
    if not author.tier.can_create_tmp_url:
        return Response({"error": "you dont have permissions to create temporary link!"},
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if 300 <= time <= 30000:
        expires = datetime.datetime.now() + datetime.timedelta(seconds=time)
        TemporaryUrl.objects.create(main_url=url, expires=expires)
        return Response({"url": url, "time": time}, status=status.HTTP_200_OK)
    return Response({"error": "time needs to be between 300 and 30000 seconds!"}, status=status.HTTP_400_BAD_REQUEST)
