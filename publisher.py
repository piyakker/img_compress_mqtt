import time
import random
import argparse

import paho.mqtt.client as mqtt

def main(args):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.connect(host=args['ip'], port=args['port'])
    client.loop_start()

    # Intervally send topic message
    try:
        while True:
            # Fill the payload
            if args['topic'] == 'msg':
                payload = 'hello'
            elif args['topic'] == 'random':
                payload = random.randint(1,10)
            # Publish the message to topic
            client.publish(topic=args['topic'], payload=payload)
            time.sleep(1)
    except KeyboardInterrupt as e:
        client.loop_stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    parser.add_argument("--topic",
                        default="msg",
                        choices=['msg', 'random'],
                        help="Availabel information to publish")
    args = vars(parser.parse_args())
    main(args)
