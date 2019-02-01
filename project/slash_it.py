# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

import time

from core.adam import Adam
from resource.pic import Picture

adam = Adam()
pic = Picture()


class SlashIt:

    def __init__(self):
        adam.hot_key('win', 'd')
        time.sleep(1)

    def launch_game(self):
        adam.click_key('win')
        time.sleep(0.5)
        adam.send_text('steam')
        adam.click_key('enter')
        adam.wait_for_object(pic.ad_close)
        adam.click_object()
        for i in range(10):
            adam.touch_object(pic.library)
            time.sleep(1)
            if adam.find_object(pic.search_library):
                adam.click_object()
                break
            else:
                continue
        else:
            raise Exception("Can't connect to network.")
        time.sleep(0.5)
        adam.send_text('slash it 2')
        time.sleep(0.5)
        adam.click_key('enter')
        time.sleep(1)
        adam.wait_for_object(pic.slash_it_steam)
        adam.touch_object(pic.play)


game = SlashIt()
game.launch_game()
