###############################################################################
#
# Copyright 2012 Siding Developers (see AUTHORS.txt)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
Functions for enabling and disabling Aero Glass on
:class:`~PySide.QtGui.QWidget` instances.
"""

###############################################################################
# Imports
###############################################################################

import weakref

from PySide.QtCore import Qt
from PySide.QtGui import QColor

from ctypes.wintypes import DWORD, HRGN
from ctypes import windll, c_bool, c_int, POINTER, Structure
from ctypes import pythonapi, c_void_p, py_object
from ctypes import WINFUNCTYPE

###############################################################################
# Constants and Structures
###############################################################################

DWM_BB_ENABLE               = 0x0001
DWM_BB_BLURREGION           = 0x0002
DWM_BB_TRANSITIONMAXIMIZED  = 0x0003
WM_DWMCOMPOSITIONCHANGED    = 0x031E

class DWM_BLURBEHIND(Structure):
    """
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa969500%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('dwFlags', DWORD),
        ('fEnable', c_bool),
        ('hRgnBlur', HRGN),
        ('fTransitionOnMaximized', c_bool)
        ]

class MARGINS(Structure):
    """
    http://msdn.microsoft.com/en-us/library/windows/desktop/bb773244%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('cxLeftWidth', c_int),
        ('cxRightWidth', c_int),
        ('cyTopHeight', c_int),
        ('cyBottomHeight', c_int)
        ]

###############################################################################
# The Widget Manager
###############################################################################

class WidgetManager(object):
    """
    The WidgetManager is a special class that keeps track of widgets with
    Aero Glass styling, and that responds to the WM_DWMCOMPOSITIONCHANGED
    message.
    """
    def __init__(self):
        self._widgets = {}
        self._sys_enabled = DWM_is_composition_enabled()
        self._enabled = False

    @property
    def status(self):
        """ Whether or not Aero is currently alive. """
        return self._sys_enabled and self._enabled

    def attach(self, app):
        """ Connect to the ``compositionChanged`` slot of the given app. """
        app.compositionChanged.connect(self.compositionChanged)

    def compositionChanged(self):
        """
        Update the state of Aero Glass on all widgets when the
        WM_DWMCOMPOSITIONCHANGED message is received.
        """
        enabled = DWM_is_composition_enabled()
        if enabled == self._sys_enabled or not self._enabled:
            return
        self._update_widgets()
        from siding import style
        style.reload()

    def enable(self):
        """
        Enable Aero.
        """
        if self._enabled:
            return
        self._enabled = True
        if self._sys_enabled:
            self._update_widgets()
    
    def disable(self):
        """
        Disable Aero.
        """
        if not self._enabled:
            return
        self._enabled = False
        if self._sys_enabled:
            self._update_widgets()
    
    def _update_widgets(self):
        """
        Iterate every widget we're managing, and enable or disable Aero on it.
        """
        state = self._enabled and self._sys_enabled
        
        for ref in self._widgets.keys():
            widget = ref()
            if not widget:
                del self._widgets[ref]
                continue
            
            self._update_widget(state, widget, self._widgets[ref])
    
    def _update_widget(self, state, widget, info):
        """
        Update a widget, either enabling or disabling Aero.
        """
        if state == info[0]:
            return
        
        if state:
            # We're enabling Aero.
            if DWM_extend_frame_into_client_area(widget, MARGINS(*info[1])):
                if DWM_enable_blur_behind_window(widget):
                    info[0] = True
                else:
                    DWM_retract_frame(widget)
        else:
            # We're disabling Aero.
            DWM_enable_blur_behind_window(widget, False)
            DWM_retract_frame(widget)
            info[0] = False

    def _find_widget(self, widget):
        """
        Find the widget in our list of tracked widgets and return the weak
        reference.
        """
        for ref in self._widgets.keys():
            wid = ref()
            if not wid:
                del self._widgets[ref]
                continue
            if wid is widget:
                return ref
    
    def add(self, widget, margin=(-1,-1,-1,-1)):
        """
        Enable Aero Glass on the QWidget widget.
        """
        state = self._enabled and self._sys_enabled
        
        ref = self._find_widget(widget)
        if ref:
            self.remove(widget)
        
        ref = weakref.ref(widget)
        self._widgets[ref] = info = [False, margin]
        
        if state:
            self._update_widget(True, widget, info)
    
    def remove(self, widget):
        """
        Disable Aero Glass on the QWidget widget and stop tracking it.
        """
        ref = self._find_widget(widget)
        if not ref:
            return
        
        info = self._widgets[ref]
        if info[0]:
            self._update_widget(False, widget, info)
        
        del self._widgets[ref]

###############################################################################
# Wrapped Functions
###############################################################################

pythonapi.PyCObject_AsVoidPtr.restype = c_void_p
pythonapi.PyCObject_AsVoidPtr.argtypes = [ py_object ]

prototype = WINFUNCTYPE(c_int, c_int, POINTER(MARGINS))
params = (1,"hWnd",0), (1,"pMarInset",MARGINS(-1,-1,-1,-1))
_DwmExtendFrameIntoClientArea = prototype(("DwmExtendFrameIntoClientArea",
                                    windll.dwmapi), params)

prototype = WINFUNCTYPE(c_int, c_int, POINTER(DWM_BLURBEHIND))
params = (1, "hWnd", 0), (1, "pBlurBehind", 0)
_DwmEnableBlurBehindWindow = prototype(("DwmEnableBlurBehindWindow",
                                    windll.dwmapi), params)

prototype = WINFUNCTYPE(c_int, POINTER(DWORD), POINTER(c_bool))
params = (2, "pcrColorization", DWORD(0)), (1, "pfOpaqueBlend", c_bool(False))
_DwmGetColorizationColor = prototype(("DwmGetColorizationColor",
                                    windll.dwmapi), params)

prototype = WINFUNCTYPE(c_int, POINTER(c_bool))
params = (2, "pfEnabled", c_bool(False)),
_DwmIsCompositionEnabled = prototype(("DwmIsCompositionEnabled",
                                    windll.dwmapi), params)

# Before we get started, see if we have the DWM functions.
has_dwm = hasattr(windll, 'dwmapi') and \
          hasattr(windll.dwmapi, 'DwmIsCompositionEnabled')

def DWM_is_composition_enabled():
    """
    Returns True if DWM composition is currently enabled on the system. This
    value can change over the life of an application.
    """
    if not has_dwm:
        return False

    return _DwmIsCompositionEnabled()

def DWM_retract_frame(widget):
    """
    Undo DWM_extend_frame_into_client_area on the provided widget.
    """
    if not has_dwm:
        return False

    m = MARGINS(0, 0, 0, 0)
    result = _DwmExtendFrameIntoClientArea(pythonapi.PyCObject_AsVoidPtr(
                widget.winId()), m)
    if result:
        return False

    widget.setAttribute(Qt.WA_TranslucentBackground, False)
    return True

def DWM_extend_frame_into_client_area(widget, margin):
    """
    Extend the window frame into the client area. Margins of -1 (the default)
    will result in the entire window being rendered as the frame.

    Note: You should not call DWM_enable_blur_behind_window before calling
    this function.
    """
    if not has_dwm:
        return False

    result = _DwmExtendFrameIntoClientArea(pythonapi.PyCObject_AsVoidPtr(
                widget.winId()), margin)
    
    widget.setAttribute(Qt.WA_TranslucentBackground, not result)
    return not result

def DWM_enable_blur_behind_window(widget, enable=True):
    """
    Enable or disable blur behind window on a window.
    """
    if not has_dwm:
        return False

    bb = DWM_BLURBEHIND()
    bb.fEnable = c_bool(enable)
    bb.dwFlags = DWM_BB_ENABLE
    bb.hRgnBlur = None

    widget.setAttribute(Qt.WA_TranslucentBackground, enable)
    widget.setAttribute(Qt.WA_NoSystemBackground, enable)

    result = _DwmEnableBlurBehindWindow(pythonapi.PyCObject_AsVoidPtr(
                widget.winId()), bb)
    
    return not result

def DWM_colorization_color():
    """
    Returns the current colorization color for the window.
    """
    color = _DwmGetColorizationColor()
    return QColor(color)

###############################################################################
# Initialization
###############################################################################

manager = WidgetManager()


enable = manager.enable
disable = manager.disable

add = manager.add
remove = manager.remove
