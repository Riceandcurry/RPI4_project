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




def leds():
    print("Turning ON GREEN (11)") 
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

    print("Turning ON RED (13)")
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

    print("Turning ON BLUE (15)")
    GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)

    print("Turning ON 11 and 13") #11 and 13
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    print("Turning ON 13 and 15") #13 and 15
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)  
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    print("Turning ON 11 and 15") #11 15
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)  
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    time.sleep(2)

    print("all offff") #all offfff
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)  
    GPIO.output(RED_LED_PIN, GPIO.LOW)  

def servo():
    print("pwm on") 
    pwm=GPIO.PWM(SERVO_PIN, 50) #GPIO 17 - pin 11, ground and 5v gpio5 - pin 29
    pwm.start(0)
    pwm.ChangeDutyCycle(5) # left -45?
    time.sleep(1)
    pwm.ChangeDutyCycle(7.5) # neutral position
    time.sleep(1)
    pwm.ChangeDutyCycle(10) # right +45 ?
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


def touch():
    print("\n--- Starting Touch Sensor Test ---")
    global touch_count
    touch_count = 0 # reset counter
    
    # Set up interrupt listener
    GPIO.add_event_detect(TOUCH_PIN, GPIO.RISING, callback=touch_callback, bouncetime=300)
    
    print("Touch the sensor 3 times to proceed...")
    while touch_count < 3:
        time.sleep(0.1)
        
    print("sensor count 3 reached")

def ir():
    print("IR Sensor Active. Press Ctrl+C to exit.") 
    ir_count = 0
    while (ir_count < 5):
        # Check if the signal goes LOW (detects an obstacle)
        if GPIO.input(IR_PIN) == GPIO.LOW:
            print("Object Detected!")
            ir_count += 1
        else:
            print("Path Clear")
        time.sleep(0.5)
    print("ir sensor end")
        
def pir(duration_seconds=10): #change for actual code
    print("pir sensor start")
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        motion = GPIO.input(PIR_PIN)
        if motion == 1:
            print("motion! (got 1)")
        else:
            print("no motion (got 0)")
        time.sleep(0.5)

while True:
    leds()
    servo()
    buzzer()
    touch()
    ir()
    pir(duration_seconds=10) # Test PIR for 10 seconds before looping back
    
    print("\n==============================")
    print("Iteration complete. Restarting loop...")
    print("==============================\n")
    time.sleep(1)