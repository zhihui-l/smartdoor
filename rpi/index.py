###################################

### author: Yimian Liu and Zhihui Liu ###

### Date: Dec 15 2022 ############

##################################

import multiprocessing as mp
from flask import Flask, request, jsonify, send_file, Response
import sys, os

# add self-defined library's dir to sys path
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/modules')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/utilities')

# import self-defined modules
from display import display
from hub import hub
from motor import motor
from face_recg import face_recg
from camera import camera

# import self-defined utilities
from imgConvert import *
import db

# multiprocessing queues for IPC among modules 
queue_photo_from_camera = mp.Queue()
queue_cmd_from_display = mp.Queue()
queue_cmd_to_display = mp.Queue()
queue_cmd_to_motor = mp.Queue()
queue_cmd_from_face_recg = mp.Queue()
queue_cmd_to_face_recg = mp.Queue()
queue_cmd_to_hub = mp.Queue()

# multiprocessing dict for some globally shared data
global_shared_dict = (mp.Manager()).dict()
global_shared_dict['live_video_frame'] = ''
global_shared_dict['good'] = ''
global_shared_dict['iter'] = 0

# Get Admin email from local file
f = open('/var/EMAIL')
data = f.read()
global_shared_dict['email'] = data
f.close()

# Get admin phone number from local file
f = open('/var/SMS')
data = f.read()
global_shared_dict['sms'] = data
f.close()

# define processes
process = {
    "camera": mp.Process(target=camera, args=(queue_photo_from_camera,)),
    "display": mp.Process(target=display, args=(queue_cmd_from_display, queue_cmd_to_display, global_shared_dict)),
    "motor": mp.Process(target=motor, args=(queue_cmd_to_motor,)),
    "face_recg": mp.Process(target=face_recg, args=(global_shared_dict, queue_cmd_from_face_recg, queue_cmd_to_face_recg, queue_photo_from_camera)),
    "hub": mp.Process(target=hub, args=(
        queue_cmd_to_hub,
        queue_cmd_from_display, 
        queue_cmd_to_display, 
        queue_cmd_to_motor,
        queue_cmd_from_face_recg,
        queue_cmd_to_face_recg,
        global_shared_dict))
}

# start processes
for p in process.values():
    p.start()


############################
#    Flask API Gateway 
############################

app = Flask(__name__)

@app.route("/api/addUser")
def api_addUser():
    id = db.addUser(request.args.get('name'))
    return jsonify({
        "status": True,
        "id": id
    })


@app.route("/api/getUser")
def api_getUser():
    return jsonify(db.getUser())


@app.route("/api/activeUser")
def api_activeUser():
    db.activeUser(request.args.get('id'))
    return jsonify({
      "status": True
    })


@app.route("/api/deactiveUser")
def api_deactiveUser():
    db.deactiveUser(request.args.get('id'))
    return jsonify({
      "status": True
    })


@app.route("/api/train")
def api_train():
    id = request.args.get('id')
    queue_cmd_to_hub.put({
        "type": 'TRAIN',
        "id": int(id)
    })
    return jsonify({
      "status": True
    })


@app.route("/api/getLog")
def api_getLog():
    return jsonify(db.getLog())


@app.route("/api/openDoor")
def api_openDoor():
    queue_cmd_to_hub.put({
        "type": 'REMOTE_OPEN'
    })
    return jsonify({
      "status": True
    })


def genVideoStream():
    while True:
        frame = imgc_base642bytesio(global_shared_dict['live_video_frame']).getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/api/live")
def api_live():
    #return imgc_base642url(global_shared_dict['live_video_frame'])
    #return send_file(imgc_base642bytesio(global_shared_dict['live_video_frame']), mimetype = 'image/jpg')
    return Response(genVideoStream(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/api/getLogImg")
def api_getLogImg():
    id = request.args.get('id')
    img = db.getLogImg(id)[0][0]
    #return imgc_base642url(img)
    return send_file(imgc_base642bytesio(img), mimetype = 'image/jpg')


@app.route("/api/getInfo")
def api_getInfo():
    return jsonify({
      "email": global_shared_dict['email'],
      "telephone": global_shared_dict['sms']
    })


@app.route("/api/setInfo")
def api_setInfo():
    global_shared_dict['email'] = request.args.get('email')
    global_shared_dict['sms'] = request.args.get('telephone')
    f = open('/var/EMAIL','w')
    f.write(global_shared_dict['email'])
    f.close()
    f = open('/var/SMS','w')
    f.write(global_shared_dict['sms'])
    f.close()
    return jsonify({
      "status": True
    })

# launch Flask APP
app.run(host="0.0.0.0")

# wait for all processes to finish
for p in process.values():
    p.join()

