"""
singlesiding supports PySide2 and 6 but needs to adapt to whats
already imported NOT whats available! Thus we deal with it here.
"""
import sys

if 'PySide6' in sys.modules:
    from PySide6 import QtCore, QtWidgets, QtNetwork
elif 'PySide2' in sys.modules:
    from PySide2 import QtCore, QtWidgets, QtNetwork
    QtWidgets.QApplication.exec = QtWidgets.QApplication.exec_
else:
    try:
        from PySide6 import QtCore, QtWidgets, QtNetwork
    except ImportError:
        from PySide2 import QtCore, QtWidgets, QtNetwork
        QtWidgets.QApplication.exec = QtWidgets.QApplication.exec_
