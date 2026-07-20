import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import datetime


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #GPI.BOARD

SERVO_PIN = 29
PIR_PIN = 7
GREEN_LED_PIN = 11
RED_LED_PIN = 13
BLUE_LED_PIN = 15
BUZZER_PIN = 18
TOUCH_PIN = 22
IR_PIN = 16


GPIO.setup(SERVO_PIN, GPIO.OUT) #servo, GPIO 5
GPIO.setup(PIR_PIN,GPIO.IN) # pir sensor, GPIO4. 
GPIO.setup(GREEN_LED_PIN, GPIO.OUT) #green led, GPIO 17
GPIO.setup(BLUE_LED_PIN, GPIO.OUT) #
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(TOUCH_PIN, GPIO.IN)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
pwm.start(0)

medicine_time = None
scheduled_med_time = None  # Expected format: "HH:MM"
meds_cycle_triggered = False

BROKER_IP = "10.80.203.109"  
SUB_TOPIC = "pi3_to_pi2"     
PUB_TOPIC = "pi2_to_pi3"     


def led_waiting():
    print("time for med")
    GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)

def led_taken_meds():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def led_not_taken_meds():
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(RED_LED_PIN, GPIO.LOW)    

def servo_open():
    print("Servo opening...") 
    print("Servo: 90 degrees left")
    pwm.ChangeDutyCycle(2.5) 
    time.sleep(1)
    pwm.ChangeDutyCycle(0)# prevent jitter

def servo_close():
    print("Servo closing...")
    print("Servo: 90 degrees right")
    pwm.ChangeDutyCycle(12.5) 
    time.sleep(1)
    pwm.ChangeDutyCycle(0)    # prevent jitter
    print("servo closed")

def buzzer(): #1 second buzzer
    print("Buzzer ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    
    print("Buzzer OFF")
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def touch_callback(channel):
    global touch_count
    touch_count += 1
    print(f"Touch detected! Count: {touch_count}")


def touch(timeout, target_touches): #current touch 1
    print(f"[TOUCH] You have {timeout} seconds to touch the sensor {target_touches} times!")
    touch_counts = 0
    start_time = time.time()
    last_state = GPIO.LOW
    
    while (time.time() - start_time) < timeout:
        current_state = GPIO.input(TOUCH_PIN)
        if current_state == GPIO.HIGH and last_state == GPIO.LOW:
            touch_counts += 1
            print(f"  Touch registered! ({touch_counts}/{target_touches})")
            time.sleep(0.2) 
            if touch_counts >= target_touches:
                return True
        last_state = current_state
        time.sleep(0.05) 
    return False

def ir(target_clearances, timeout):
    print(f"IR Sensor Active. Waiting for {target_clearances} clear readings (Max {timeout}s)...") 
    clear_count = 0
    start_time = time.time()
    
    while clear_count < target_clearances:
        if (time.time() - start_time) >= timeout:
            print(f"IR window timed out after {timeout} seconds. Moving on...")
            return False
        if GPIO.input(IR_PIN) == GPIO.HIGH:
            clear_count += 1
            print(f"Path Clear! ({clear_count}/{target_clearances})")
            time.sleep(0.4) 
        else:
            print("Object Detected (Blocked)")
            time.sleep(0.2)
    print("ir sensor end")
    return True
        
def pir(motion_threshold): #change for testing, 10?
    print("pir active, waiting ..............")
    motion_counter = 0
    while motion_counter < motion_threshold:
        motion = GPIO.input(PIR_PIN)
        if motion == 1:
            motion_counter += 1
            print(f" Motion detected! (Activity Level: {motion_counter}/{motion_threshold})")
            time.sleep(0.1) 
        else:
            time.sleep(0.2)
            
    print("motion threshold reached")


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
    try: #CHANGED CODEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE when tested 
        data = json.loads(payload)
        if "medicine_time" in data:
            scheduled_med_time = data["medicine_time"]
            meds_cycle_triggered = False  # Reset flag so the new scheduled time can execute
            print(f"[SCHEDULE UPDATED]: Next medicine cycle set for {scheduled_med_time}")
    except json.JSONDecodeError:
        print("[ERROR]: Payload received was neither a 'Ping' nor a valid JSON string.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER_IP, 1883, 60)
client.loop_start()

try:
    while True:
        # Check current time
        now = datetime.datetime.now()
        current_time_str = now.strftime("%H:%M")
        
        # only when i asked
        if scheduled_med_time and (current_time_str == scheduled_med_time) and not meds_cycle_triggered:
            print(f"\n[ALERT] Current time matches schedule ({current_time_str})! Starting routine...")
            
            pir(15) 
            led_waiting()
            buzzer()
            servo_open()
            
            ir_success = ir(5, 5.0)

            if not ir_success:
                print("IR Path did not clear!")
                led_not_taken_meds()
                servo_close()
            else:
                print("IR Path cleared")
                success = touch(5.0, 1)     
                if success:
                    print("Meds successfully taken!")
                    cur_med_taken = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[patient ate medicine on]: {cur_med_taken}")
                    
                    # Notify Pi 3 over MQTT
                    message_to_send = f"[patient ate medicine on]: {cur_med_taken}"
                    client.publish(PUB_TOPIC, message_to_send)
                    
                    led_taken_meds()
                    servo_close()
                else:
                    print("Meds not taken")
                    led_not_taken_meds()
                    servo_close()
            
            print("\nCycle finished. Resetting flag and waiting for next schedule changes...")
            meds_cycle_triggered = True  # Prevent looping again within the same minute
            
        # Reset the trigger flag when the minute passes so it can accept the same time tomorrow
        if scheduled_med_time and (current_time_str != scheduled_med_time):
            meds_cycle_triggered = False

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping application and cleaning up GPIO...")
    pwm.stop()
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()