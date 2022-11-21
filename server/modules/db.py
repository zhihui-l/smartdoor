import mariadb

db = mariadb.connect(
  host="localhost",
  user="smartdoor",
  password="",
  database="smartdoor"
)

cursor = db.cursor()

def addUser(username):
    global cursor, db
    cursor.execute("INSERT INTO user (name) VALUES ('%s')" % username)
    db.commit()

def getUser():
    global cursor, db
    cursor.execute("SELECT * FROM user WHERE status=TRUE")
    #db.commit()
    return cursor.fetchall()

def rmUser(id):
    global cursor, db
    cursor.execute("UPDATE user SET status=FALSE WHERE id=%d" % id)
    db.commit()

