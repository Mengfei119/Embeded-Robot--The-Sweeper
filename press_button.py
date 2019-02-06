
import pygame
from pygame.locals import* 
import os
import RPi.GPIO as GPIO
import time

# set environment variable to play on Pi
'''
os.putenv('SDL_VIDEODRIVER','fbcon') 
os.putenv('SDL_FBDEV','/dev/fb1') 
os.putenv('SDL_MOUSEDRV','TSLIB') 
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen') '''

#pygame and GPIO initial
pygame.init()
#pygame.mouse.set_visible(False) 
GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
my_button = { 'trash1':(80, 180)}
screen.fill(black) # Erase the Work space

for my_text, text_pos in my_buttons.items():
     text_surface = my_font.render(my_text, True, white)
     rect = text_surface.get_rect(center=text_pos)
     screen.blit(text_surface, rect)
pygame.display.flip()

def start_react():
    my_font = pygame.font.Font(None, 50)
    my_button = { 'trash1':(80, 180)}
    screen.fill(black)# Erase the Work space
    for my_text, text_pos in my_buttons.items():
         text_surface = my_font.render(my_text, True, white)
         rect = text_surface.get_rect(center=text_pos)
         screen.blit(text_surface, rect)
    
    #pygame.draw.rect(screen,black,((0,0),(200, 240)))

    for my_text, text_pos in my_button.items():
        text_surface = my_font.render(my_text, True, white)
        rect = text_surface.get_rect(center= text_pos)
        screen.blit(text_surface, rect)
   
    pygame.display.flip()

def stop_react():
    my_font = pygame.font.Font(None, 50)
    my_button = { 'trash2':(80, 180)}
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

#def GPIO23_callback(channel):
 #   exit(0)

while True:
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
                         start_react()
                     #"stop"button is pressed 
                     else:
                         stop_react()
   


#GPIO.add_event_detect(17,GPIO.FALLING, callback=GPIO17_callback, bouncetime=20)
#GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=20) 
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=20) 
time.sleep(100)
