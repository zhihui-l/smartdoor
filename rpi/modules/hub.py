"""
hub module
"""
from time import time
from threading import Timer
import os
import sys
import requests

# add self modules path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../utilities')

# import self defined utilities
from db import log, getUser, addUserIteration, getUserTrainInfo

def hub(
    queue_cmd_to_hub,
    queue_cmd_from_display,
    queue_cmd_to_display,
    queue_cmd_to_motor,
    queue_cmd_from_face_recg,
    queue_cmd_to_face_recg,
    global_shared_dict
    ):

    def openDoor(banner, static_var = {"schedualed_close_time": 0}):
        queue_cmd_to_motor.put({"type": 'OPEN'})
        Timer(0.6, lambda :queue_cmd_to_motor.put({"type": 'STOP'})).start()
        queue_cmd_to_display.put({"type": 'WELCOME', "data": banner})
        static_var['schedualed_close_time'] = time() + 6

        def closeDoor():
            if time() > static_var['schedualed_close_time']:
                queue_cmd_to_motor.put({"type": 'CLOSE'})
                queue_cmd_to_display.put({"type": 'INIT'})
                Timer(0.6, lambda :queue_cmd_to_motor.put({"type": 'STOP'})).start()
        
        Timer(7.0, closeDoor).start()

    def recgFail(banner, static_var = {"schedualed_close_time": 0}):
        queue_cmd_to_display.put({"type": 'FAILURE', "data": banner})
        static_var['schedualed_close_time'] = time() + 6

        def init():
            if time() > static_var['schedualed_close_time']:
                queue_cmd_to_display.put({"type": 'INIT'})
        
        Timer(7.0, init).start()

    def train(id):
        userInfo = getUserTrainInfo(id)
        global_shared_dict['iter'] = int(userInfo[0][1])
        queue_cmd_to_display.put({"type": 'TRAIN', "data": id, "name": userInfo[0][0]})
        queue_cmd_to_face_recg.put({"type": 'TRAIN LIVE', "data": id})
        cmd = queue_cmd_from_display.get()
        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
        if cmd['type'] == 'TRAIN FINISH':
            log('TRAIN', uid = id, img = global_shared_dict['good'])
        

    def recg():
        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'RECG'})
        start_time = time()
        while time() < start_time + 15:
            if not queue_cmd_from_face_recg.empty():
                cmd = queue_cmd_from_face_recg.get()
                if cmd['type'] == 'FACE OK':
                    if cmd['confidence'] > 60:
                        user = getUser(cmd['id'])
                        if len(user) == 1:
                            queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
                            openDoor('Welcome %s ~~' % user[0][0])
                            log('RECG_SUCCESS', uid = cmd['id'], img = global_shared_dict['good'])
                            return None


        queue_cmd_to_face_recg.put({"type": 'CHANGE STATE', "data": 'IDLE'})
        recgFail('Cannot recg you!!')
        log('RECG_FAILURE', img = global_shared_dict['live_video_frame'])


    def request():
        requests.get(url = 'https://api.yimian.xyz/mail/?subject=Access_Control_Request&body=Log_on_web_dashboard_to_decide!!&from=access_control&to='+global_shared_dict['email'])
        requests.get(url = 'https://api.yimian.xyz/mail/?subject=Access_Control_Request&body=Log_on_web_dashboard_to_decide!!&from=access_control&to='+global_shared_dict['sms']+'@vzwpix.com')
        log('REQUEST', img = global_shared_dict['live_video_frame'])

    """init"""
    queue_cmd_to_display.put({
        "type": 'INIT'
    })

    queue_cmd_to_motor.put({
        "type": 'CLOSE'
    })
    Timer(1.5, lambda :queue_cmd_to_motor.put({"type": 'STOP'})).start()

    """loop"""
    try:
        while True:
            if not queue_cmd_to_hub.empty():
                cmd = queue_cmd_to_hub.get()
                print('queue_cmd_to_hub: ', cmd)
                if cmd['type'] == 'REMOTE_OPEN':
                    openDoor('Welcome ~')
                    log('REMOTE_OPEN')

                if cmd['type'] == 'TRAIN':
                    train(cmd['id'])
                

            if not queue_cmd_from_display.empty():
                cmd = queue_cmd_from_display.get()
                print('queue_cmd_from_display: ', cmd)
                if cmd['type'] == 'START RECOG':
                    recg()
                if cmd['type'] == 'REQUEST':
                    request()


            if not queue_cmd_from_face_recg.empty():
                cmd = queue_cmd_from_face_recg.get()
                if cmd['type'] == 'FACE TRAINED':
                    addUserIteration(cmd['id'])

    except KeyboardInterrupt:
        pass