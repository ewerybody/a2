import typing

import a2ui
import a2mod
from a2element.common import DrawCtrl, EditCtrl
import a2ctrl.icons
from a2ctrl.icons import Ico

Icons: a2ctrl.icons._Icons

def draw(
    main: a2ui.A2Window, element_cfg: dict[str, str], mod: a2mod.Mod, user_cfg: dict[str, str]
) -> DrawCtrl: ...
def edit(
    element_cfg: dict[str, str], main: a2ui.A2Window, user_cfg: dict[str, str]
) -> EditCtrl: ...
def get_cfg_value(
    element_cfg: dict,
    user_cfg: dict,
    attr_name: str = ...,
    typ: typing.Any = ...,
    default: typing.Any = ...,
) -> typing.Any: ...

def iter_element_cfg_type(cfg_list: list[dict], typ: typing.Optional[str] = ...) -> dict: ...