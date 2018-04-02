# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import bpy


class RgbNcs:

    textblockname = 'NCS.txt'
    emptyshablon = ''

    @staticmethod
    def search(context):
        pass

    @staticmethod
    def checktextblock(context):
        textblock = None
        textblockmode = None
        if __class__.textblockname in bpy.data.texts:
            textblock = bpy.data.texts[__class__.textblockname]
            textblockmode = 'OK'
        else:
            textblock = bpy.data.texts.new(name=__class__.textblockname)
            textblock.from_string(__class__.emptyshablon)
            textblock.name = __class__.textblockname
            textblockmode = 'SAMPLE'
        if textblock:
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
                areatoshow.spaces.active.text = textblock
                textblock.current_line_index = 0
        return textblockmode


class RgbNcsVars(bpy.types.PropertyGroup):
    fullinfo = bpy.props.BoolProperty(
        name = 'FullInfoString',
        description = 'FullInfoString',
        default = True
    )
    relevantslimit = bpy.props.IntProperty(
        name = 'RelevantsLimit',
        description = 'RelevantsLimit',
        default = 5
    )

def register():
    bpy.utils.register_class(RgbNcsVars)
    bpy.types.Scene.rgb_ncs_vars = bpy.props.PointerProperty(type=RgbNcsVars)


def unregister():
    del bpy.types.Scene.rgb_ncs_vars
    bpy.utils.unregister_class(RgbNcsVars)
