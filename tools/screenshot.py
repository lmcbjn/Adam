# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

"""
Take a screenshot after clicking hot key and then save it as .bmp file.
"""

import datetime
import pyautogui as auto

from pynput.keyboard import Key, Listener


def on_press(key):
    if key == Key.print_screen:
        time = datetime.datetime.now().strftime("%H%M%S")
        image = auto.screenshot()
        image.save("{0}.bmp".format(time))


with Listener(on_press=on_press) as listener:
    listener.join()
