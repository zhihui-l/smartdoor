import multiprocessing as mp
from flask import Flask, request, jsonify, send_file
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/modules')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/utilities')


from display import display
from hub import hub
from motor import motor
from face_recg import face_recg

from imgConvert import *

import db

queue_photo = mp.Queue()
queue_cmd_from_display = mp.Queue()
queue_cmd_to_display = mp.Queue()
queue_cmd_to_motor = mp.Queue()
queue_cmd_from_face_recg = mp.Queue()
queue_cmd_to_face_recg = mp.Queue()
queue_cmd_to_hub = mp.Queue()

dict_live_photo = (mp.Manager()).dict()
dict_live_photo['png'] = ''
dict_live_photo['good'] = ''
f = open('/var/EMAIL')
data = f.read()
dict_live_photo['email'] = data
f.close()
f = open('/var/SMS')
data = f.read()
dict_live_photo['sms'] = data
f.close()



process = {
    "display": mp.Process(target=display, args=(queue_cmd_from_display, queue_cmd_to_display, dict_live_photo)),
    "motor": mp.Process(target=motor, args=(queue_cmd_to_motor,)),
    "face_recg": mp.Process(target=face_recg, args=(dict_live_photo, queue_cmd_from_face_recg, queue_cmd_to_face_recg)),
    "hub": mp.Process(target=hub, args=(
        queue_cmd_to_hub,
        queue_cmd_from_display, 
        queue_cmd_to_display, 
        queue_cmd_to_motor,
        queue_cmd_from_face_recg,
        queue_cmd_to_face_recg,
        dict_live_photo))
}

print('dis')
for p in process.values():
    p.start()
print('play')

app = Flask(__name__)
print('displayyyy')


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


@app.route("/api/live")
def api_live():
    #return imgc_base642url(dict_live_photo['png'])
    return send_file(imgc_base642bytesio(dict_live_photo['png']), mimetype = 'image/jpg')


@app.route("/api/getLogImg")
def api_getLogImg():
    id = request.args.get('id')
    img = db.getLogImg(id)[0][0]
    #return imgc_base642url(img)
    return send_file(imgc_base642bytesio(img), mimetype = 'image/jpg')


@app.route("/api/getInfo")
def api_getInfo():
    return jsonify({
      "email": dict_live_photo['email'],
      "telephone": dict_live_photo['sms']
    })


@app.route("/api/setInfo")
def api_setInfo():
    dict_live_photo['email'] = request.args.get('email')
    dict_live_photo['sms'] = request.args.get('telephone')
    f = open('/var/EMAIL','w')
    f.write(dict_live_photo['email'])
    f.close()
    f = open('/var/SMS','w')
    f.write(dict_live_photo['sms'])
    f.close()
    return jsonify({
      "status": True
    })

app.run(host="0.0.0.0")


for p in process.values():
    p.join()

