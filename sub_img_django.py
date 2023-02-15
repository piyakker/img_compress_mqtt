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
client_id = 'xzcfghjt123'
save_folder = os.path.abspath('../../../Pictures')

def compress(client, image_file, id):

    filepath = os.path.join(os.getcwd(), image_file)
    image = Image.open(filepath)

    filename = uuid.uuid1()
    save_path = os.path.join(save_folder, f"{filename}.jpg")

    image.save(save_path,
               "JPEG",
               optimize=True,
               quality=10)
    
    try:
        requests.post('http://localhost:8000/compressed',
                    data={
                'id': id,
                'imgUrl': save_path
            })
        print(f'save path of compressed image {filename} to db')
    except:
        print('Failed to save path of compressed image to db')

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

        unpickled = pickle.loads(msg.payload)

        f = open('receive.jpg', 'wb')
        f.write(unpickled['payload'])
        f.close()
        compress(client, 'receive.jpg', unpickled['id'])
        
    client.subscribe(topic)
    client.on_message = on_message


def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()
