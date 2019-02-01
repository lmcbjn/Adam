# ！/usr/bin/env python3
# -*-coding: UTF-8 -*-
# Author Frank

import time
import cv2
import numpy
import pytesseract
import pyautogui as auto

from datetime import datetime
from resource import pic as picture

pic = picture.Picture()


class Adam:

    def __init__(self):
        self._point = None
        # auto.FAILSAFE = False
        # auto.PAUSE = 0.1

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

    def wait_for_object(self, image, duration=60):
        """
        Find object on the screen within given times.
        :param image:
        :param duration:->int seconds
        :return:
        """
        start = datetime.utcnow()
        while True:
            delta = datetime.utcnow() - start
            if delta.seconds < duration:
                if self.find_object(image):
                    return True
                else:
                    continue
            else:
                raise Exception("Can't find image")

    def touch_object(self, image):
        if self.find_object(image):
            self.click_object()
        else:
            raise Exception("Can't find image.")

    def click_object(self, left=True, times=1):
        self.click_point(self._point, left, times)

    def show_screenshot(self, rgb=True):
        mode = cv2.COLOR_RGB2BGR
        if not rgb:
            mode = cv2.COLOR_BGR2GRAY
        img = cv2.cvtColor(numpy.asarray(self.screenshot()), mode)
        img = cv2.resize(img, (1536, 864))
        cv2.imshow('image', img)
        cv2.waitKey(0)

    @classmethod
    def click_point(cls, points, left=True, times=1):
        if isinstance(points, tuple):
            if left:
                if times == 1:
                    auto.click(*points)
                elif times == 2:
                    auto.doubleClick(*points)
                elif times == 3:
                    auto.tripleClick(*points)
                else:
                    raise Exception("times must within 1~3.")
                time.sleep(0.2)
            else:
                auto.rightClick(*points)
        elif isinstance(points, list):
            for point in points:
                auto.click(point)
                time.sleep(0.2)
        auto.dragTo(1920, 1080)

    @classmethod
    def find_text(cls, message):
        img = cls.screenshot()
        """
        waiting for adding image processing.
        """
        text = cls.do_ocr_on_image(img)
        for word in text:
            if message in word:
                return word
        else:
            return False

    @classmethod
    def key_down(cls, key):
        auto.keyDown(key)

    @classmethod
    def key_up(cls, key):
        auto.keyUp(key)

    @classmethod
    def click_key(cls, key, times=1, interval=0):
        auto.press(key, presses=times, interval=interval)

    @classmethod
    def hot_key(cls, *keys):
        auto.hotkey(*keys)

    @classmethod
    def send_text(cls, message, interval=0.1):
        auto.typewrite(message, interval=interval)

    @classmethod
    def do_ocr_on_image(cls, img, data=False):
        image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        if data:
            data = pytesseract.image_to_data(image)
            return data
        string = pytesseract.image_to_string(image)
        return string

    @classmethod
    def screenshot(cls):
        """
        Take a screenshot and save it.
        :return:
        """
        return auto.screenshot()
