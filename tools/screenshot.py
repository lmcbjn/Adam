# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

"""
Take a screenshot after clicking hot key and then save it as .bmp file.
"""

import time
import threading
import datetime
import pyautogui as auto

from core.adam import Adam
from pynput.keyboard import Key, Listener

lock = True


def on_press(key):
    if key == Key.print_screen:
        time = datetime.datetime.now().strftime("%H%M%S")
        image = auto.screenshot()
        image.save("{0}.bmp".format(time))
    if key == Key.home:
        adam = Adam()
        adam.show_screenshot(False)
    if key == Key.esc:
        global lock
        lock = False
        return False


def listen():
    with Listener(on_press=on_press) as listener:
        listener.join()


def print_hello():
    while lock:
        print('hello')
        time.sleep(1)


threads = []
funcs = [listen, print_hello]
count = range(len(funcs))
for func in funcs:
    t = threading.Thread(target=func)
    threads.append(t)
for t in threads:
    t.setDaemon(True)
    t.start()
for i in count:
    threads[i].join()
