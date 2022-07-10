import RPi.GPIO as GPIO

class LightController:
    _instance = None 
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance 

    def __init__(self):
        self.lightOn = False
        self.pin = 23
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)

    def turnOnLight(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.lightOn = True

    def turnOffLight(self):  
        GPIO.output(self.pin, GPIO.LOW)
        self.lightOn = False