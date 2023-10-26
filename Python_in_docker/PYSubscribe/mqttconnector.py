import paho.mqtt.client as mqtt
import time
from threading import Thread
from PYmongoGetDatabase import get_database
import datetime;

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
    ct = datetime.datetime.now()
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    print(topic+" "+payload," time stamp " , ct)
    item_1 = {
        "timestamp" : ct,
        "payload" : payload,
    }
    collection_name.insert_one(item_1)



client2 = mqtt.Client()
client2.on_connect =on_connect

client2.username_pw_set('user1',password='1234')
client2.connect(broker,port)
client2.on_message = on_message
client2.subscribe("testtopic")
client2.loop_forever()
