from threading import Timer

def timeout(t, cb):
    t = Timer(t, cb)
    t.daemon = True
    t.start()