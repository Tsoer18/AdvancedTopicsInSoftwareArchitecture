import paho.mqtt.client as mqtt
import json
import time



broker = 'mqtt5monitor'
port = 1884

# Variables for response time calculation
ErrorMessageReceived = False
start_time = 0

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    global ErrorMessageReceived, start_time
    ErrorMessageReceived = True
    end_time = time.time()
    response_time = end_time - start_time
    #print(start_time)
    #print(end_time)
    print(f"Received Error response in {response_time} seconds")
    client.publish("Robots/test", "EndTest")
    print("End Test")
    client.disconnect() # disconnect gracefully
    client.loop_stop()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def Heartbeat(client):
    while(True):
        time.sleep(30)
        global ErrorMessageReceived, start_time
        ErrorMessageReceived = False
        start_time = time.time()
        client.publish("Robots/test", "StartTest")
        print("Start  Test")
        


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.subscribe("Robots/Error/NoHeartBeat/Test")
client.loop_start()

Heartbeat(client)