import paho.mqtt.client as mqtt
import time
import json
import random
import datetime;

Robots = [["WheelR","Working",0],["TrackR","Working",0],["GunR","Working",0],["WeldingR","Working",0],["AmmoR","Working",0]]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def mock_data(client):
    while True:
        for i in range(len(Robots)):
            Robot = Robots[i]
            status = Robot[1] 
            if(Robot[2]== 4):
                Robot[1] = "Done"
                Robot[2] = 0
                for j in range(i + 1, len(Robots)):
                    next_robot = Robots[j]
                    next_robot[1] = "Working"
                    next_robot[2] = 0 
            else:
                if(status == "Working"):
                    Robot[2] += 1
    
            
            ct = str(datetime.datetime.now())
            location = Robot[0]
            status = Robot[1]
            data = {
                "status": status,
                "placementx": random.uniform(0, 100),
                "placementy": random.uniform(0, 100),
                "placementz": random.uniform(0, 100),
                "location": location,
                "timestamp": ct
            }
            payload = json.dumps(data)
            client.publish("Sensors/"+Robot[0]+"/Robots",payload)
            #client1.publish("Sensors/"+Robot[0]+"/Robots",payload)
               
        time.sleep(2)


broker = 'mqtt5Mongodb'
port = 1883

broker1 = 'mqtt5monitor'
port1 = 1884

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_message_Heartbeat(client, userdata, msg):
    time.sleep(0)
    print("Bread")
    client1.publish("HeartBeat/Robots","Bread")



client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.loop_start()

client1 = mqtt.Client()
client1.on_connect = on_connect
client1.username_pw_set('user1', password= '1234')
client1.message_callback_add("Robots/Heartbeat", on_message_Heartbeat)
client1.on_message = on_message
client1.connect(broker1, port1)
client1.subscribe("Robots/#")
client1.loop_start()

mock_data(client)