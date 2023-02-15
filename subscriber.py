import argparse

import paho.mqtt.client as mqtt

def on_connect(client,userdata, flags, rc):
    print("Connection generated!")

def on_message(client, obj, msg):
    print(f"Message : {(msg.payload).decode('utf-8') }")

def main(args):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host=args['ip'], port=args['port'])
    client.subscribe('msg', 0)
    client.subscribe('random', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    main(args)
