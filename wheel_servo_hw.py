#pwm_calibrate.py
#lab:thursday section
#author:ziqi wang(zw568) & mengfei xiong(mx224)
#function: lift up/ put down the arm by button control

import RPi.GPIO as GPIO
import time
import sys
import pigpio

global p3, p4

GPIO.setmode(GPIO.BCM)

pi_hw = pigpio.pi()

pi_hw.set_mode(6,pigpio.OUTPUT)
pi_hw.set_mode(16,pigpio.OUTPUT)

#pi_hw.hardware_PWM(6,50,0)
#pi_hw.hardware_PWM(16,50,0)

time.sleep(0.1)

GPIO.setup(6, GPIO.OUT)# pin2 as the servo GPIO output
GPIO.setup(16, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#initial stop mode
initial_left = 1.5
initial_right = 1.5

initial = initial_left
dc = initial
c = 20.0 + dc
p3=pi_hw.hardware_PWM(6,50,1000/c)
p3.start(100 * dc/(dc +20.0 ))

initial = initial_right
dc = initial
c = 20.0 + dc
p4=pi_hw.hardware_PWM(16,50,1000/c)
p4.start(100 * dc/(dc +20.0 ))

#Change the speed of a servo 
def set_speed(speed, p):
     global p3,p4
     if p == p3:
         init = initial_left
     else:
         init = initial_right
     dc=init + 0.2 * speed
     c=20+dc
     p.ChangeFrequency(1000/c)
     p.ChangeDutyCycle(100 * dc/(20+dc))
     

def GPIO17_callback(channel):
    set_speed(0.1, p3)
    set_speed(0.1, p4)
    time.sleep(0.1)
    print "stop rotating"

    #time.sleep(5)
    
def GPIO22_callback(channel):
    set_speed(0, p3)
    set_speed(0, p4)
    #time.sleep(0.1)
    print "clockwise rotating"
    
GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback, bouncetime=20)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=20) 

time.sleep(100)

p3.stop()
p4.stop()
pi_hw.stop()
GPIO.cleanup()

