import mariadb
import os
import hashlib
import time
import random
from PIL import Image
import json

DB_DIR = '/tmp/smartdoorDB'


if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)


db = mariadb.connect(
  host="localhost",
  user="smartdoor",
  password="",
  database="smartdoor"
)

cursor = db.cursor()

def addUser(name):
    global cursor, db
    cursor.execute("INSERT INTO user (name) VALUES ('%s')" % name)
    id = cursor.lastrowid
    db.commit()
    return id

def activeUser(id):
    global cursor, db
    cursor.execute("UPDATE user SET active=TRUE WHERE uid=%s" % str(id))
    db.commit()
    return id

def deactiveUser(id):
    global cursor, db
    cursor.execute("UPDATE user SET active=FALSE WHERE uid=%s" % str(id))
    db.commit()
    return id

def getUser(uid = None):
    global cursor, db
    if uid:
        cursor.execute("SELECT name FROM user WHERE uid = %d AND active=TRUE" % int(uid))
    else:
        cursor.execute("SELECT * FROM user")
    return cursor.fetchall()


def addUserIteration(uid):
    global cursor, db
    cursor.execute("UPDATE user SET iteration=iteration+1 where uid=%s" % str(uid))
    db.commit()
    return id


def log(type, uid = "NULL", img = "NULL", data = "NULL"):
    global cursor, db
    if img != 'NULL':
        img = "'"+img+"'"
    if data != 'NULL':
        data = "'"+data+"'"
    cursor.execute("INSERT INTO log (type, uid, img, data) VALUES ('%s', %s, %s, %s)" % (type, str(uid), img, data))
    db.commit()

def getLog():
    global cursor, db
    cursor.execute("SELECT l.lid, l.type, l.uid, u.name, l.createtime, l.img IS NOT NULL, l.data FROM log l LEFT JOIN user u ON l.uid = u.uid ORDER BY l.lid DESC")
    return cursor.fetchall()

def getLogImg(lid):
    global cursor, db
    cursor.execute("SELECT img FROM log WHERE lid = %s " % str(lid))
    return cursor.fetchall()
