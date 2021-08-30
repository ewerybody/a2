import time
import a2core
from a2element.common import DrawCtrl, EditCtrl, DrawCtrlMixin


# amend with new elements to show in edit mode on Add Element-buttons:
DISPLAY_ELEMENTS = [
    'button',
    'check',
    'combo',
    'coords',
    'exit',
    'group',
    'hotkey',
    'init',
    'label',
    'menu_item',
    'number',
    'path',
    'pathlist',
    'string',
]

_UI_DATA = None
log = a2core.get_logger(__name__)


def get_list(force=False):
    """
    Loads the python modules of the given DISPLAY_ELEMENTS to fetch display names and icons
    so they can be listed in a2 module edit mode.
    """
    if not _UI_DATA and not force:
        _load_ui_data()
    return _UI_DATA


def _load_ui_data():
    import a2ctrl

    global _UI_DATA
    _UI_DATA = []
    for element in DISPLAY_ELEMENTS:
        element_mod = a2ctrl.get_a2element_module(element)
        if element_mod:
            display_name = element_mod.Edit.element_name()
            icon = element_mod.Edit.element_icon()
            if display_name == EditCtrl.element_name():
                log.error('Element "%s" has no element_name properly set!' % element)
                display_name = element.title()
            _UI_DATA.append((element, display_name, icon))
