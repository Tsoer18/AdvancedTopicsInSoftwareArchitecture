import paho.mqtt.client as mqtt
from PYmongoGetDatabase import get_database
import json

CONNECTION_STRING = "some string"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

dbname = get_database()




broker = 'mqtt5'
port = 1883


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    collection_name = dbname["sensorstate"]
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    #print(topic+" "+payload," time stamp ")

    try:
        data = json.loads(payload)  # Parse the JSON payload
        item = {
            "timestamp": data.get("timestamp"),# Access specific fields from the JSON data
            "status": data.get("status"),  
            "placementx": data.get("placementx"),
            "placementy": data.get("placementy"),
            "location": data.get("location")
        }
        collection_name.insert_one(item)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)



client2 = mqtt.Client()
client2.on_connect =on_connect

client2.username_pw_set('user1',password='1234')
client2.connect(broker,port)
client2.on_message = on_message
client2.subscribe("Sensors/+/Robots")
client2.loop_forever()
