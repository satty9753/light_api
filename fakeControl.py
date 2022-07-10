class LightController:
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

controller = LightController()