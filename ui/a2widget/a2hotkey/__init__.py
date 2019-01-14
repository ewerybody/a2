from .hotkey_widget import A2Hotkey, DIALOG_CLASSES, DIALOG_DEFAULT
from .hotkey_common import Vars


def iter_dialog_styles():
    """
    Iterates through the available Hotkey Dialog class names and their labels.
    """
    for dialog_class in DIALOG_CLASSES:
        yield dialog_class.__name__, dialog_class.label


def set_dialog_style(label_text):
    """
    Sets the Hotkey Dialog class name from a given label name.
    """
    import a2core
    a2 = a2core.A2Obj.inst()

    for class_name, class_label in iter_dialog_styles():
        if class_label == label_text:
            a2.db.set(Vars.dialog_style_setting, class_name)
            return


def get_current_style():
    """
    Returns the currently set Hotkey Dialog CLASS name.

    :rtype: str
    """
    import a2core
    a2 = a2core.A2Obj.inst()
    return a2.db.get(Vars.dialog_style_setting) or DIALOG_DEFAULT.__name__
