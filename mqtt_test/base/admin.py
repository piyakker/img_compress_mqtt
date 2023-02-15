from django.contrib import admin
from .models import OriginalImage, CompressedImage

# Register your models here.
admin.site.register(OriginalImage)
admin.site.register(CompressedImage)
