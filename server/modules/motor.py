import RPi.GPIO as GPIO
import time as time



def motor(queue_cmd_to_motor):
 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    
    servo = GPIO.PWM(26,500)

    try:
        while True:
            cmd = queue_cmd_to_motor.get()
            if cmd['type'] == 'OPEN':
                servo.start(0)
                servo.ChangeDutyCycle(20)
                time.sleep(1.5)
                servo.stop()
            if cmd['type'] == 'CLOSE':
                servo.start(0)
                servo.ChangeDutyCycle(70)
                time.sleep(1.5)
                servo.stop()
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()