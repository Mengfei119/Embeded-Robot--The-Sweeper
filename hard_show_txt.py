#sweeper.py
#lab:thursday section in 2018 Fall
#developed by Mengfei Xiong(mx224) and Ziqi Wang(zw568)
#final project of ECE5725
#function: run automatically to collect and throw different trash
#into different trash cans

import RPi.GPIO as GPIO
import os, time
import cv2
import numpy as np 
import pygame
from pygame.locals import*
import sys
import pigpio
import subprocess 
 
global p1, p2, p3, p4, p5
global setColor, hisColor

os.putenv('SDL_VIDEODRIVER','fbcon') 
os.putenv('SDL_FBDEV','/dev/fb1') 
os.putenv('SDL_MOUSEDRV','TSLIB') 
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen') 
pygame.init()
#pygame and GPIO initial
pygame.mouse.set_visible(False)

GPIO.setmode(GPIO.BCM)
pi_hw = pigpio.pi()
pi_hw.set_mode(12,pigpio.OUTPUT)
GPIO.setup(6, GPIO.OUT)# pin2 as the servo GPIO output
GPIO.setup(16, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#initial stop mode
initial_left = 1.5
initial_right = 1.5

initial = initial_left
dc = initial
c = 20.0 + dc
p3=GPIO.PWM(6,1000/c)
p3.start(100 * dc/(dc +20.0 ))

initial = initial_right
dc = initial
c = 20.0 + dc
p4=GPIO.PWM(16,1000/c)
p4.start(100 * dc/(dc +20.0 ))

#Change the speed of a servo
def set_speed(speed, p):
     global p3,p4
     if p == p3:
         init = initial_left
     else:
         init = initial_right
     dc = 0
     c = 20 + dc
     p.ChangeFrequency(1000/c)
     p.ChangeDutyCycle(100 * dc/(20+dc))
     
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

#change the mode of arms
def lift_up():
    global p1, p2
    initial_left1 = 2
    initial_right1 = 1.2
    
    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p1.ChangeFrequency(1000/c1) #frequency 
    p1.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    
    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p2.ChangeFrequency(1000/c1) #frequency 
    p2.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    print"lift up"
    time.sleep(0.2)
    
def put_down():
    global p1, p2
    initial_left1 = 1.3
    initial_right1 = 1.9
    
    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p1.ChangeFrequency(1000/c1) #frequency 
    p1.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    
    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p2.ChangeFrequency(1000/c1) #frequency 
    p2.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    print"put down"
    time.sleep(0.2)

def arm_initial():
    global p1, p2
    GPIO.setup(5, GPIO.OUT)# pin2 as the servo GPIO output
    GPIO.setup(19, GPIO.OUT)

    initial_left1 = 2
    initial_right1 = 1.2

    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p1=GPIO.PWM(5,1000/c1)
    p1.start(100 * dc1/(dc1 +20.0 ))

    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p2=GPIO.PWM(19,1000/c1)
    p2.start(100 * dc1/(dc1 +20.0 ))

#change the mode of camera by controlling the servo
def look_up():
    global p5
    p5=pi_hw.hardware_PWM(12,50,76000)
    print "look up"
    
def look_down():
    global p5
    p5=pi_hw.hardware_PWM(12,50,91500)
    print "look down"

#draw text on the screen
def lock_react():
    my_font = pygame.font.Font(None, 50)
    my_button = { 'get trash':(80, 180)}
    size = width, height = 320,240
    black=0,0,0
    screen=pygame.display.set_mode(size)
    screen.fill(black)# Erase the Work space
    for my_text, text_pos in my_buttons.items():
         text_surface = my_font.render(my_text, True, white)
         rect = text_surface.get_rect(center=text_pos)
         screen.blit(text_surface, rect)

    for my_text, text_pos in my_button.items():
        text_surface = my_font.render(my_text, True, white)
        rect = text_surface.get_rect(center= text_pos)
        screen.blit(text_surface, rect)
   
    pygame.display.flip()

def drop_react():
    my_font = pygame.font.Font(None, 50)
    my_button = { 'drop trash':(80, 180)}
    screen.fill(black) # Erase the Work space
    #pygame.draw.rect(screen,black,((0,0),(150, 240)))
    for my_text, text_pos in my_buttons.items():
         text_surface = my_font.render(my_text, True, white)
         rect = text_surface.get_rect(center=text_pos)
         screen.blit(text_surface, rect)

    for my_text, text_pos in my_button.items():
        text_surface = my_font.render(my_text, True, white)
        rect = text_surface.get_rect(center= text_pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()


#function of object detection alg.
def run_test(color):
    time.sleep(0.2)
    global flagRotate
    global setColor
    #get a frame
    if flagRotate == True:
        print "1"
        set_speed(0.2, p3)
        set_speed(0.2, p4)
        time.sleep(0.1)
        set_speed(0, p3)
        set_speed(0, p4)
        time.sleep(0.2)
    else:
        print"2"
        set_speed(0, p3)
        set_speed(0, p4)
        time.sleep(0.1)
    ret, frame = cap.read()
    cv2.resize(frame,(320,160))
    #cv2.imshow('Capture', frame)
    
    #change to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #get mask for colors
    if setColor == 0:
        mask = cv2.inRange(hsv, lower_green, upper_green)
    if setColor == 1:
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    if setColor == 2:
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if setColor == 3:
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
    
        
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
    #cv2.imshow('Mask', mask)
    
    #detect blue
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    #cnts = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    #draw two direction lines
    cv2.line(frame, (150,0), (150,450), (0,0,255), 2)
    cv2.line(frame, (450,0), (450,450), (0,0,255), 2)
    
    
    if len(cnts) != 0:
        #find the largest contour in the mask
        c = max(cnts, key=cv2.contourArea)
        
        #((x,y),radius) = cv2.minEnclosingCircle(c)
        cv2.drawContours(res, cnts, -1, 255, 3)
        area = cv2.contourArea(c)
        print"area" + str(area)
        
        #calculate x,y coordinate of center
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #draw the center of the object
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        #run to the blue object thrshold 15000
        if area > 1000:
            start_run_time = time.time()
            #current_run_time = time.time()
            flagRotate = False
            #print"3 " +str(area)
            set_speed(0, p3)
            set_speed(0, p4)
            time.sleep(0.1)
         
            print "setColor " + str(setColor)
            time_flag = 1
            
            #if the trash can is in the middle of the image and the area is larger than threshold
            #lift up the arm and make the camera look up
            if cX > 150 and cX < 450 and area > 15000 and setColor % 2 == 1:
                    
                    set_speed(0, p3)
                    set_speed(0, p4)
                    print "reached drop position"
                    lift_up()
                    print"drop it"
                    drop_react()
                    setColor = (setColor + 1) % 4
                    print "setColor " + str(setColor)
                    #look_down()
                    p5=pi_hw.hardware_PWM(12,50,91500)   
                    print "look down"
                    set_speed(-0.3, p3)
                    set_speed(0.3, p4)
                    time.sleep(0.5)
                    set_speed(-0.3, p3)
                    set_speed(-0.3, p4)
                    print"180 "
                    time.sleep(1.0)
                    print"180 "
                    time.sleep(1.5)
            #if the trash in the middle of the image and the area is larger than threshold
            #put down the arm and make the camera look down
            elif cX > 150 and cX < 450 and area > 45000 and setColor % 2 == 0 and time_flag == 1:
                    set_speed(0, p3)
                    set_speed(0, p4)
                    print "reached object"
                    put_down()
                    time.sleep(0.1)
                    print"got it"
                    lock_react()
                    setColor = (setColor + 1) % 4
                    print "setColor " + str(setColor)
                    #look_up()
                    p5=pi_hw.hardware_PWM(12,50,76000)   
                    print "look down"
                
            #if the target is in the middle of the image and the area is smaller than threshold
            #go forward
            elif (cX > 150 and cX < 450 and area <= 35000 and setColor % 2 == 0) or (cX > 150 and cX < 450 and area <= 15000 and setColor % 2 == 1):
                set_speed(0.2, p3)
                set_speed(-0.2, p4)
                print"reaching "
                time.sleep(0.15)
                set_speed(0, p3)
                set_speed(0, p4)
                time.sleep(0.05)
            #if the target is in the left of the image
            #turn left
            elif cX >= 450:
                set_speed(-0.2, p3)
                set_speed(-0.2, p4)
                print">450"
                time.sleep(0.1)
                set_speed(0, p3)
                set_speed(0, p4)
                time.sleep(0.15)
            #if the target is in the right of the image
            #turn right
            elif cX <= 150:
                set_speed(0.2, p3)
                set_speed(0.2, p4)
                print"<150"
                time.sleep(0.1)
                set_speed(0, p3)
                set_speed(0, p4)
                time.sleep(0.15)
            #if there'no target in the image
            #start rotate
            else:
                flagRotate = 0
                print"cannot find target rotate again"
    else:
        #if cannot found target -> rotate
        flagRotate = True
        time.sleep(0.2)
        print"change rotate" + str(flagRotate)
    # display the image with center
    #cv2.imshow("Image", frame)

#main

# set environment variable to play on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(0.25)
size = width, height = 320,240
black=0,0,0
white= 255,255,255
text_pos=(80,180)
screen=pygame.display.set_mode(size)

#draw buttons on PiTFT
my_font = pygame.font.Font(None, 40) 
my_buttons ={'start':(280, 40), 'quit':(280, 150)} 
 

my_font = pygame.font.Font(None, 50)
my_button = { 'lock trash':(80, 180)}
screen.fill(black) # Erase the Work space

for my_text, text_pos in my_buttons.items():
     text_surface = my_font.render(my_text, True, white)
     rect = text_surface.get_rect(center=text_pos)
     screen.blit(text_surface, rect)
pygame.display.flip()

#get picture
cap = cv2.VideoCapture(0)
#set color range
lower_blue = np.array([100, 43, 46])
upper_blue = np.array([264, 255, 255])

lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

lower_green = np.array([29, 86, 6])
upper_green = np.array([64, 255, 255])

lower_purple = np.array([125, 43, 46])
upper_purple = np.array([155, 255, 255])


#set initial arm mode:lift up
#set initial camera mode:look_down
arm_initial()
#camera_servo_initial()
global p5
p5=pi_hw.hardware_PWM(12,50,91500)
#initial variable
flagRotate = True
setColor = 0
hisColor = 0
color = 0
start_flag = 0

while True:
    #set 23 as bail out button
    if(not GPIO.input(23) ):
        break
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
             pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
             pos = pygame.mouse.get_pos()
             x,y  = pos
             if x>150:
                 #"start"button is pressed
                 if y<100:
                     start_flag = 1
                     color = hisColor
                     run_test(color)
                 #"stop"button is pressed 
                 else:
                     start_flag = 0
                     hisColor = setColor
                     set_speed(0, p3)
                     set_speed(0, p4)
                     #stop_react()
    if start_flag == 1:
        run_test(color)
        print"set" + str(setColor)
#clear
p1.stop()
p2.stop()
p3.stop()
p4.stop()
pi_hw.stop()
GPIO.cleanup()
cap.release()

