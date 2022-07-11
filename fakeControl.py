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
       pass

    def turnOnLight(self):
        self.lightOn = True

    def turnOffLight(self):  
        self.lightOn = False

    def getLightStatus(self):
        self.lightOn = True