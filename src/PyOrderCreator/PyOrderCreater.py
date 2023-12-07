import paho.mqtt.client as mqtt
import json
import time
import random
import psycopg2


broker = 'mqtt5monitor'
port = 1884

def get_connection():
    try:
        return psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="db",
            port=5432,
        )
    except:
        return False


def on_message(client, userdata, msg):
    print(msg)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

def OrderCreate(client):
    while True:
        conn = get_connection()
        curr = conn.cursor()
        curr.execute("SELECT * FROM orders WHERE isdone = 'f' AND orderdeliveredtoscheduler = 'f'")
        data1 = curr.fetchone()
        if (data1 != None):
            data = {
                "orderID": data1[0],
                "Wheel": data1[4],
                "Engine": data1[5],
                "Gun": data1[6],
                "Welding": data1[7],
                "Ammo": data1[8]
            }
            payload = json.dumps(data)
            client.publish("Scheduler/order/newOrder",payload)
        conn.close()
            

        time.sleep(10)  # Send order every 8 secounds

def setorderdeliveredtoschedulertotrue(orderid):
    print("Trying to update order status in db:")
    conn = get_connection()
    curr1 = conn.cursor()
    curr1.execute("UPDATE orders SET orderdeliveredtoscheduler = 't' WHERE id = '%s'",(orderid,))
    conn.commit()
    conn.close()

def noticeOrderRecieved(client,userdata,msg):
    payload = msg.payload.decode("utf-8")
    data = json.loads(payload)
    print(data.get("Message"))
    setorderdeliveredtoschedulertotrue(data.get("orderid"))


def setorderisdontotrue(orderid):
    print("Trying to update order in db in isdone")
    conn = get_connection()
    curr1 = conn.cursor()
    curr1.execute("UPDATE orders SET isdone = 't' WHERE id = '%s'",(orderid,))
    conn.commit()
    conn.close()

def OrderisDone(client,userdata,msg):
    payload = msg.payload.decode("utf-8")
    data = json.loads(payload)
    print(data.get("Message"))
    setorderisdontotrue(data.get("orderid"))




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('user1', password= '1234')
client.message_callback_add('Scheduler/order/recievedOrder', noticeOrderRecieved)
client.message_callback_add("scheduler/order/done", OrderisDone)
client.connect(broker, port)
client.subscribe("Scheduler/#")
client.loop_start()

OrderCreate(client)
