import logging
import typing
from singlesiding import QSingleApplication
from a2qt import QtWidgets
import a2app
import a2db
import a2ui
import a2modsource

A2DEFAULT_HOTKEY: str
EDIT_DISCLAIMER: str
NAME: str

class A2Obj:
    """Non-Ui a2 backend object."""

    _instance: object

    app: a2app.A2App = ...
    win: a2ui.A2Window = ...
    paths: Paths
    urls: URLs
    db: a2db.A2db
    dev_mode: bool

    enabled: typing.Dict[str, typing.List[str]]
    module_sources: typing.Dict[str, a2modsource.ModSource]
    def __init__(self) -> None: ...
    @classmethod
    def inst(cls) -> A2Obj: ...
    def start_up(self) -> None: ...
    def fetch_modules(self) -> None: ...
    def fetch_modules_if_stale(self) -> None: ...

class Paths:
    """Aquires and hosts common paths around a2."""

    a2: str
    a2exe: str
    a2uiexe: str
    a2_config: str
    a2_script: str
    a2_urls: str
    autohotkey: str
    data: str
    defaults: str
    elements: str
    includes: str
    git: str
    lib: str
    uninstaller: str
    widgets: str
    def set_data_path(self, str): ...
    def write_user_include(self): ...

class URLs:
    a2: str
    help: str
    wiki: str
    helpEditCtrl: str
    helpHotkey: str
    helpCheckbox: str
    help_scopes: str
    help_string: str
    help_number: str
    help_path: str
    report_bug: str
    report_sugg: str
    security: str
    ahk: str
    ahk_commands: str
    ahk_run: str
    ahk_send: str
    ahkWinActive: str
    ahk_builtin_vars: str
    ahkWinTitle: str

def get_logger(str) -> logging.Logger: ...
def set_loglevel(debug: bool = False): ...
def tags() -> dict[str, str]:
    """Return tags dictionary with shortnames/english desctiptions."""
