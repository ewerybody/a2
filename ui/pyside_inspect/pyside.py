try:
    import PySide6
    from PySide6 import __all__
    NAME = PySide6.__name__
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
    qt_docs_url = 'https://doc.qt.io/qtforpython-6/PySide6/{mod}/{cls}.html'
except ImportError:
    import PySide2
    from PySide2 import __all__
    NAME = PySide2.__name__
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    qt_docs_url = 'https://doc.qt.io/qtforpython-5/PySide2/{mod}/{cls}.html'