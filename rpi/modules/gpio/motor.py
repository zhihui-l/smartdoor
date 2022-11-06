
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Motor():
    PIN = {
        'IN1': 0,
        'IN2': 0,
        'PWM': 0
    }
    obj_pwm = None
    callback = None
    __speed = 0
    __stop = False
    def __init__(self, IN1, IN2, PWM, freq = 50, callback = lambda speed:None):
        self.PIN = {}
        self.PIN['IN1'] = IN1
        self.PIN['IN2'] = IN2
        self.PIN['PWM'] = PWM
        self.callback = callback
        # gpio setup
        [GPIO.setup(pin, GPIO.OUT) for pin in self.PIN.values()] 
        # pwm setup
        self.pwm_obj = GPIO.PWM(self.PIN['PWM'], freq)
        self.pwm_obj.start(0)
    
    def __setattr__(self, name, value):
        if name == 'speed':
            self.setSpeed(value)
        else:
            self.__dict__[name] = value

    def setSpeed(self, value):
        if self.__speed != value:
            self.callback(value)
        if self.__stop:
            return
        if value > 0:
            GPIO.output(self.PIN['IN1'], GPIO.HIGH)
            GPIO.output(self.PIN['IN2'], GPIO.LOW)
        else:
            GPIO.output(self.PIN['IN1'], GPIO.LOW)
            GPIO.output(self.PIN['IN2'], GPIO.HIGH)
        self.pwm_obj.ChangeDutyCycle(abs(value))
        self.__speed = value

    def stop(self):
        self.__stop = True
        self.pwm_obj.ChangeDutyCycle(0)
    def resume(self):
        self.__stop = False
        print(self.__speed)
        self.pwm_obj.ChangeDutyCycle(abs(self.__speed))