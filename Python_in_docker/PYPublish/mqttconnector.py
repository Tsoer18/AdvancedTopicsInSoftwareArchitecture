import paho.mqtt.client as mqtt
import time
import json
import random
import datetime;

locations = ["WheelR","TrackR","GunR","WeldingR","AmmoR"]
WheelRStatus = "Working"
TrackRStatus = "Working"
GunRStatus = "Working"
WeldingRStatus = "Working"
AmmoRStatus = "Working"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def mock_data(client):
    while True:
        for location in locations:
            ct = str(datetime.datetime.now())
            status = WeldingRStatus
            data = {
                "status": status, # Randomly select "ON" or "OFF"
                "placementx": random.uniform(0, 100),
                "placementy": random.uniform(0, 100),
                "placementz": random.uniform(0, 100),
                "location": location,
                "timestamp": ct
            }
            payload = json.dumps(data)
            client.publish("Sensors/"+location+"/Robots",payload)
            client1.publish("Sensors/"+location+"/Robots",payload)        
        time.sleep(2)

broker = 'mqtt5Mongodb'
port = 1883

broker1 = 'mqtt5monitor'
port1 = 1884

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_message_Heartbeat(client1, userdata, msg):
    print("Bread")


client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.loop_start()

client1 = mqtt.Client()
client1.on_connect = on_connect
client1.username_pw_set('user1', password= '1234')
client1.message_callback_add("Robots/Heartbeat/WheelR", on_message_Heartbeat)
client1.on_message = on_message
client1.connect(broker1, port1)
client1.subscribe("Robots/#")
client1.loop_start()

mock_data(client)