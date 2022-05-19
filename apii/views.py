from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializer import OriginalImageSerializer
from .models import OriginalImage, User
from rest_framework.response import Response
from rest_framework import status


class ImageViewSet(ListAPIView):
    serializer_class = OriginalImageSerializer
    queryset = OriginalImage.objects.all()

    def post(self, request):
        serializer = OriginalImageSerializer(data=request.data)
        if serializer.is_valid():
            author = User.objects.get(user=request.user)
            OriginalImage.objects.create(img=request.data['img'], author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
