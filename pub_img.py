import time
import argparse
from paho.mqtt import client as mqtt_client
broker = 'broker.hivemq.com'
port = 1883
topic = "photos"
client_id = 'your client id'


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


def publish(client, filename):
    with open(f"./images/{filename}", 'rb') as file:
        filecontent = file.read()
        byteArr = bytearray(filecontent)
        print(byteArr)
        result = client.publish(topic, byteArr, 2)
    msg_status = result[0]
    if msg_status == 0:
        print(f"message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")


def main(args):
    client = connect_mqtt()
    client.loop_start()
    publish(client, args['img'])
    time.sleep(5)
    client.loop_stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img')
    args = vars(parser.parse_args())
    main(args)
