#pwm_calibrate.py
#lab:thursday section
#author:ziqi wang(zw568) & mengfei xiong(mx224)
#function: lift up/ put down the arm by button control
import cv2
import time
import RPi.GPIO as GPIO
import numpy as np
global p1, p2, p3, p4

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)# pin2 as the servo GPIO output
GPIO.setup(19, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)# pin2 as the servo GPIO output
GPIO.setup(16, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def arm_initial():
    #set up servo arms, 'lift up' motion
    initial_left = 1.5
    initial_right = 1.5

    initial = initial_left
    dc = initial
    c = 20.0 + dc
    p1=GPIO.PWM(5,1000/c)
    p1.start(100 * dc/(dc +20.0 ))

    initial = initial_right
    dc = initial
    c = 20.0 + dc
    p2=GPIO.PWM(19,1000/c)
    p2.start(100 * dc/(dc +20.0 ))
    
def wheel_initial():
    left_init = 1.5 
    right_init = 1.5 
    init = 1.5 
    dc=init 
    c=20+dc 
    p3=GPIO.PWM(6, 1000/c) 
    p3.start(100 * dc/(20+dc)) 
    p4=GPIO.PWM(16, 1000/c) 
    p4.start(100 * dc/(20+dc))

def GPIO17_callback(channel):

    wheel_mode('rotate')
    print ("in searching mode- rotating")
    time.sleep(0.1)


'''
def GPIO17_callback(channel):
    initial_left = 2
    initial_right = 1.2
    
    initial = initial_left
    dc = initial
    c = 20.0 + dc
    p1.ChangeFrequency(1000/c) #frequency 
    p1.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    
    initial = initial_right
    dc = initial
    c = 20.0 + dc
    p2.ChangeFrequency(1000/c) #frequency 
    p2.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    
    time.sleep(0.1)
    
def GPIO22_callback(channel):
    initial_left = 1.2
    initial_right = 2
    
    initial = initial_left
    dc = initial
    c = 20.0 + dc
    p1.ChangeFrequency(1000/c) #frequency 
    p1.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    
    initial = initial_right
    dc = initial
    c = 20.0 + dc
    p2.ChangeFrequency(1000/c) #frequency 
    p2.ChangeDutyCycle(100 * dc/(dc +20.0 )) # calculate the dc
    
    time.sleep(0.1)
    print "put down"'''
    
#Change the speed of a continuous servo 
def set_speed(speed, p):
     global p1,p2
     if p == p3:
         init = left_init
     else:
         init = right_init
         dc = init + 0.2 * speed
         c = 20 + dc
         p.ChangeFrequency(1000/c)
         p.ChangeDutyCycle(100 * dc/(20+dc))

def wheel_mode(mode):
    if mode == 'stop':
        set_speed(0, p3)
        set_speed(0, p4)
    if mode == 'forward' :
        set_speed(-0.5, p3)
        set_speed(0.5,  p4)
    if mode == 'roatte':
        set_speed(0.5, p3)
        set_speed(0, p4)
        
#main


arm_initial()
wheel_initial()
cap = cv2.VideoCapture(0)
frame = cap.read()

# if there is no object right in the front
# rotate in clockwise to find the object
GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback, bouncetime=20)       

'''
cv2.imshow("Frame", frame)
key = cv2.waitKey(1) & 0xFF
counter += 1'''

# Break the loop if "q" is pressed.
if cv2.waitKey(1) & 0xFF == ord("q"):
    exit()
    
time.sleep(10)
p1.stop()
p2.stop()
p3.stop()
p4.stop()
GPIO.cleanup()

'''
# arm mode change
GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback, bouncetime=20)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=20) 
time.sleep(100)

p1.stop()
p2.stop()
GPIO.cleanup()'''


'''
# camera use
# Create a VideoCapture class object to stream video from Pi camera
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    cv2.imshow('capture',frame)
    #if q pressed break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''
