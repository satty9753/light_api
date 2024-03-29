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
        self.timeInterval = 0
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        #GPIO.setup(self.pin, GPIO.IN)
        self.getLightStatus()

    def turnOnLight(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.lightOn = True

    def turnOffLight(self):  
        GPIO.output(self.pin, GPIO.LOW)
        self.lightOn = False

    def getLightStatus(self):
        lightStatus = GPIO.input(self.pin)
        if lightStatus == 1:
            self.lightOn = True
        else:
            self.lightOn = False
