import datetime
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .serializer import OriginalImageSerializer, TemporaryUlrSerializer
from .models import OriginalImage, Author, TemporaryUrl
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .comress import check_tier_permissions


class ImageViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OriginalImageSerializer

    def get_queryset(self):
        author = Author.objects.get(user=self.request.user)
        return OriginalImage.objects.filter(author=author)

    def post(self, request):
        serializer = OriginalImageSerializer(data=request.data)
        if serializer.is_valid():
            author = Author.objects.get(user=request.user)
            original_img = OriginalImage.objects.create(img=request.data['img'], author=author)
            context = check_tier_permissions(original_img, author, request.get_host())
            return Response(context, status=status.HTTP_201_CREATED)


class TemporaryUrlViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemporaryUlrSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = TemporaryUlrSerializer(data=request.data)
        if serializer.is_valid():
            author = Author.objects.get(user=request.user)
            if author.tier.can_create_tmp_url:
                expires = datetime.datetime.now() + datetime.timedelta(seconds=int(request.data['time']))
                tmp = TemporaryUrl.objects.create(main_url=request.data['main_url'], expires=expires)
                tmp_url = f"{request.build_absolute_uri()}/{tmp.tmp_url}"
                return Response({"tmp_url": tmp_url, "main_url": tmp.main_url, "expires": tmp.expires},
                                status=status.HTTP_200_OK)
            return Response({"error": "you dont have permissions to create temporary link!"},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response({"error": "time to expire needs to be between 300 and 30000 seconds"},
                        status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def redirect_temporary_url(request, url):
    try:
        tmp = TemporaryUrl.objects.get(tmp_url=url)
        return redirect(tmp.main_url)
    except TemporaryUrl.DoesNotExist:
        return Response({"error": "That link doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
