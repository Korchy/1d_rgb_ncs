# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_rgb_ncs
#
# Version history:
#   1.0. - Search for some nearest NCS colors from RGB value

bl_info = {
    'name': 'RGB_NCS',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_rgb_ncs',
    'tracker_url': 'https://github.com/Korchy/1d_rgb_ncs',
    'description': 'RGB_NCS: Search for some nearest NCS colors from RGB value'
}

from . import rgb_ncs_panel
from . import rgb_ncs_ops
from . import rgb_ncs


def register():
    rgb_ncs.register()
    rgb_ncs_ops.register()
    rgb_ncs_panel.register()


def unregister():
    rgb_ncs_panel.unregister()
    rgb_ncs_ops.unregister()
    rgb_ncs.unregister()


if __name__ == '__main__':
    register()
