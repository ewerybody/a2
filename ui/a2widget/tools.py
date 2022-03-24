"""Qt Widget tools"""


from a2qt import QtCore, QtGui, QtWidgets


class BlockSignalContext:
    """
    Make sure signals are blocked during some setting operation
    and they're released on exit if not already blocked before.

        with BlockSignalContext(self):
            self.setData(some_data)
    """

    def __init__(self, widget):
        self.widget = widget
        self.signals_blocked = widget.signalsBlocked()

    def __enter__(self):
        if not self.signals_blocked:
            self.widget.blockSignals(True)

    def __exit__(self, *args):
        if not self.signals_blocked:
            self.widget.blockSignals(False)


def get_screen(geometry):
    # type: (QtCore.QRect | QtCore.QRectF) -> QtGui.QScreen
    """Get the screen object a geometry rectangle is on.
    If none is found take the cursor position.
    """
    center = geometry.center()
    pointer_pos = None
    pointer_screen = None
    for screen in QtWidgets.QApplication.screens():
        if screen.geometry().contains(center):
            return screen
        if pointer_pos is None:
            pointer_pos = QtGui.QCursor.pos()
        if screen.geometry().contains(pointer_pos):
            pointer_screen = screen
    if pointer_screen is None:
        raise RuntimeError(
            'Ridiculous Error to make type checker happy .. I mean to get '
            'here neither geometry center NOR pointer would be on any screen!'
        )
    return pointer_screen


def fit_to_sceen(geometry):
    # type: (QtCore.QRect | QtCore.QRectF) -> None
    """Make sure a window geometry is fully visible on the current screen."""
    screen = get_screen(geometry).geometry()
    # make sure that the titles fit into the screen as well.
    screen.setY(30)
    if not screen.contains(geometry.topLeft()):
        corner = geometry.topLeft() - screen.topLeft()
        geometry.translate(-min(corner.x(), 0), -min(corner.y(), screen.top()))

    if not screen.contains(geometry.bottomRight()):
        corner = screen.bottomRight() - geometry.bottomRight()
        geometry.translate(min(corner.x(), 0), min(corner.y(), 0))
