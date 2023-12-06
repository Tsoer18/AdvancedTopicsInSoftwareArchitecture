import paho.mqtt.client as mqtt
import json
import time
import psycopg2

broker = 'mqtt5monitor'
port = 1884

# Variables for response time calculation
beat_received = False
start_time = 0

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    global beat_received, start_time
    beat_received = True
    end_time = time.time()
    response_time = end_time - start_time
    #print(start_time)
    #print(end_time)
    #print(f"Received heartbeat response in {response_time} seconds")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
def scan_database():
    print("test")

def workingLoop(client):
    while True:
        global beat_received, start_time
        beat_received = False
        start_time = time.time()
        client.publish("Robots/Heartbeat", "dough")
        print("dough")
        while not beat_received:
            if (time.time() - start_time) > 1.5:  # Check if 1.5 seconds have passed
                print("Response not received within 1.5 seconds")
                client.publish("Robots/Error/NoHeartBeat","No Dough")
                time.sleep(10)
                client.publish("Robots/Heartbeat", "dough")
                start_time = time.time()
                print("dough")

        time.sleep(2)

database_connection = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password="postgres")
cur = database_connection.cursor()
cur.execute("SELECT * FROM orders;")
allOrders = cur.fetchall
print(allOrders)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('user1', password= '1234')
client.connect(broker, port)
client.subscribe("HeartBeat/Robots")
client.loop_start()

