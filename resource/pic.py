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

    # steam/
    ad_close = os.path.join(prefix, 'steam/ad_close.bmp')
    library = os.path.join(prefix, 'steam/library.bmp')
    play = os.path.join(prefix, 'steam/play.bmp')
    search_library = os.path.join(prefix, 'steam/search_library.bmp')
    slash_it_steam = os.path.join(prefix, 'steam/slash_it_steam.bmp')
