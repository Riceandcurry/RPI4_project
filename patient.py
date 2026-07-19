import RPi.GPIO as GPIO
import time
import signal

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
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(TOUCH_PIN, GPIO.IN)

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


def servo():
    print("pwm on") 
    pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency (20ms period)
    pwm.start(0)
    
    #(-90°)
    print("Servo: 90 degrees left")
    pwm.ChangeDutyCycle(2.5) 
    time.sleep(1)
    
    #(0°)
    print("Servo: Neutral position")
    pwm.ChangeDutyCycle(7.5) 
    time.sleep(1)
    
    #(+90°)
    print("Servo: 90 degrees right")
    pwm.ChangeDutyCycle(12.5) 
    time.sleep(1)
    
    pwm.stop()
    print("pwm off")

def buzzer():
    print("Buzzer ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    
    print("Buzzer OFF")
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def touch_callback(channel):
    global touch_count
    touch_count += 1
    print(f"Touch detected! Count: {touch_count}")


def touch(timeout, target_touches):
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
        
def pir(motion_threshold): #change for actual code
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





while True:
    pir(15) # pir only comes backe
    led_waiting()
    buzzer()
    servo()
    ir_success = ir(5,5.0)

    if not ir_success:
        print("IR Path did not clear!")
        led_not_taken_meds()
        continue 
    else:
        print("IR Path cleared")
        success = touch(5.0,3)     
        if success:
            print("taken meds!")
            led_taken_meds()
        else:
            print("not taken meds")
            led_not_taken_meds()
        
    print("\nCycle finished. Resetting back to PIR scan stage...")
    time.sleep(1)
