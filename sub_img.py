from PIL import Image
import os
from paho.mqtt import client as mqtt_client
broker = 'broker.hivemq.com'
port = 1883
topic = "photos"
topic_sub = "photos"
client_id = 'xzcfghjt123'


def compress(image_file):

    filepath = os.path.join(os.getcwd(), image_file)

    image = Image.open(filepath)

    image.save("/home/ericlien/Pictures/image-file-compressed.jpg",
               "JPEG",
               optimize=True,
               quality=10)
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
        print(f"Message : {msg.payload}")
        f = open('receive.jpg', 'wb')
        f.write(msg.payload)
        f.close()
        compress('receive.jpg')
        print('image received')
    client.subscribe(topic_sub)
    client.on_message = on_message


def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()
