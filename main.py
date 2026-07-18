import RPi.GPIO as GPIO
import time
import signal

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #GPI.BOARD

GPIO.setup(29, GPIO.OUT) #servo, GPIO 5
GPIO.setup(7,GPIO.IN) # pir sensor, GPIO4. 
GPIO.setup(11, GPIO.OUT) #11 means pin 11, GPIO 17
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# Define the pin connected to the IR Sensor's OUT wire (GPIO 23 -> pin 16)
sensor_pin = 16
GPIO.setup(sensor_pin, GPIO.IN)
# GPIO 24 (pin 18)
BUZZER_PIN = 18
GPIO.setup(18, GPIO.OUT)
# Touch sensor OUT pin connected to GPIO 25 (pin 22)
TOUCH_PIN = 22
GPIO.setup(22, GPIO.IN)


while True:

    print("Turning ON 11") #------------------------------LED
    GPIO.output(11, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(11, GPIO.LOW)

    print("Turning ON 13")
    GPIO.output(13, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(13, GPIO.LOW)

    print("Turning ON 15")
    GPIO.output(15, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(15, GPIO.LOW)

    print("Turning ON 11 and 13") #11 and 13
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(2)
    print("Turning ON 13 and 15") #13 and 15
    GPIO.output(11, GPIO.LOW)  
    GPIO.output(15, GPIO.HIGH)
    time.sleep(2)
    print("Turning ON 11 and 15") #11 15
    GPIO.output(13, GPIO.LOW)  
    GPIO.output(11, GPIO.HIGH)
    time.sleep(2)

    print("all offff") #all offfff
    GPIO.output(11, GPIO.LOW)  
    GPIO.output(15, GPIO.LOW)  
    
    time.sleep(2)

    print("pwm on") #---------------------------------------servo
    pwm=GPIO.PWM(29, 50) #GPIO 17 - pin 11, ground and 5v gpio5 - pin 29
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
        i = GPIO.input(7) #get resut of input
        if i == 1:
            print("got 1") #movement detected
        elif i == 0:
            print("got 0") #movement not detected
        time.sleep(0.2) #0.2 second pause cause why not
 





GPIO.cleanup() #general exit statement



