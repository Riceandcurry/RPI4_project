import RPi.GPIO as GPIO
import time
import signal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #GPI.BOARD

SERVO_PIN = 29
PIR_PIN = 7
GREEN_LED_PIN = 11
BLUE_LED_PIN = 15
RED_LED_PIN = 13
BUZZER_PIN = 18
TOUCH_PIN = 22
IR_PIN = 16


GPIO.setup(SERVO_PIN, GPIO.OUT) #servo, GPIO 5
GPIO.setup(PIR_PIN,GPIO.IN) # pir sensor, GPIO4. 
GPIO.setup(GREEN_LED_PIN, GPIO.OUT) #11 means pin 11, GPIO 17
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

# Define the pin connected to the IR Sensor's OUT wire (GPIO 23 -> pin 16)

GPIO.setup(IR_PIN, GPIO.IN)
# GPIO 24 (pin 18)

GPIO.setup(BUZZER_PIN, GPIO.OUT)
# Touch sensor OUT pin connected to GPIO 25 (pin 22)

GPIO.setup(TOUCH_PIN, GPIO.IN)


while True:

    print("Turning ON 11") #------------------------------LED
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

    print("Turning ON 13")
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

    print("Turning ON 15")
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
    
    time.sleep(2)

    print("pwm on") #---------------------------------------servo
    pwm=GPIO.PWM(SERVO_PIN, 50) #GPIO 17 - pin 11, ground and 5v gpio5 - pin 29
    pwm.start(0)
    pwm.ChangeDutyCycle(5) # left -45?
    time.sleep(1)
    pwm.ChangeDutyCycle(7.5) # neutral position
    time.sleep(1)
    pwm.ChangeDutyCycle(10) # right +45 ?
    time.sleep(1)

    
    pwm.stop()  #GPIO servo motor works
    print("pwm off")
    print("pir")

    print("Buzzer test started.") #--------------------------buzzer

    print("Buzzer ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    
    print("Buzzer OFF")
    GPIO.output(BUZZER_PIN, GPIO.LOW)

    print("Buzzer test completed.")
    
    count = 0 #----------------------------------touch
    def touch_detected(channel):
        global count
        count += 1
        print("Touch detected! Count:", count)

    # Detect rising signal: from Low to HIGH
    GPIO.add_event_detect(
        TOUCH_PIN,
        GPIO.RISING,
        callback=touch_detected,
        bouncetime=300
    )

    print("Touch sensor test started...")
    print("Touch the sensor to see the output.")
    while(count < 3):
        time.sleep(0.1)
    print("\nTarget reached (3 counts)!")

    print("IR Sensor Active. Press Ctrl+C to exit.") #---------------------IR
    ir_count = 0
    while (ir_count < 5):
        # Check if the signal goes LOW (detects an obstacle)
        if GPIO.input(sensor_pin) == GPIO.LOW:
            print("Object Detected!")
            ir_count += 1
        else:
            print("Path Clear")
        time.sleep(0.5)
        


    while True: #--------------------------------------------PIR
        i = GPIO.input(PIR_PIN) #get resut of input
        if i == 1:
            print("got 1") #movement detected
        elif i == 0:
            print("got 0") #movement not detected
        time.sleep(0.2) #0.2 second pause cause why not
 





GPIO.cleanup() #general exit statement



