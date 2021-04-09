from threading import Thread
from mysite.pi import Pi

shared_list = [0, 0]

pi = Pi(shared_list)
threading = Thread(target=pi.run, daemon=True)
threading.start()

print("__init__ has done")