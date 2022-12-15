import RPi.GPIO as GPIO
import time as time

def motor(queue_cmd_to_motor):
 

    PIN = 13


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    
    servo = GPIO.PWM(PIN,500)
    servo.start(0)

    try:
        while True:
            cmd = queue_cmd_to_motor.get()
            if cmd['type'] == 'OPEN':
                servo.ChangeDutyCycle(20)

            if cmd['type'] == 'CLOSE':
                servo.ChangeDutyCycle(70)

            if cmd['type'] == 'STOP':
                servo.ChangeDutyCycle(0)
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()