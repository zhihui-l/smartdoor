
# import system modules
import os
import sys

# add self modules path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../utilities/display')

# import other modules
from enum import Enum
import numpy as np
import pygame
from pygame.locals import *   # for event MOUSE variables

from imgConvert import *

# import self-defined modules
from screen import Screen
from text import Text
from vbutton import VButton
from imgBoard import ImgBoard

def display(queue_cmd_from_display, queue_cmd_to_display, dict_live_photo):
    print('display')
    # set env var
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb0')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


    # Flags
    FPS = 100
    # PiTFT Page states
    PAGE = Enum('page', ('DEFAULT', 'WELCOME', 'FAILURE', 'RECOGNITION', 'TRAIN'))
    print('display5')
    # set page flag to default 
    page = PAGE.DEFAULT

    # init pygame
    pygame.init()
    # hide cursor on piTFT
    pygame.mouse.set_visible(False)
    # clock obj to control FPS
    clock = pygame.time.Clock()
    print('display6')
    # create a screen
    screen = Screen(width = 320, height = 240)
    print('display8')
    # create a open button on screen
    button_open = VButton(
        text = Text('OPEN'),
        position = screen%(50, 80),
        size = (80, 40),
        enable = False
    )

    button_finish = VButton(
        text = Text('FINISH'),
        position = screen%(85, 50),
        size = (80, 40),
        enable = False
    )

    print('display9')

    button_request = VButton(
        text = Text('Request'),
        position = screen%(50, 80),
        size = (80, 40),
        enable = False
    )
    print('display7')
    # banner text
    banner = Text(text='', position = screen%(50,20))
    print('display2')


    live_video = ImgBoard(
        position = screen%(35, 50),
        size = 110,
        enable = False
    )


    def clear_screen():
        button_open.enable = False
        button_request.enable = False
        button_finish.enable = False
        live_video.enable = False
        banner.text = ''
        banner.refresh()
        banner.enable = False

    def page_default():
        clear_screen()
        page = PAGE.DEFAULT
        banner.enable = True
        button_open.enable = True
        banner.text = 'Press Open button to begin recg..'
        banner.refresh()


    def page_welcome(data):
        clear_screen()
        page = PAGE.WELCOME
        banner.enable = True
        banner.text = data
        banner.refresh()


    def page_failure(data):
        clear_screen()
        page = PAGE.FAILURE
        banner.enable = True
        button_request.enable = True
        banner.text = data
        banner.refresh()

    def page_recognition():
        clear_screen()
        page = PAGE.RECOGNITION
        banner.enable = True
        live_video.enable = True

    def page_train():
        clear_screen()
        page = PAGE.TRAIN
        live_video.enable = True
        button_finish.enable = True


    try:
        print('display3')
        while True:

            clock.tick(FPS) 

            # draw on the screen
            screen.clear()
            screen << button_open
            screen << button_request
            screen << button_finish
            screen << banner

            if 'png' in dict_live_photo:
                img = imgc_base642bytesio(dict_live_photo['png'])
                if img:
                    live_video.refresh(img = pygame.image.load(img))
                    screen << live_video
            pygame.display.flip()        # display workspace on screen

            if not queue_cmd_to_display.empty():
                print('in10')
                cmd = queue_cmd_to_display.get()
                print(cmd)
                if cmd['type'] == 'WELCOME':
                    page_welcome(cmd['data'])
                if cmd['type'] == 'FAILURE':
                    page_failure(cmd['data'])
                if cmd['type'] == 'INIT':
                    page_default()
                if cmd['type'] == 'RECOG':
                    page_recognition()
                if cmd['type'] == 'TEXT':
                    banner.text = cmd['data']
                    banner.refresh()
                if cmd['type'] == 'TRAIN':
                    page_train()

            # touch event
            for event in pygame.event.get():    
                print('in2')    
                if(event.type is MOUSEBUTTONUP):            
                    pos = pygame.mouse.get_pos() 
                    # when open button is pressed
                    if (button_open.collidepoint(pos) ):
                        page_recognition()
                        print('in')
                        queue_cmd_from_display.put({
                            "type": 'START RECOG'
                        })

                    if (button_request.collidepoint(pos)):
                        banner.text = 'No internet connection!!'
                        banner.refresh()

                    if (button_finish.collidepoint(pos)):
                        page_default()
                        queue_cmd_from_display.put({
                            "type": 'TRAIN FINISH'
                        })


    except KeyboardInterrupt:
        print('qqqqqqqqqqqqqqqqqqqqq')
        pygame.quit()
