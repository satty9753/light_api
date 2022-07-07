import RPi.GPIO as GPIO
from time import sleep

lightOn = False

def turnOnLight():
    GPIO.setmode(GPIO.BCM)
    pin = 23
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    lightOn = True

def turnOffLight():
    GPIO.setmode(GPIO.BCM)
    pin = 23
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    lightOn = False