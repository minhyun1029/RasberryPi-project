import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
AIN1 = 13
AIN2 = 15
PWMA = 12

GPIO.setup(AIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(AIN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PWMA, GPIO.OUT, initial=GPIO.LOW)

p = GPIO.PWM(PWMA, 100)

p.start(0)

try:
    while 1:
        
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        p.ChangeDutyCycle(50)  
        time.sleep(0.5) 

       
        p.ChangeDutyCycle(0)
        time.sleep(1)  

        
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        p.ChangeDutyCycle(50)  
        time.sleep(0.5)  

        
        p.ChangeDutyCycle(0)
        time.sleep(1)  

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
