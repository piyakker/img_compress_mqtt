from django.urls import path

from . import views

app_name = 'sampleapp'
urlpatterns = [
    path('', views.image_request, name="image-request"),
    path('compressed', views.save_compressed, name="image-url"),
    path('get-compressed', views.get_compressed_url)
]
