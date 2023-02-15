from django.db import models

# Create your models here.

# UploadImage => OriginalImage
class UploadImage(models.Model):
    # name, image_url
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.caption

# CompressedImage
class compressedImage(models.Model):
    # image_url, original_image
    imgUrl = models.CharField(max_length=200)
    originalImg = models.ForeignKey(
        UploadImage, on_delete=models.SET_NULL, null=True)
