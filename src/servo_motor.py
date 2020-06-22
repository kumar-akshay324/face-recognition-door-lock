import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self):
        self.servo_pin = 17
        self.status_pin = 3

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        GPIO.setup(self.status_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, 50) # GPIO 17 for PWM with 50Hz
        self.setAngle(0)

    def setAngle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.status_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.status_pin, False)
        self.pwm.ChangeDutyCycle(0)

    def lockDoor(self):
        self.setAngle(90)
        print ("Door Locked")
    
    def unlockDoor(self):
        self.setAngle(0)
        print ("Door Unlocked")