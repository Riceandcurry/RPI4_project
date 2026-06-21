import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.OUT) #servo
GPIO.setup(7,GPIO.IN) # pir sensor

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
    i = GPIO.input(7) #get resut of input
    if i == 1:
        print("got 1") #movement detected
    elif i == 0:
        print("got 0") #movement not detected
    time.sleep(0.2) #0.2 second pause cause why not

GPIO.cleanup() #general exit statement



