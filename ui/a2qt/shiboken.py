"""
a2qt Qt for Python wrapper.
"""
import a2qt

if a2qt.QT_VERSION == 6:
    from shiboken6 import *

else:
    from shiboken2 import *
