
# import system modules
import os
import sys

# add self modules path
sys.path.append('modules/display')
sys.path.append('modules/gpio')
sys.path.append('modules/sys')

# import other modules
from enum import Enum
import numpy as np
import pygame
from pygame.locals import *   # for event MOUSE variables


# import self-defined modules
from screen import Screen
from button import Button
from text import Text
from vbutton import VButton


# set env var
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


# Flags
FPS = 100
# PiTFT Page states
PAGE = Enum('page', ('DEFAULT', 'WELCOME', 'FAILURE'))

# set page flag to default 
page = PAGE.DEFAULT

# init pygame
pygame.init()
# hide cursor on piTFT
pygame.mouse.set_visible(False)
# clock obj to control FPS
clock = pygame.time.Clock()

# create a screen
screen = Screen(width = 320, height = 240)

# create a open button on screen
button_open = VButton(
    text = Text('OPEN'),
    position = screen%(50, 80),
    size = (80, 40)
)


# create retry and request buttons on screen
button_retry = VButton(
    text = Text('Retry'),
    position = screen%(20, 80),
    size = (80, 40),
    enable = False
)
button_request = VButton(
    text = Text('Request'),
    position = screen%(80, 80),
    size = (80, 40),
    enable = False
)

# banner text
banner = Text(text='Please look at the camera!', position = screen%(50,20))




while True:
    clock.tick(FPS) 

    # draw on the screen
    screen.clear()
    screen << button_open
    screen << button_retry
    screen << button_request
    screen << banner
    pygame.display.flip()        # display workspace on screen





    # touch event
    for event in pygame.event.get():        
        if(event.type is MOUSEBUTTONUP):            
            pos = pygame.mouse.get_pos() 
            # when open button is pressed
            if (button_open.collidepoint(pos)):
                button_open.enable = False;
                if False:
                    page = PAGE.WELCOME
                    banner.text = 'Welcome {username}!!'
                    banner.refresh()
                else:
                    page = PAGE.FAILURE
                    banner.text = 'No face matched!!'
                    banner.refresh()
                    button_request.enable = True
                    button_retry.enable = True

            # when button is pressed
            if (button_retry.collidepoint(pos)):
                button_retry.enable = False;
                button_request.enable = False;
                page = PAGE.DEFAULT
                banner.text = 'Please look at the camera..'
                banner.refresh()
                button_open.enable = True

            if (button_request.collidepoint(pos)):
                banner.text = 'No internet connection!!'
                banner.refresh()
            
