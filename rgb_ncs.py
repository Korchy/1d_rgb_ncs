# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import bpy
import json
import os
import re
from mathutils import Vector


class RgbNcs:

    textblockname = 'NCS.txt'
    emptyshablon = 'RGB ## вводные данные\n172-173-175\n84-84-82'
    colorsdatabase = None
    colorsdatabesefile = os.path.join(os.path.dirname(__file__), 'colors.json')
    textblock = None
    rgbmask = re.compile('^\d{1,3}-\d{1,3}-\d{1,3}$')

    @staticmethod
    def search(context):
        if __class__.textblock:
            for line in __class__.textblock.lines[1:]:
                line.body += ' ' + __class__.getcolorinfo(line.body, context.window_manager.rgb_ncs_vars.relevantslimit, context.window_manager.rgb_ncs_vars.fullinfo)

    @staticmethod
    def getcolorinfo(color, limit, fullinfo):
        rez = ''
        if color and __class__.rgbmask.match(color.strip()) is not None:
            db = __class__.colorsdb()
            rgbarr = color.split('-')
            rgb = Vector((int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2])))
            ncss = sorted(db, key=lambda x: (rgb - Vector((x[0][0], x[0][1], x[0][2]))).length)[:limit]
            rez += ' ' * (15 - len(color)) + '| '
            for ncs in ncss:
                rez += ' (={:<7.2%} {:03d}-{:03d}-{:03d} [{:<15}] '.format(__class__.relevance(rgb, ncs[0]), int(ncs[0][0]), int(ncs[0][1]), int(ncs[0][2]), ncs[1][0])
                if fullinfo:
                    rez += ' {} {}'.format(ncs[1][2], '-'.join([a.zfill(3) for a in ncs[1][1].split('-')]))
                rez += ') |'
        return rez

    @staticmethod
    def relevance(vector1, vector2):
        v1len2 = vector1[0] ** 2 + vector1[1] ** 2 + vector1[2] ** 2
        v2len2 = vector2[0] ** 2 + vector2[1] ** 2 + vector2[2] ** 2
        relevance = v1len2 / v2len2
        if relevance > 1:
            relevance = v2len2 / v1len2
        return relevance

    @staticmethod
    def colorsdb():
        if not __class__.colorsdatabase:
            with open(__class__.colorsdatabesefile) as data:
                __class__.colorsdatabase = json.load(data)
        return __class__.colorsdatabase

    @staticmethod
    def checktextblock(context):
        textblockmode = None
        if __class__.textblockname in bpy.data.texts:
            __class__.textblock = bpy.data.texts[__class__.textblockname]
            textblockmode = 'OK'
        else:
            __class__.textblock = bpy.data.texts.new(name=__class__.textblockname)
            __class__.textblock.from_string(__class__.emptyshablon)
            __class__.textblock.name = __class__.textblockname
            textblockmode = 'SAMPLE'
        if __class__.textblock:
            areatoshow = None
            for area in context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    areatoshow = area
            if not areatoshow:
                for area in context.screen.areas:
                    if area.type not in ['PROPERTIES', 'INFO', 'OUTLINER']:
                        areatoshow = area
                        break
            if areatoshow:
                areatoshow.type = 'TEXT_EDITOR'
                areatoshow.spaces.active.text = __class__.textblock
                __class__.textblock.current_line_index = 0
        return textblockmode


class RgbNcsVars(bpy.types.PropertyGroup):
    fullinfo = bpy.props.BoolProperty(
        name='FullInfo',
        description='FullInfo',
        default=True
    )
    relevantslimit = bpy.props.IntProperty(
        name='Colors',
        description='Relevants Colors Limit',
        default=5
    )


def register():
    bpy.utils.register_class(RgbNcsVars)
    bpy.types.WindowManager.rgb_ncs_vars = bpy.props.PointerProperty(type=RgbNcsVars)


def unregister():
    del bpy.types.WindowManager.rgb_ncs_vars
    bpy.utils.unregister_class(RgbNcsVars)
