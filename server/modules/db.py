import mariadb
import os
import hashlib
import time
import random
from PIL import Image

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

def addUser(name = None, id = None):
    global cursor, db
    if id:
        cursor.execute("UPDATE user SET status=TRUE WHERE id=%d" % id)
    elif name: 
        cursor.execute("INSERT INTO user (name) VALUES ('%s')" % name)
        id = cursor.lastrowid
    db.commit()
    return id

def getUser(ActiveOnly = True):
    global cursor, db
    if ActiveOnly: cursor.execute("SELECT * FROM user WHERE status=TRUE")
    else: cursor.execute("SELECT * FROM user")
    #db.commit()
    return cursor.fetchall()

def rmUser(id):
    global cursor, db
    cursor.execute("UPDATE user SET status=FALSE WHERE id=%d" % id)
    db.commit()

def saveImageByUser(id, image):
    dir = DB_DIR + '/' + str(id)
    filename = hashlib.md5((str(time.time())+str(random.random())).encode("utf-8")).hexdigest()
    if not os.path.exists(dir):
        os.makedirs(dir)
    image.save(dir + '/' + filename + '.jpg')    


def getImagesByUser(id):
    imageList = []
    dir = DB_DIR + '/' + str(id)
    for root, dirs, files in os.walk(dir):
        for filename in files:
            imageList.append(Image.open(dir + '/' + filename))
    return imageList

