"""
a2qt Qt for Python wrapper.
"""
import a2qt

if a2qt.QT_VERSION == 6:
    from PySide6.QtOpenGL import *

else:
    from PySide2.QtGui import (
        QAbstractOpenGLFunctions, QOpenGLBuffer, QOpenGLDebugLogger,
        QOpenGLDebugMessage, QOpenGLFramebufferObject,
        QOpenGLFramebufferObjectFormat, QOpenGLPixelTransferOptions,
        QOpenGLShader, QOpenGLShaderProgram, QOpenGLTexture,
        QOpenGLTextureBlitter, QOpenGLTimeMonitor, QOpenGLTimerQuery,
        QOpenGLVersionProfile, QOpenGLVertexArrayObject, QOpenGLWindow)
