# Builtin module
import pickle

# Third part moduldes
from mqtt_test.mqtt import client as mqtt_client
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

# Dev modules
from base.forms import UserImageForm
from .models import CompressedImage, OriginalImage



def publish(client, filename, topic):
    result = client.publish(
        topic, filename, 2)
    msg_status = result[0]
    if msg_status == 0:
        print(f"message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")


def image_request(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            img_object = form.save(commit=False)
            img_bytes = request.FILES['orig_img_url'].read()
            img_object.save()

            pickled = pickle.dumps({
              'payload': bytearray(img_bytes),
              'id': img_object.id
            })

            # use loop_start instead of loop_forever is because uploading images isn't that frequent.
            mqtt_client.loop_start()
            publish(mqtt_client, pickled, 'django/mqtt')
            mqtt_client.loop_stop()

            return render(
                request,
                'image_form.html',{
                  'form': form, 
                  'img_obj': img_object
                })
    else:
        form = UserImageForm()

    return render(request, 'image_form.html', {'form': form})


def save_compressed(request):
    if request.method == 'POST':
        imgUrl = request.POST['imgUrl']
        original_image = OriginalImage.objects.get(id=request.POST['id'])

        img = CompressedImage.objects.create(
                orig_img=original_image,
                comp_img_url=imgUrl
            )

        return
    return HttpResponse('save compressed page')


def get_compressed_url(request):
    pk = request.GET.get('pk')
    original_image = OriginalImage.objects.get(pk=pk)
    urls = CompressedImage.objects.filter(
        orig_img=original_image
        )
    
    if len(urls):
        return JsonResponse({
            'url': urls[0].comp_img_url
            })
