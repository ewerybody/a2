"""
a2qt Qt for Python wrapper.
"""
import a2qt

if a2qt.QT_VERSION == 6:
    from PySide6.QtSql import *

else:
    from PySide2.QtSql import *
