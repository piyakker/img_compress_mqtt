from django.contrib import admin
from .models import UploadImage, compressedImage

# Register your models here.
admin.site.register(UploadImage)
admin.site.register(compressedImage)
