# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

"""
This file is used to store paths of pictures.
"""
import os


class Picture:
    prefix = __file__.replace('pic.py', 'pic/')
    # root
    minimize = os.path.join(prefix, 'minimize.bmp')

# pic = Picture
# print(pic.minimize)
