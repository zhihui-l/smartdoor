
import os, io
import sys
import numpy as np

from PIL import Image

from imgConvert import *

# add self modules path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../utilities')

from cv import detect_face, recg_face, label_face, train_face, retrain_face



def face_recg(dict_live_photo, queue_cmd_from_face_recg, queue_cmd_to_face_recg, queue_photo_from_camera):

    STATE = 'IDLE' # IDLE, RECG, TRAIN
    ID_TRAINING = 8

    try:

        while True:

            if not queue_cmd_to_face_recg.empty():
                cmd = queue_cmd_to_face_recg.get()
                if cmd['type'] == 'CHANGE STATE':
                    STATE = cmd['data']

                if cmd['type'] == 'TRAIN LIVE':
                    ID_TRAINING = cmd['data']
                    STATE = 'TRAIN'

            img = queue_photo_from_camera.get()
            img, faces, faces_position, HAVE_MODEL = detect_face(img)

            if HAVE_MODEL and len(faces) == 1:
                id, confidence = recg_face(faces[0])
                img = label_face(img, faces_position[0], id, int(confidence))

            dict_live_photo['png'] = imgc_cv2base64(img)
            

            if HAVE_MODEL and len(faces) == 1:

                if STATE == 'RECG':
                    queue_cmd_from_face_recg.put({
                        "type": 'FACE OK',
                        "id": id,
                        "confidence": confidence
                    })

            if len(faces) == 1:
                dict_live_photo['good'] =dict_live_photo['png']
                if STATE == 'TRAIN':
                    train_face(ID_TRAINING, faces[0])
                    queue_cmd_from_face_recg.put({
                        "type": 'FACE TRAINED',
                        "id": ID_TRAINING,
                        "face": faces[0]
                    })
                    dict_live_photo['iter']+=1


    except KeyboardInterrupt:
        pass