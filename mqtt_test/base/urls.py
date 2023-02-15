from django.urls import path
from .views import image_request, save_compressed, get_compressed_url

app_name = 'sampleapp'
urlpatterns = [
    path('', image_request, name="image-request"),
    path('compressed', save_compressed, name="image-url"),
    path('get-compressed', get_compressed_url)
]