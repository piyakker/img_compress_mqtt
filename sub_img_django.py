# built-in modules
import os
import uuid


# third party modules
import pickle
import requests
from PIL import Image
from paho.mqtt import client as mqtt_client


# variables (put into .env)
broker = 'broker.hivemq.com'
port = 1883
topic = "django/mqtt"
topic_sub = "django/mqtt"
client_id = 'xzcfghjt123'


def compress(client, image_file, id):

    filepath = os.path.join(os.getcwd(), image_file)
    print(filepath)
    image = Image.open(filepath)
    filename = uuid.uuid1()
    image.save(f"/home/ericlien/Pictures/{filename}.jpg",
               "JPEG",
               optimize=True,
               quality=10)
    client.publish(
        'compressed', f"/home/ericlien/Pictures/{filename}.jpg", 2)
    requests.post('http://127.0.0.1:8000/compressed',
                  data={'id': id, 'imgUrl': f"/home/ericlien/Pictures/{filename}.jpg"})
    print('done')
    os.remove(image_file)
    return


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        # print(type(msg))
        # print(dir(msg))
        unpickled = pickle.loads(msg.payload)
        # print(f"Message : {unpickled['payload']}")
        f = open('receive.jpg', 'wb')
        f.write(unpickled['payload'])
        f.close()
        compress(client, 'receive.jpg', unpickled['id'])
        
    client.subscribe(topic_sub)
    client.on_message = on_message


def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()
