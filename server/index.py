from flask import Flask, request, jsonify

import sys
sys.path.append('modules')

from db import addUser, rmUser, getUser

app = Flask(__name__)



@app.route("/api/addUser")
def api_addUser():
    addUser(request.args.get('id'))
    return jsonify(jsonify({
        "status": True
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