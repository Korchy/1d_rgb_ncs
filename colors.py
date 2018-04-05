# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import json
import os
from mathutils import Vector
from .rgb import RGB
import copy


class Colors:

    __ncsdatabase = None
    __ncsdatabesefile = os.path.join(os.path.dirname(__file__), 'ncs.json')

    @staticmethod
    def search_nearest_ncs_by_rgb(rgb_string, limit):
        rgb = RGB.fromstring(rgb_string)
        db = __class__.ncsdb()
        rgb_vector = rgb.to_vector()
        ncs_list = copy.deepcopy(sorted(db, key=lambda x: (rgb_vector - Vector((x[0][0], x[0][1], x[0][2]))).length)[:limit])
        for ncs in ncs_list:
            ncs.append(RGB.relevance(rgb, RGB.fromlist(ncs[0])))
        return ncs_list

    @staticmethod
    def ncsdb():
        if not __class__.__ncsdatabase:
            with open(__class__.__ncsdatabesefile) as data:
                __class__.__ncsdatabase = json.load(data)
        return __class__.__ncsdatabase
