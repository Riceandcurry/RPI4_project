import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.OUT) #servo
GPIO.setup(11, GPIO.IN)  #pir sensor 
GPIO.setup(7,GPIO.OUT) # pir sensor

"""
pwm=GPIO.PWM(11, 50) #GPIO 14, ground and 5v
pwm.start(0)
pwm.ChangeDutyCycle(5) # left -45?
time.sleep(1)
pwm.ChangeDutyCycle(7.5) # neutral position
time.sleep(1)
pwm.ChangeDutyCycle(10) # right +45 ?
time.sleep(1)

pwm.stop()  #GPIO servo motor works
"""



print("hello worlddd")


while True:
    GPIO.output(7,1)  #output high to the pin 7
    time.sleep(1)
    GPIO.output(7,0)  #output low to pin 7
    time.sleep(1)
    i = GPIO.input(11)
    if i == 1:
        print("got 1")
    elif i == 0:
        print("got none")
    else:
        print("none")

GPIO.cleanup()



