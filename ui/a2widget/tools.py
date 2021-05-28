"""Qt Widget tools"""


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
