import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #GPI.BOARD
#GPIO.setup(11, GPIO.OUT) #servo
#GPIO.setup(7,GPIO.IN) # pir sensor
#GPIO.setup(11, GPIO.OUT) #ir led/rgb
#GPIO.setup(7, GPIO.IN)  #ir reciever
RED_PIN = 11
GREEN_PIN = 13
BLUE_PIN = 15

# Set pins as outputs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Initialize PWM on all 3 pins at 100Hz
red_pwm = GPIO.PWM(RED_PIN, 100)
green_pwm = GPIO.PWM(GREEN_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_PIN, 100)

# Start with LED off (0% duty cycle)
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def set_color(red, green, blue):
    # Pass values from 0 to 100 for intensity
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

try:
    while True:
        set_color(100, 0, 0)   # Red
        time.sleep(1)
        set_color(0, 100, 0)   # Green
        time.sleep(1)
        set_color(0, 0, 100)   # Blue
        time.sleep(1)
        set_color(50, 0, 50)   # Purple
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    # Clean up PWM and GPIO state
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()

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

"""
while True:
    i = GPIO.input(7) #get resut of input
    if i == 1:
        print("got 1") #movement detected
    elif i == 0:
        print("got 0") #movement not detected
    time.sleep(0.2) #0.2 second pause cause why not
"""

print("hello worlddd")

"""
pwm = GPIO.PWM(11, 38000)
pwm.start(50)  # 50% duty cycle

print("IR transmitter ON (38kHz)")

while True:
        if GPIO.input(7) == 0:
            print("detected")
        elif GPIO.input(7) == 1:
            print("nothin!")
        time.sleep(0.05)
"""
GPIO.cleanup() #general exit statement



