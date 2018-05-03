# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   2018.04.11 - 1.0.0. - release - Search for some nearest NCS color from RGB value
#   2018.05.03 - 1.0.1. - change - combine all modules to one script (for convenient embed to 1d)
#   2018.05.03 - 1.0.2. - improve - add graphical version


bl_info = {
    'name': 'RGB_NCS',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 2),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_rgb_ncs',
    'tracker_url': 'https://github.com/Korchy/1d_rgb_ncs',
    'description': 'RGB_NCS: Search for some nearest NCS colors from RGB value'
}

import bpy
import json
import os
import re
from mathutils import Vector
import copy


class RgbNcs:

    __ncsdatabase = None
    __ncsdatabesefile = os.path.join(os.path.dirname(__file__), 'ncs.json')

    __textblockname = 'NCS.txt'
    __emptyshablon = 'RGB ## вводные данные\t\t|\t%\t\tRGB\t\tNCS\t\tHEX\t\tCMYC\t|\n172-173-175\n84-84-82\n5-5-5'
    __textblock = None
    __matches = []  # search results -> first element - rgb color

    @staticmethod
    def ncsdb():
        if not __class__.__ncsdatabase:
            with open(__class__.__ncsdatabesefile) as data:
                __class__.__ncsdatabase = json.load(data)
        return __class__.__ncsdatabase

    @staticmethod
    def matches():
        return __class__.__matches

    @staticmethod
    def matches_str():
        matches_str = ''
        if __class__.__matches:
            matches_str += '%\tRGB\tNCS\tHEX\tCMYK\n'
            for line in __class__.__matches:
                matches_str += '{:<7.2%}\t{:03d}-{:03d}-{:03d}\t{:<15}\t'.format(line[2], int(line[0][0]), int(line[0][1]), int(line[0][2]), line[1][0])
                matches_str += '{}\t{}'.format(line[1][2], '-'.join([a.zfill(3) for a in line[1][1].split('-')]))
                matches_str += '\n'
        return matches_str

    @staticmethod
    def search_nearest_ncs_by_rgb(rgb, limit):
        db = __class__.ncsdb()
        rgb_vector = rgb.to_vector()
        ncs_list = copy.deepcopy(sorted(db, key=lambda x: (rgb_vector - Vector((x[0][0], x[0][1], x[0][2]))).length)[:limit])
        for ncs in ncs_list:
            ncs.append(RGB.relevance(rgb, RGB.fromlist(ncs[0])))
        return ncs_list

    @staticmethod
    def search_text(context):
        __class__.clear(context)
        if __class__.__textblock:
            for line in __class__.__textblock.lines[1:]:
                rez = __class__.search_nearest_ncs_by_rgb(RGB.fromstring(line.body.strip()), context.window_manager.rgb_ncs_vars.relevantslimit)
                __class__.__matches.append(rez)
                line.body += ' ' * (15 - len(line.body.strip())) + __class__.formatinfo(rez, context.window_manager.rgb_ncs_vars.fullinfo)

    @staticmethod
    def search_graphic(context):
        __class__.clear(context)
        __class__.__matches = __class__.search_nearest_ncs_by_rgb(RGB.fromlist(context.window_manager.rgb_ncs_vars.source_color), context.window_manager.rgb_ncs_vars.relevantslimit)

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
        __class__.__matches = []
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


class RGB:

    __r = None
    __g = None
    __b = None

    # __relevance0 = math.sqrt(3)*255   # rgb colors relevance = 0 when compare 2 rgb colors (diagonal of the rgb-cube 255x255x255)
    __relevance0 = 255   # rgb colors relevance = 0 when compare 2 rgb colors (not real but more convenient for designers)

    def __init__(self, r, g, b):
        if isinstance(r, int) and r >= 0 and r <= 255 and isinstance(g, int) and g >= 0 and g <= 255 and isinstance(b, int) and b >= 0 and b <= 255:
            self.__r = r
            self.__g = g
            self.__b = b
        if isinstance(r, float) and r >= 0.0 and r <= 1.0 and isinstance(g, float) and g >= 0.0 and g <= 1.0 and isinstance(b, float) and b >= 0.0 and b <= 1.0:
            self.__r = 255 * r
            self.__g = 255 * g
            self.__b = 255 * b

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
        # [0-255, 0-255, 0-255] or [0.0-1.0, 0.0-1.0, 0.0-1.0]
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

    @staticmethod
    def rgb_to_unit(rgb):
        if isinstance(rgb, RGB):
            return [rgb.r / 255, rgb.g / 255, rgb.b / 255]

    def to_unit(self):
        return __class__.rgb_to_unit(self)


# --- VARS ----------------------------------------------------

class RgbNcsVars(bpy.types.PropertyGroup):
    fullinfo = bpy.props.BoolProperty(
        name='FullInfo',
        description='FullInfo',
        default=True
    )
    relevantslimit = bpy.props.IntProperty(
        name='Colors',
        description='Relevants Colors Limit',
        min=0,
        default=5
    )
    source_color = bpy.props.FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.8, 0.8, 1.0)
    )


class DestColorItem(bpy.types.PropertyGroup):
    dest_color = bpy.props.FloatVectorProperty(
         name='Color',
         subtype='COLOR',
         size=4,
         min=0.0,
         max=1.0,
         default=(0.8, 0.8, 0.8, 1.0)
     )


# --- OPS ----------------------------------------------------

class RbgNcsSearch(bpy.types.Operator):
    bl_idname = 'rgbncs.search'
    bl_label = 'Search nearest NCS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        textblock = RgbNcs.checktextblock(context)
        if textblock == 'OK':
            RgbNcs.search_text(context)
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


class NCSMatchAddNode(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch_addnode'
    bl_label = 'Add RGB Node'
    bl_options = {'REGISTER', 'INTERNAL'}

    add_node_id = bpy.props.IntProperty(
        name='NodeId',
        min=0,
        subtype='UNSIGNED',
        default=0
    )

    def execute(self, context):
        # add RGB node to active object - active material
        if context.selected_objects:
            added = []
            for object in context.selected_objects:
                if object.active_material and object.active_material not in added:
                    if not object.active_material.use_nodes:
                        object.active_material.use_nodes = True
                    rgb_node = object.active_material.node_tree.nodes.new(type='ShaderNodeRGB')
                    rgb_node.location = (0, 0)
                    matches = RgbNcs.matches()
                    print(self.add_node_id)
                    rgb_node.outputs[0].default_value = (matches[self.add_node_id][0][0] / 255, matches[self.add_node_id][0][1] / 255, matches[self.add_node_id][0][2] / 255, 1.0)
                    added.append(object.active_material)
        return {'FINISHED'}


class NCSMatchCopyMatchesToClipboard(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch_toclipboard'
    bl_label = 'To Clipboard'
    bl_description = 'Copy search results to clipboard'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        # copy NCS matches string to clipboard
        matches_str = RgbNcs.matches_str()
        if matches_str:
            context.window_manager.clipboard = matches_str
        return {'FINISHED'}


class NCSMatch(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch'
    bl_label = 'Search for closest NCS:'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        RgbNcs.clear(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        RgbNcs.search_graphic(context)
        matches = RgbNcs.matches()
        for i, match in enumerate(matches):
            context.window_manager.colormatching_colors.add()
            context.window_manager.colormatching_colors[i].dest_color[0] = match[0][0] / 255
            context.window_manager.colormatching_colors[i].dest_color[1] = match[0][1] / 255
            context.window_manager.colormatching_colors[i].dest_color[2] = match[0][2] / 255
        # show window
        return context.window_manager.invoke_popup(self, width=700)

    def draw(self, context):
        matches = RgbNcs.matches()
        row = self.layout.split(0.92)
        row.label(self.bl_label)
        row.operator('colormatch.ncsmatch_toclipboard', text='', icon='COPYDOWN')
        row = self.layout.row().separator()
        row = self.layout.row()
        for i, match in enumerate(matches):
            col = row.column()
            col.label(str(round(match[2] * 100, 2)) + ' %')
            col.prop(context.window_manager.colormatching_colors[i], 'dest_color', text='')
            col.label(match[1][0])
            col.label('CMYK ' + match[1][1])
            col.operator('colormatch.ncsmatch_addnode').add_node_id = i

    def check(self, context):
        return True

    def cancel(self, context):
        self.execute(context)


# --- UI ----------------------------------------------------

class RgbNcsPanel(bpy.types.Panel):
    bl_idname = 'rbgncs.panel'
    bl_label = 'RGB_NCS'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        self.layout.prop(context.window_manager.rgb_ncs_vars, 'relevantslimit')
        self.layout.label('TEXT:')
        box = self.layout.box()
        box.operator('rgbncs.search', icon='COLORSET_03_VEC', text='RGB to NCS')
        box.prop(context.window_manager.rgb_ncs_vars, 'fullinfo')
        box.operator('rgbncs.clear', icon='CANCEL', text='Clear')
        self.layout.label('GRAPHIC:')
        box = self.layout.box()
        box.prop(context.window_manager.rgb_ncs_vars, 'source_color')
        box.operator('colormatch.ncsmatch', text='Search NCS (NCl)')


# --- REGISTER ----------------------------------------------------

def register():
    bpy.utils.register_class(RgbNcsVars)
    bpy.utils.register_class(DestColorItem)
    bpy.utils.register_class(RbgNcsSearch)
    bpy.utils.register_class(RbgNcsClear)
    bpy.utils.register_class(RgbNcsPanel)
    bpy.utils.register_class(NCSMatch)
    bpy.utils.register_class(NCSMatchAddNode)
    bpy.utils.register_class(NCSMatchCopyMatchesToClipboard)
    bpy.types.WindowManager.rgb_ncs_vars = bpy.props.PointerProperty(type=RgbNcsVars)
    bpy.types.WindowManager.colormatching_colors = bpy.props.CollectionProperty(type=DestColorItem)


def unregister():
    del bpy.types.WindowManager.colormatching_colors
    del bpy.types.WindowManager.rgb_ncs_vars
    bpy.utils.unregister_class(NCSMatchCopyMatchesToClipboard)
    bpy.utils.unregister_class(NCSMatchAddNode)
    bpy.utils.unregister_class(NCSMatch)
    bpy.utils.unregister_class(RgbNcsPanel)
    bpy.utils.unregister_class(RbgNcsClear)
    bpy.utils.unregister_class(RbgNcsSearch)
    bpy.utils.unregister_class(DestColorItem)
    bpy.utils.unregister_class(RgbNcsVars)


if __name__ == '__main__':
    register()
