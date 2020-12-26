"""
a2qt Qt for Python wrapper.
"""
import a2qt
if a2qt.QT_VERSION == 6:
    from PySide6.QtGui import *

else:
    from PySide2.QtGui import (
        QAbstractTextDocumentLayout, QAccessible,
        QAccessibleEditableTextInterface, QAccessibleEvent, QAccessibleInterface,
        QAccessibleObject, QAccessibleStateChangeEvent,
        QAccessibleTableCellInterface, QAccessibleTableModelChangeEvent,
        QAccessibleTextCursorEvent, QAccessibleTextInsertEvent,
        QAccessibleTextInterface, QAccessibleTextRemoveEvent,
        QAccessibleTextSelectionEvent, QAccessibleTextUpdateEvent,
        QAccessibleValueChangeEvent, QAccessibleValueInterface, QActionEvent,
        QBackingStore, QBitmap, QBrush, QClipboard, QCloseEvent, QColor,
        QColorConstants, QColorSpace, QConicalGradient, QContextMenuEvent,
        QCursor, QDesktopServices, QDoubleValidator, QDrag, QDragEnterEvent,
        QDragLeaveEvent, QDragMoveEvent, QDropEvent, QEnterEvent, QExposeEvent,
        QFileOpenEvent, QFocusEvent, QFont, QFontDatabase, QFontInfo,
        QFontMetrics, QFontMetricsF, QGradient, QGuiApplication, QHelpEvent,
        QHideEvent, QHoverEvent, QIcon, QIconDragEvent, QIconEngine, QImage,
        QImageIOHandler, QImageReader, QImageWriter, QInputEvent, QInputMethod,
        QInputMethodEvent, QInputMethodQueryEvent, QIntValidator, QKeyEvent,
        QKeySequence, QLinearGradient, QMatrix2x2, QMatrix2x3, QMatrix2x4,
        QMatrix3x2, QMatrix3x3, QMatrix3x4, QMatrix4x2, QMatrix4x3, QMatrix4x4,
        QMouseEvent, QMoveEvent, QMovie, QNativeGestureEvent, QOffscreenSurface,
        QOpenGLContext, QOpenGLContextGroup, QOpenGLExtraFunctions,
        QOpenGLFunctions, QPageLayout, QPageSize, QPagedPaintDevice,
        QPaintDevice, QPaintDeviceWindow, QPaintEngine, QPaintEngineState,
        QPaintEvent, QPainter, QPainterPath, QPainterPathStroker, QPalette,
        QPdfWriter, QPen, QPicture, QPixelFormat, QPixmap, QPixmapCache,
        QPointingDeviceUniqueId, QPolygon, QPolygonF, QPyTextObject, QQuaternion,
        QRadialGradient, QRasterWindow, QRawFont, QRegion,
        QRegularExpressionValidator, QResizeEvent, QScreen, QScrollEvent,
        QScrollPrepareEvent, QSessionManager, QShortcutEvent, QShowEvent,
        QStandardItem, QStandardItemModel, QStaticText, QStatusTipEvent,
        QStyleHints, QSurface, QSurfaceFormat, QSyntaxHighlighter, QTabletEvent,
        QTextBlock, QTextBlockFormat, QTextBlockGroup, QTextBlockUserData,
        QTextCharFormat, QTextCursor, QTextDocument, QTextDocumentFragment,
        QTextDocumentWriter, QTextFormat, QTextFragment, QTextFrame,
        QTextFrameFormat, QTextImageFormat, QTextInlineObject, QTextItem,
        QTextLayout, QTextLength, QTextLine, QTextList, QTextListFormat,
        QTextObject, QTextObjectInterface, QTextOption, QTextTable,
        QTextTableCell, QTextTableCellFormat, QTextTableFormat,
        QToolBarChangeEvent, QTouchEvent, QTransform, QValidator, QVector2D,
        QVector3D, QVector4D, QWhatsThisClickedEvent, QWheelEvent, QWindow,
        QWindowStateChangeEvent, Qt, qAlpha, qBlue, qGray, qGreen, qIsGray, qRed,
        qRgb, qRgba)
    from PySide2.QtWidgets import (
        QAction, QActionGroup, QShortcut, QUndoCommand, QUndoGroup, QUndoStack)
