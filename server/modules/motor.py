import RPi.GPIO as GPIO
import time as time
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
 
servo = GPIO.PWM(26,500)
servo.start(0)
def motor(queue_cmd_to_motor):
    try:
        cmd = queue_cmd_to_motor.get()
        print(cmd)
        if cmd['type'] == 'OPEN':
            servo.ChangeDutyCycle(20)
        if cmd['type'] == 'CLOSE':
            servo.ChangeDutyCycle(70)
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()