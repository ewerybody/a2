try:
    import PySide6
    from PySide6 import __all__
    NAME = PySide6.__name__
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
except ImportError:
    import PySide2
    from PySide2 import __all__
    NAME = PySide2.__name__
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
