from django.db import models

# Create your models here.

# UploadImage => OriginalImage
class OriginalImage(models.Model):
    # name, image_url
    name = models.CharField(max_length=200)
    orig_img_url = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

# CompressedImage
class CompressedImage(models.Model):
    # image_url, original_image
    comp_img_url = models.CharField(max_length=200)
    orig_img = models.ForeignKey(
        OriginalImage, on_delete=models.SET_NULL, null=True)
