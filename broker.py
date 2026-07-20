import time
import paho.mqtt.client as mqtt
import datetime



BROKER_IP = "10.80.203.109"  
SUB_TOPIC = "pi3_to_pi2"     
PUB_TOPIC = "pi2_to_pi3"     

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker on Pi 1!")
        client.subscribe(SUB_TOPIC) 
        print(f"Subscribed to: {SUB_TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"\n[RECEIVED from Pi 3]: {payload}")
    if "Ping" in payload:
        print("Sending reply back to Pi 3...")
        client.publish(PUB_TOPIC, "Ping reply from Pi 2!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER_IP, 1883, 60)
client.loop_start()

try:
    while True:
        cur_med_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[patient ate medicine on]: {cur_med_taken}") #for us to see
        message_to_send = (f"[patient ate medicine on]: {cur_med_taken}")
        client.publish(PUB_TOPIC, message_to_send)
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
    client.disconnect()