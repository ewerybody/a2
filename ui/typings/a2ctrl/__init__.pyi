import a2ui
import a2mod
from a2element.common import DrawCtrl, EditCtrl
from a2ctrl.icons import Ico, Icons

def draw(
    main: a2ui.A2Window, element_cfg: dict[str, str], mod: a2mod.Mod, user_cfg: dict[str, str]
) -> DrawCtrl: ...
def edit(
    element_cfg: dict[str, str], main: a2ui.A2Window, user_cfg: dict[str, str]
) -> EditCtrl: ...
