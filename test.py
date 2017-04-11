import threading
from time import sleep
import main

a = 5


def bunk():
    sleep(1)


def func(b):
    t = threading.Thread(name="2nd step thread no. " + str(b), target=bunk)
    t.start()
    for i in range(10000):
        sleep(0.1)


for i in range(10):
    t = threading.Thread(name="Thread no. " + str(i), target=func, args=(i,))
    t.start()