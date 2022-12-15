"""
display module
"""
# import system modules
import os
import sys

# add self modules path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../utilities/display')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../assets')

# import other modules
from enum import Enum
import numpy as np
import pygame
from pygame.locals import *   # for event MOUSE variables
from time import localtime, strftime
from imgConvert import *

# import self-defined modules
from screen import Screen
from text import Text
from vbutton import VButton
from imgBoard import ImgBoard

def display(queue_cmd_from_display, queue_cmd_to_display, global_shared_dict):
    # set env var
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb0')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    # Flags
    FPS = 100

    # PiTFT Page states
    PAGE = Enum('page', ('DEFAULT', 'WELCOME', 'FAILURE', 'RECOGNITION', 'TRAIN'))

    # set page flag to default 
    page = PAGE.DEFAULT

    # init pygame
    pygame.init()
    # hide cursor on piTFT
    pygame.mouse.set_visible(False)
    # clock obj to control FPS
    clock = pygame.time.Clock()

    # create a screen
    screen = Screen(width = 320, height = 240, background = (0, 0, 0))

    # create a open button on screen
    button_open = VButton(
        text = Text('OPEN'),
        position = screen%(50, 80),
        size = (80, 40),
        enable = False
    )

    button_finish = VButton(
        text = Text('FINISH'),
        position = screen%(85, 80),
        size = (80, 40),
        enable = False
    )


    button_request = VButton(
        text = Text('Request'),
        position = screen%(50, 80),
        size = (80, 40),
        enable = False
    )

    # banner text
    banner = Text(text='', position = screen%(50,40))

    train_text_uid = Text(text='', position = screen%(85,17))
    train_text_name = Text(text='', position=screen%(85, 37))
    train_text_iter = Text(text='', position=screen%(85, 57))

    text_date = Text(text = '', position = screen%(23,5))

    live_video = ImgBoard(
        position = screen%(35, 55),
        size = 110,
        enable = False
    )


    icon_lock = ImgBoard(enable = False)

    # define pages
    def clear_screen():
        button_open.enable = False
        button_request.enable = False
        button_finish.enable = False
        live_video.enable = False
        banner.text = ''
        banner.refresh()
        banner.enable = False
        train_text_iter.enable = False
        train_text_name.enable = False
        train_text_uid.enable = False
        icon_lock.h=2
        icon_lock.enable = False

    def page_default():
        clear_screen()
        page = PAGE.DEFAULT
        banner.enable = True
        button_open.enable = True
        banner.text = 'Access Co   trol'
        banner.size = 43
        banner.position = screen%(50,40)
        banner.refresh()
        icon_lock.position = screen%(66, 40)
        icon_lock.size = 13
        icon_lock.enable = True
        icon_lock.refresh(img = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/../assets/lock.png'))


    def page_welcome(data):
        clear_screen()
        page = PAGE.WELCOME
        banner.enable = True
        banner.size = 37
        banner.position = screen%(50, 80)
        banner.text = data
        banner.refresh()
        icon_lock.position = screen%(50, 50)
        icon_lock.size = 35
        icon_lock.enable = True
        icon_lock.h = 6
        icon_lock.refresh(img = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/../assets/success.png'))



    def page_failure(data):
        clear_screen()
        page = PAGE.FAILURE
        button_request.enable = True
        icon_lock.position = screen%(50, 45)
        icon_lock.size = 45
        icon_lock.enable = True
        icon_lock.refresh(img = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/../assets/failure.png'))

    def page_recognition():
        clear_screen()
        page = PAGE.RECOGNITION
        banner.enable = True
        live_video.enable = True
        icon_lock.position = screen%(85, 50)
        icon_lock.size = 35
        icon_lock.enable = True
        icon_lock.refresh(img = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/../assets/lock1.png'))


    def page_train(id, name):
        clear_screen()
        page = PAGE.TRAIN
        live_video.enable = True
        button_finish.enable = True
        train_text_uid.text = 'uid: '+str(id)
        train_text_uid.refresh()
        train_text_name.text = str(name)
        train_text_name.refresh()
        train_text_iter.enable = True
        train_text_name.enable = True
        train_text_uid.enable = True

    try:
        while True:

            clock.tick(FPS) 

            # draw on the screen
            screen.clear()

            screen << text_date

            if 'live_video_frame' in global_shared_dict:
                img = imgc_base642bytesio(global_shared_dict['live_video_frame'])
                if img:
                    live_video.refresh(img = pygame.image.load(img))
                    screen << live_video
                    train_text_iter.text = 'iter: '+str(global_shared_dict['iter'])
                    train_text_iter.refresh()

            screen << button_open
            screen << button_request
            screen << button_finish
            screen << banner
            screen << train_text_iter
            screen << train_text_name
            screen << train_text_uid
            screen << icon_lock

            pygame.display.flip()        # display workspace on screen


            text_date.text = strftime("%m/%d/%Y %H:%M:%S",localtime())
            text_date.refresh()

            if not queue_cmd_to_display.empty():
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
                    page_train(cmd['data'], cmd['name'])

            # touch event
            for event in pygame.event.get():    
                if(event.type is MOUSEBUTTONUP):            
                    pos = pygame.mouse.get_pos() 
                    # when open button is pressed
                    if (button_open.collidepoint(pos) ):
                        page_recognition()
                        queue_cmd_from_display.put({
                            "type": 'START RECOG'
                        })

                    if (button_request.collidepoint(pos)):
                        button_request.enable = False
                        queue_cmd_from_display.put({
                            "type": 'REQUEST'
                        })
                        button_request.enable = False
                        banner.enable = True
                        banner.text = 'Request Sent!!'
                        banner.position = screen%(50, 80)
                        banner.size = 37
                        banner.refresh()


                    if (button_finish.collidepoint(pos)):
                        page_default()
                        queue_cmd_from_display.put({
                            "type": 'TRAIN FINISH'
                        })


    except KeyboardInterrupt:
        pygame.quit()
