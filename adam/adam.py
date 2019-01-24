# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

import time
import cv2
import numpy
import pyautogui as auto

from resource import pic as picture

pic = picture.Picture()


class Adam:

    def __init__(self):
        self._point = None
        # auto.FAILSAFE = False
        auto.PAUSE = 0.1

    def count_object(self, image):
        """
        Count the object on screen.
        :param image: image of object.
        :return:
        """
        # Take a ScreenShot, then convert picture to OpenCV format.
        image_small = cv2.imread(image)
        image_big = cv2.cvtColor(numpy.asarray(self.screenshot()), cv2.COLOR_RGB2BGR)
        width, height = image_small.shape[1], image_small.shape[0]
        size = height if height < width else width
        # match template
        cv_result = cv2.matchTemplate(image_big, image_small, cv2.TM_CCOEFF_NORMED)
        # threshold = max matching ratio
        threshold = cv2.minMaxLoc(cv_result)[1]
        if threshold < 0.9:
            return 0
        else:
            # lower matching ratio
            threshold *= 0.91
            # select points which bigger than matching ratio, then add them to point_list.
            location = numpy.where(cv_result >= threshold)
            point_list = []
            for point in zip(*location[::-1]):
                point_list.append(point)
            # sort all the points in point_list, key is the sum of point.x and point.y.
            point_list.sort(key=lambda point1: point1[0] + point1[1])
            # remove points which near matched point.
            guard = point_list[0]
            for point in point_list[:]:
                number = abs(point[0] - guard[0]) + abs(point[1] - guard[1])
                if 0 < number < size:
                    point_list.remove(point)
                else:
                    guard = point
            self._point = [(point1[0] + width / 2, point1[1] + height / 2) for point1 in point_list]
            return len(point_list)

    def click_point(self, left=True, times=1):
        print(self._point)
        if isinstance(self._point, tuple):
            if left:
                if times == 1:
                    auto.click(*self._point)
                elif times == 2:
                    auto.doubleClick(*self._point)
                elif times == 3:
                    auto.tripleClick(*self._point)
                else:
                    raise Exception("times muse within 1~3.")
            else:
                auto.rightClick(*self._point)
        elif isinstance(self._point, list):
            for point in self._point:
                auto.click(point)
                time.sleep(0.2)
        auto.dragTo(1920, 1080)

    def find_object(self, image):
        """
        Find object on screen.
        :param image: image of object.
        :return:
        """
        image_small = cv2.imread(image)
        image_big = cv2.cvtColor(numpy.asarray(self.screenshot()), cv2.COLOR_RGB2BGR)
        matrix = cv2.matchTemplate(image_small, image_big, cv2.TM_CCOEFF_NORMED)
        match_rate = cv2.minMaxLoc(matrix)
        if match_rate[1] < 0.9:
            return False
        width, height, = image_small.shape[1], image_small.shape[0]
        self._point = (width / 2 + match_rate[3][0], height / 2 + match_rate[3][1])
        return True

    def wait_for_object(self, image, times):
        """
        Find object on the screen within given times.
        :param image:
        :param times:
        :return:
        """
        pass

    @classmethod
    def screenshot(cls):
        """
        Take a screenshot and save it.
        :return:
        """
        return auto.screenshot()


adam = Adam()
# result = adam.find_object(pic.minimize)
if adam.count_object(pic.minimize):
    adam.click_point()
