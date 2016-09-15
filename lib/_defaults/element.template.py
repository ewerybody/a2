"""
{description}

@created: {creation_date}
@author: {author_name}
"""
import a2ctrl
from PySide import QtGui
from a2element import DrawCtrl, EditCtrl


class Draw(DrawCtrl):
    """
    blaaaa
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        pass


class Edit(EditCtrl):
    """
    blaaa
    """
    def __init__(self, cfg, main, parentCfg):
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
    @staticmethod
    def element_name():
        return '{element_name}'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().check


def get_settings(module_key, cfg, db_dict, user_cfg):
    #db_dict.setdefault('variables', {})
    #value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=bool, default=False)
    #db_dict['variables'][cfg['name']] = value
    pass
