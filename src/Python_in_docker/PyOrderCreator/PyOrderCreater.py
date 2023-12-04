import paho.mqtt.client as mqtt
import json
import time
import random


broker = 'mqtt5monitor'
port = 1884



def on_message(client, userdata, msg):
    print(msg)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def OrderCreate(client):
    while True:
        data = {
            "Wheel": random.choice(["Wheel", "Track", "BoatPart"]),
            "Engine": random.choice(["V8", "Truckv12", "L8"]),
            "Gun": random.choice(["80mm", "90mm", "2x60mm"]),
            "Welding": random.choice(["Welding", "Rivets", "Bolts"]),
            "Ammo": random.choice(["ArmorPerice", "Trace", "Exploding"])
        }
        payload = json.dumps(data)
        client.publish("Scheduler/order/newOrder",payload)
        time.sleep(10)  # Send order every 8 secounds


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.loop_start()

OrderCreate(client)
