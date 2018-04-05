# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import bpy
from .colors import Colors


class RgbNcs:

    __textblockname = 'NCS.txt'
    __emptyshablon = 'RGB ## вводные данные\t\t|\t%\t\tRGB\t\tNCS\t\tHEX\t\tCMYC\t|\n172-173-175\n84-84-82\n5-5-5'
    __textblock = None

    @staticmethod
    def search(context):
        __class__.clear(context)
        if __class__.__textblock:
            for line in __class__.__textblock.lines[1:]:
                rez = Colors.search_nearest_ncs_by_rgb(line.body.strip(), context.window_manager.rgb_ncs_vars.relevantslimit)
                line.body += ' ' * (15 - len(line.body.strip())) + __class__.formatinfo(rez, context.window_manager.rgb_ncs_vars.fullinfo)

    @staticmethod
    def formatinfo(data, fullinfo):
        rez = ''
        if data:
            for line in data:
                rez += '| (={:<7.2%} {:03d}-{:03d}-{:03d} [{:<15}] '.format(line[2], int(line[0][0]), int(line[0][1]), int(line[0][2]), line[1][0])
                if fullinfo:
                    rez += ' {} {}'.format(line[1][2], '-'.join([a.zfill(3) for a in line[1][1].split('-')]))
                rez += ') '
            rez += '|'
        return rez

    @staticmethod
    def clear(context):
        if __class__.__textblock:
            for line in __class__.__textblock.lines[1:]:
                line.body = line.body[:11].strip()

    @staticmethod
    def checktextblock(context):
        textblockmode = None
        if __class__.__textblockname in bpy.data.texts:
            __class__.__textblock = bpy.data.texts[__class__.__textblockname]
            textblockmode = 'OK'
        else:
            __class__.__textblock = bpy.data.texts.new(name=__class__.__textblockname)
            __class__.__textblock.from_string(__class__.__emptyshablon)
            __class__.__textblock.name = __class__.__textblockname
            textblockmode = 'SAMPLE'
        if __class__.__textblock:
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
                areatoshow.spaces.active.text = __class__.__textblock
                __class__.__textblock.current_line_index = 0
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
