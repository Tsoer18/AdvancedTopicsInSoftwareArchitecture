import paho.mqtt.client as mqtt
import time
import json
import random
import datetime;



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def mock_data(client):
    while True:
        location = random.choice(["WheelR","TrackR","GunR","weldingR","AmmoR"])
        ct = str(datetime.datetime.now())

        data = {
            "status": random.choice(["ON", "OFF"]),  # Randomly select "ON" or "OFF"
            "placementx": random.uniform(0, 100),
            "placementy": random.uniform(0, 100),
            "location": location,
            "timestamp": ct
        }

        payload = json.dumps(data)
        client.publish("Sensors/"+location+"/Robots",payload)

        time.sleep(2)

broker = 'mqtt5'
port = 1883

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.loop_start()

mock_data(client)