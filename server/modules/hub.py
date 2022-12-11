from time import time
from threading import Timer
import os
import sys

# add self modules path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../utilities')

from db import log, getUser

def hub(
    queue_cmd_to_hub,
    queue_cmd_from_display,
    queue_cmd_to_display,
    queue_cmd_to_motor,
    queue_cmd_from_face_recg,
    queue_cmd_to_face_recg,
    dict_live_photo
    ):

    def openDoor(banner, static_var = {"schedualed_close_time": 0}):
        queue_cmd_to_motor.put({"type": 'OPEN'})
        queue_cmd_to_display.put({"type": 'WELCOME', "data": banner})
        static_var['schedualed_close_time'] = time() + 6

        def closeDoor():
            print('sssss')
            if time() > static_var['schedualed_close_time']:
                queue_cmd_to_motor.put({"type": 'CLOSE'})
                queue_cmd_to_display.put({"type": 'INIT'})
        
        Timer(7.0, closeDoor).start()

    def recgFail(banner, static_var = {"schedualed_close_time": 0}):
        queue_cmd_to_display.put({"type": 'FAILURE', "data": banner})
        static_var['schedualed_close_time'] = time() + 6

        def init():
            if time() > static_var['schedualed_close_time']:
                queue_cmd_to_display.put({"type": 'INIT'})
        
        Timer(7.0, init).start()

    def train(id):
        queue_cmd_to_display.put({"type": 'TRAIN', "data": id})
        queue_cmd_to_face_recg.put({"type": 'TRAIN LIVE', "data": id})
        cmd = queue_cmd_from_display.get()
        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
        if cmd['type'] == 'TRAIN FINISH':
            log('TRAIN', uid = id, img = dict_live_photo['png'])
        

    def recg():
        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'RECG'})
        start_time = time()
        while time() < start_time + 10:
            if not queue_cmd_from_face_recg.empty():
                cmd = queue_cmd_from_face_recg.get()
                if cmd['type'] == 'FACE OK':
                    if cmd['confidence'] > 30:
                        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
                        openDoor('Welcome %s ~~' % getUser(cmd['id'])[0][0])
                        log('RECG_SUCCESS', uid = cmd['id'], img = cmd['photo']['png'])
                        return None

        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
        recgFail('Cannot recg you!!')
        log('RECG_FAILURE', img = dict_live_photo['png'])

    """init"""
    queue_cmd_to_display.put({
        "type": 'INIT'
    })
    queue_cmd_to_motor.put({
        "type": 'CLOSE'
    })

    """loop"""
    try:
        while True:
            if not queue_cmd_to_hub.empty():
                cmd = queue_cmd_to_hub.get()
                print('queue_cmd_to_hub: ', cmd)
                if cmd['type'] == 'REMOTE_OPEN':
                    openDoor('Opened by Admin remotely!!')
                    log('REMOTE_OPEN')

                if cmd['type'] == 'TRAIN':
                    train(cmd['id'])
                

            if not queue_cmd_from_display.empty():
                cmd = queue_cmd_from_display.get()
                print('queue_cmd_from_display: ', cmd)
                if cmd['type'] == 'START RECOG':
                    recg()
    
    except KeyboardInterrupt:
        pass