import logging
import typing
import typing
from singlesiding import QSingleApplication
from a2qt import QtWidgets
import a2db
import a2modsource

A2DEFAULT_HOTKEY: str
EDIT_DISCLAIMER: str

class A2Obj(object):
    """Non-Ui a2 backend object."""

    _instance: object

    app: typing.Optional[QSingleApplication] = None
    win: typing.Optional[QtWidgets.QMainWindow] = None
    paths: Paths
    db: a2db.A2db

    enabled: typing.Dict[str, typing.List[str]]
    module_sources: typing.Dict[str, a2modsource.ModSource]

    def __init__(self) -> None: ...
    @classmethod
    def inst(cls) -> A2Obj: ...
    def start_up(self) -> None: ...
    def fetch_modules(self) -> None: ...

class Paths(object):
    """Aquires and hosts common paths around a2."""

    a2: str
    autohotkey: str
    data: str
    defaults: str
    includes: str
    lib: str
    def set_data_path(self, str): ...
    def write_user_include(self): ...

def get_logger(str) -> logging.Logger: ...
