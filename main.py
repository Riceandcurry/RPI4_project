import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #GPI.BOARD
GPIO.setup(29, GPIO.OUT) #servo
GPIO.setup(7,GPIO.OUT) # pir sensor, GPIO4. change to OUT
#GPIO.setup(11, GPIO.OUT) #ir led/rgb
#GPIO.setup(7, GPIO.IN)  #ir reciever

GPIO.setup(11, GPIO.OUT) #11 means pin 11, GPIO 17
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)



while True:

    print("Turning ON 11")
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

    print("pwm on")
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
    '''
    while True:
        i = GPIO.input(7) #get resut of input
        if i == 1:
            print("got 1") #movement detected
        elif i == 0:
            print("got 0") #movement not detected
        time.sleep(0.2) #0.2 second pause cause why not
    '''
    pwm = GPIO.PWM(7, 38000) #og 11
    pwm.start(50)  # 50% duty cycle

    print("IR transmitter ON (38kHz)")

    while True:
            if GPIO.input(7) == 0:
                print("detected")
            elif GPIO.input(7) == 1:
                print("nothin!")
            time.sleep(0.05)

GPIO.cleanup() #general exit statement



