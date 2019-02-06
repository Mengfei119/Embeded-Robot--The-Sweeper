#pwm_calibrate.py
#lab:thursday section
#author:ziqi wang(zw568) & mengfei xiong(mx224)
#function: lift up/ put down the arm by button control
from multiprocessing import Process, Queue, Value, Lock, Array
import RPi.GPIO as GPIO
import os, time
#os.system("sudo modprobe bcm2835-v4l2")
import cv2
import numpy as np 
import pygame
from pygame.locals import*
import sys
import pigpio
import subprocess 
from datetime import datetime

global p11, p21, p31, p41, p51
global setColor, hisColor

'''os.putenv('SDL_VIDEODRIVER','fbcon') 
os.putenv('SDL_FBDEV','/dev/fb1') 
os.putenv('SDL_MOUSEDRV','TSLIB') 
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')''' 
pygame.init()
#pygame and GPIO initial
'''pygame.mouse.set_visible(False)'''

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
p31=GPIO.PWM(6,1000/c)
p31.start(100 * dc/(dc +20.0 ))

initial = initial_right
dc = initial
c = 20.0 + dc
p41=GPIO.PWM(16,1000/c)
p41.start(100 * dc/(dc +20.0 ))

#Change the speed of a servo
def set_speed(speed, p):
     global p31,p41
     if p == p31:
         init = initial_left
     else:
         init = initial_right
     dc = 0
     c = 20 + dc
     p.ChangeFrequency(1000/c)
     p.ChangeDutyCycle(100 * dc/(20+dc))
     
def set_speed(speed, p):
     global p31,p41
     if p == p31:
         init = initial_left
     else:
         init = initial_right
     dc=init + 0.2 * speed
     c=20+dc
     p.ChangeFrequency(1000/c)
     p.ChangeDutyCycle(100 * dc/(20+dc))

def lift_up():
    global p11, p21
    initial_left1 = 2
    initial_right1 = 1.2
    
    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p11.ChangeFrequency(1000/c1) #frequency 
    p11.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    
    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p21.ChangeFrequency(1000/c1) #frequency 
    p21.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    print"lift up"
    time.sleep(0.2)
    
def put_down():
    global p11, p21
    initial_left1 = 1.3
    initial_right1 = 1.9
    
    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p11.ChangeFrequency(1000/c1) #frequency 
    p11.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    
    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p21.ChangeFrequency(1000/c1) #frequency 
    p21.ChangeDutyCycle(100 * dc1/(dc1 +20.0 )) # calculate the dc
    print"put down"
    time.sleep(0.2)

def arm_initial():
    global p11, p21
    GPIO.setup(5, GPIO.OUT)# pin2 as the servo GPIO output
    GPIO.setup(19, GPIO.OUT)

    initial_left1 = 2
    initial_right1 = 1.2

    initial1 = initial_left1
    dc1 = initial1
    c1 = 20.0 + dc1
    p11=GPIO.PWM(5,1000/c1)
    p11.start(100 * dc1/(dc1 +20.0 ))

    initial1 = initial_right1
    dc1 = initial1
    c1 = 20.0 + dc1
    p21=GPIO.PWM(19,1000/c1)
    p21.start(100 * dc1/(dc1 +20.0 ))

def look_up():
    global p5
    p5=pi_hw.hardware_PWM(12,50,76000)
    print "look up"
    
def look_down():
    global p5
    p5=pi_hw.hardware_PWM(12,50,92000)   
    print "look down"   

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
    #pygame.draw.rect(screen,black,((0,0),(200, 240)))
    for my_text, text_pos in my_buttons.items():
         text_surface = my_font.render(my_text, True, white)
         rect = text_surface.get_rect(center=text_pos)
         screen.blit(text_surface, rect)

    for my_text, text_pos in my_button.items():
        text_surface = my_font.render(my_text, True, white)
        rect = text_surface.get_rect(center= text_pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()

def run_test(color):
    global flagRotate
    global setColor
    last_contour_receive_time = 0
    starttime_ms = 0
    start_datetime = datetime.now()
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
    cap = cv2.VideoCapture(0)
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
    
    current_time = datetime.now()
    delta_time = current_time - start_datetime
    delta_time_ms = delta_time.total_seconds()*1000
  
    if((delta_time_ms > 30) and send_frame_queue.qsize() < 2):
            start_datetime = currenttime
            send_frame_queue.put(mask)
    if ((not receive_contour_queue.empty())):
        last_contour_receive_time = time.time()
        mask = receive_contour.queue.get()
        #detect blue
        res = cv2.bitwise_and(frame, frame, mask=mask)
        
        #cnts = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #draw two direction lines
        cv2.line(frame, (200,0), (200,400), (0,0,255), 2)
        cv2.line(frame, (400,0), (400,400), (0,0,255), 2)
        
        
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
            
            #*******************************
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
                    
                if cX > 150 and cX < 450 and area > 15000 and setColor % 2 == 1:
                        
                        set_speed(0, p3)
                        set_speed(0, p4)
                        print "reached drop position"
                        #time.sleep(0.2)
                        lift_up()
                        print"drop it"
                        drop_react()
                        setColor = (setColor + 1) % 4
                        print "setColor " + str(setColor)
                        #look_down()
                        p5=pi_hw.hardware_PWM(12,50,92000)   
                        print "look down"   
                        time.sleep(0.1)
                        set_speed(-0.3, p3)
                        set_speed(0.3, p4)
                        time.sleep(0.5)
                        set_speed(-0.3, p3)
                        set_speed(-0.3, p4)
                        print"180 "
                        time.sleep(1.0)
                        print"180 "
                        time.sleep(1.5)
                
                elif cX > 200 and cX < 400 and area > 40000 and setColor % 2 == 0 and time_flag == 1:
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
                        time.sleep(0.1)
                    
                    
                elif (cX > 200 and cX < 400 and area <= 35000 and setColor % 2 == 0) or (cX > 200 and cX < 400 and area <= 15000 and setColor % 2 == 1):
                    set_speed(0.2, p3)
                    set_speed(-0.2, p4)
                    print"reaching "
                    time.sleep(0.1)
                    set_speed(0, p3)
                    set_speed(0, p4)
                    time.sleep(0.05)
               
                elif cX >= 400:
                    set_speed(-0.15, p3)
                    set_speed(-0.15, p4)
                    print">400"
                    time.sleep(0.1)
                    set_speed(0, p3)
                    set_speed(0, p4)
                    time.sleep(0.2)
                
                elif cX <= 200:
                    set_speed(0.15, p3)
                    set_speed(0.15, p4)
                    print"<200"
                    time.sleep(0.1)
                    set_speed(0, p3)
                    set_speed(0, p4)
                    time.sleep(0.2)
                #start_run_time = time.time()
                #time_flag = 0
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

def grab_frame(run_flag, send_frame_queue, receive_contour_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock):
    #set initial arm mode:lift up
    #set initial camera mode:look_down
    arm_initial()
    #camera_servo_initial()
    global p5
    p5=pi_hw.hardware_PWM(12,50,92000)
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
                 if x>200:
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

def process_frame_1(run_flag, send_frame_queue, receive_contour_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock):
    while(run_flag.value):
        starttime = datetime.now()
        starttime_ms = starttime.second * 1000 + starttime.microsecond/1000
        if((not send_frame_queue.empty()) and (p_start_turn.value == 1)):
            mask = send_frame_queue.get()
            p_start_turn.value = 1
            mask = cv2.erode(mask, None, iterations=4)
            mask = cv2.dilate(mask, None, iterations=4)
            #detect blue
            res = cv2.bitwise_and(frame, frame, mask=mask)
            #cnts = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            receive_contour_queue.put(contours)
        else:
            time.sleep(0.03)
        currenttime = datetime.now()
        currenttime_ms = currenttime.second * 1000 + currenttime.microsecond/1000
    print("quiting processor 1")
    

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

my_font = pygame.font.Font(None, 40) 
my_buttons ={'start':(280, 40), 'quit':(280, 200)} 
 

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
p5=pi_hw.hardware_PWM(12,50,92000)
#initial variable
flagRotate = True
setColor = 0
hisColor = 0
color = 0
start_flag = 0

if __name__ == '__main__':
    run_flag = Value('i' , 1)
    p_start_turn = Value('i' ,1)
    p_end_turn = Value('i', 1)
    send_frame_queue = Queue()
    receive_contour_queue = Queue()
    p_start_lock = Lock()
    p_end_lock = Lock()
    
    p0 = Process(target = grab_frame, args=(run_flag, send_frame_queue, receive_contour_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock))
    p1 = Process(target = grab_frame, args=(run_flag, send_frame_queue, receive_contour_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock))
    
    p0.start()
    p1.start()

    p0.join()
    p1.join()
    
    p11.stop()
    p21.stop()
    p31.stop()
    p41.stop()
    pi_hw.stop()
    GPIO.cleanup()
    cap.release()
        
        
        
