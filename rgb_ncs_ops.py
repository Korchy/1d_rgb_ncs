# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import bpy
from .rgb_ncs import RgbNcs


class RbgNcsSearch(bpy.types.Operator):
    bl_idname = 'rgbncs.search'
    bl_label = 'Search nearest NCS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        textblock = RgbNcs.checktextblock(context)
        if textblock == 'OK':
            RgbNcs.search(context)
        return {'FINISHED'}


class RbgNcsClear(bpy.types.Operator):
    bl_idname = 'rgbncs.clear'
    bl_label = 'Clear search results'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        textblock = RgbNcs.checktextblock(context)
        if textblock == 'OK':
            RgbNcs.clear(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RbgNcsSearch)
    bpy.utils.register_class(RbgNcsClear)


def unregister():
    bpy.utils.unregister_class(RbgNcsClear)
    bpy.utils.unregister_class(RbgNcsSearch)
