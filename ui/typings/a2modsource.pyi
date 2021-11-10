import a2core
import a2mod
from a2qt import QtGui

class ModSource:
    name: str
    icon: QtGui.QIcon
    mods: dict[str, a2mod.Mod]
    def __init__(self, a2: a2core.A2Obj, name: str) -> None: ...

def create(name: str, author_name: str, author_url: str) -> None: ...
