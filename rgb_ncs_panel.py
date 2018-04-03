# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS color from RGB value


import bpy


class RgbNcsPanel(bpy.types.Panel):
    bl_idname = 'rbgncs.panel'
    bl_label = 'RGB_NCS'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        self.layout.operator('rgbncs.search', icon='COLORSET_03_VEC', text='RGB to NCS')
        self.layout.prop(context.window_manager.rgb_ncs_vars, 'fullinfo')
        self.layout.prop(context.window_manager.rgb_ncs_vars, 'relevantslimit')


def register():
    bpy.utils.register_class(RgbNcsPanel)


def unregister():
    bpy.utils.unregister_class(RgbNcsPanel)
