from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.ImageViewSet.as_view(), name='upload'),
    path('tempurl', views.TemporaryUrlViewSet.as_view()),
    path('tempurl/<str:url>', views.redirect_temporary_url)
    ]
