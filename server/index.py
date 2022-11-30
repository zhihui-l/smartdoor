from flask import Flask, request, jsonify

import sys
sys.path.append('modules')

from db import addUser, rmUser, getUser, saveImageByUser, getImagesByUser
from camera import Camera

camera = Camera()


app = Flask(__name__)

@app.route("/")
def root():
    saveImageByUser(1, camera.get())
    print(len(getImagesByUser(1)))
    return 'Welcome to SmartDoor API~'


@app.route("/api/addUser")
def api_addUser():
    id = addUser(request.args.get('name'), request.args.get('id'))

    return jsonify(jsonify({
        "status": True,
        "id": id
    }))


@app.route("/api/getUser")
def api_getUser():
    return jsonify(getUser())


@app.route("/api/rmUser")
def api_rmUser():
    rmUser(request.args.get('id'))
    return jsonify({
      "status": True
    })
