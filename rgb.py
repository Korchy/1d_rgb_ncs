# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import math
import re
from mathutils import Vector


class RGB:

    __r = None
    __g = None
    __b = None

    __relevance0 = math.sqrt(3)*255   # rgb colors relevance = 0 when compare 2 rgb colors (diagonal of the rgb-cube 255x255x255)

    def __init__(self, r, g, b):
        if isinstance(r, int) and isinstance(g, int) and isinstance(b, int):
            self.__r = r
            self.__g = g
            self.__b = b

    def __repr__(self):
        return "RGB({},{},{})".format(self.__r, self.__g, self.__b)

    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g

    @property
    def b(self):
        return self.__b

    @classmethod
    def fromstring(cls, rgb):
        if re.compile('^\d{1,3}-\d{1,3}-\d{1,3}$').match(rgb) is not None:
            # 123-123-123
            rgbarr = rgb.split('-')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        elif re.compile('^\d{1,3}.\d{1,3}.\d{1,3}$').match(rgb) is not None:
            # 123.123.123
            rgbarr = rgb.split('.')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        else:
            return None

    @classmethod
    def fromlist(cls, lst):
        return cls(lst[0], lst[1], lst[2])

    @staticmethod
    def relevance(rgb1, rgb2):
        if isinstance(rgb1, RGB) and isinstance(rgb2, RGB):
            relevancelengtn = (__class__.rgb_to_vector(rgb1) - __class__.rgb_to_vector(rgb2)).length
            return 1 - relevancelengtn / __class__.__relevance0
        else:
            return 0

    @staticmethod
    def rgb_to_vector(rgb):
        if isinstance(rgb, RGB):
            return Vector((rgb.r, rgb.g, rgb.b))

    def to_vector(self):
        return __class__.rgb_to_vector(self)
