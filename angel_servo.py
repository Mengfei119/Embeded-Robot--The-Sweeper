#pwm_calibrate.py
#lab:thursday section
#author:ziqi wang(zw568) & mengfei xiong(mx274)
#function: lift up/ put down the arm by button control

import RPi.GPIO as GPIO
import time
global p5 

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)# pin2 as the servo GPIO output
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

initial_camera = 1.7

initial = initial_camera
dc = initial
c = 20.0 + dc
p5=GPIO.PWM(26,1000/c)
p5.start(100 * dc/(dc +20.0 ))


def GPIO23_callback(channel):
    initial_camera = 1.4
    
    initial = initial_camera
    dc = initial
    c = 20.0 + dc
    p5.ChangeFrequency(1000/c) #frequency 
    p5.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    

    print "look up"

    #time.sleep(5)
    
def GPIO27_callback(channel):
    initial_camera = 1.7
    
    initial = initial_camera
    dc = initial
    c = 20.0 + dc
    p5.ChangeFrequency(1000/c) #frequency 
    p5.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    

    time.sleep(0.2)
    print "look down"
    
GPIO.add_event_detect(23,GPIO.FALLING, callback=GPIO23_callback, bouncetime=20)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=20) 

time.sleep(100)

p5.stop()
GPIO.cleanup()

