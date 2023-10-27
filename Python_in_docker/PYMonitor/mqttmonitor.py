import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

broker = 'mqtt5'
port = 1883

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    print(topic+" "+payload)

    try:
        data = json.loads(payload)  # Parse the JSON payload
        status = data.get("status")
        if(status == "OFF"):
            data = {
                "location": data.get("location"),
                "timestamp": data.get("timestamp")
            }
            payload = json.dumps(data)
            print("Robot is off here is data: " + payload)
            client.publish("Monitor/Sensor") #needs to be connectid to olivers website
            

    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.on_message = on_message
client.subscribe("Sensors/+/Robots")
client.loop_forever()