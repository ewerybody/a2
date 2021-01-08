"""
a2qt Qt for Python wrapper.
"""
import a2qt
if a2qt.QT_VERSION == 6:
    from PySide6.QtCore import *
    from PySide6.QtCore import __version__, __version_info__

else:
    from PySide2.QtCore import (
        ClassInfo, MetaFunction, MetaSignal, Property, QAbstractAnimation,
        QAbstractEventDispatcher, QAbstractItemModel, QAbstractListModel,
        QAbstractNativeEventFilter, QAbstractProxyModel, QAbstractTableModel,
        QAnimationGroup, QBasicMutex, QBasicTimer, QBitArray, QBuffer,
        QByteArray, QByteArrayMatcher, QCalendar, QCborArray, QCborError,
        QCborKnownTags, QCborMap, QCborParserError, QCborSimpleType,
        QCborStreamReader, QCborStreamWriter, QCborStringResultByteArray,
        QCborStringResultString, QCborValue, QChildEvent, QCollator,
        QCollatorSortKey, QCommandLineOption, QCommandLineParser,
        QConcatenateTablesProxyModel, QCoreApplication, QCryptographicHash,
        QDataStream, QDate, QDateTime, QDeadlineTimer, QDir, QDirIterator,
        QDynamicPropertyChangeEvent, QEasingCurve, QElapsedTimer, QEnum, QEvent,
        QEventLoop, QFactoryInterface, QFile, QFileDevice, QFileInfo,
        QFileSelector, QFileSystemWatcher, QFlag, QFutureInterfaceBase,
        QGenericArgument, QGenericReturnArgument, QIODevice, QIdentityProxyModel,
        QItemSelection, QItemSelectionModel, QItemSelectionRange, QJsonArray,
        QJsonDocument, QJsonParseError, QJsonValue, QLibraryInfo, QLine, QLineF,
        QLocale, QLockFile, QMargins, QMarginsF, QMessageAuthenticationCode,
        QMessageLogContext, QMetaClassInfo, QMetaEnum, QMetaMethod, QMetaObject,
        QMetaProperty, QMimeData, QMimeDatabase, QMimeType, QModelIndex, QMutex,
        QMutexLocker, QObject, QOperatingSystemVersion, QParallelAnimationGroup,
        QPauseAnimation, QPersistentModelIndex, QPluginLoader, QPoint, QPointF,
        QProcess, QProcessEnvironment, QPropertyAnimation, QRandomGenerator,
        QRandomGenerator64, QReadLocker, QReadWriteLock, QRect, QRectF,
        QRecursiveMutex, QRegularExpression, QRegularExpressionMatch,
        QRegularExpressionMatchIterator, QResource, QRunnable, QSaveFile,
        QSemaphore, QSemaphoreReleaser, QSequentialAnimationGroup, QSettings,
        QSignalBlocker, QSignalMapper, QSize, QSizeF, QSocketDescriptor,
        QSocketNotifier, QSortFilterProxyModel, QStandardPaths, QStorageInfo,
        QStringListModel, QSysInfo, QSystemSemaphore, QT_TRANSLATE_NOOP,
        QT_TRANSLATE_NOOP3, QT_TRANSLATE_NOOP_UTF8, QT_TR_NOOP, QT_TR_NOOP_UTF8,
        QTemporaryDir, QTemporaryFile, QTextBoundaryFinder, QTextStream,
        QTextStreamManipulator, QThread, QThreadPool, QTime, QTimeLine,
        QTimeZone, QTimer, QTimerEvent, QTranslator, QTransposeProxyModel, QUrl,
        QUrlQuery, QUuid, QVariantAnimation, QVersionNumber, QWaitCondition,
        QWinEventNotifier, QWriteLocker, QXmlStreamAttribute,
        QXmlStreamAttributes, QXmlStreamEntityDeclaration,
        QXmlStreamEntityResolver, QXmlStreamNamespaceDeclaration,
        QXmlStreamNotationDeclaration, QXmlStreamReader, QXmlStreamWriter,
        QtCriticalMsg, QtDebugMsg, QtFatalMsg, QtInfoMsg, QtMsgType, QtSystemMsg,
        QtWarningMsg, SIGNAL, SLOT, Signal, SignalInstance, Slot, qAbs,
        qAddPostRoutine, qCompress, qCritical, qDebug, qFastCos, qFastSin,
        qFatal, qFuzzyCompare, qFuzzyIsNull, qInstallMessageHandler, qIsFinite,
        qIsInf, qIsNaN, qIsNull, qRegisterResourceData, qUncompress,
        qUnregisterResourceData, qVersion, qWarning, qtTrId)
    from PySide2.QtGui import Qt
    from PySide2.QtCore import __version__, __version_info__
