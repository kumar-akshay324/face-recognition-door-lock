import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self):
        self.servo_pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)

        pwm = GPIO.PWM(servo_pin, 50) # GPIO 17 for PWM with 50Hz
        self.setAngle(0)

    def setAngle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(3, False)
        pwm.ChangeDutyCycle(0)

    def lockDoor(self):
        self.setAngle(90)
    
    def unlockDoor(self):
        self.setAngle(0)