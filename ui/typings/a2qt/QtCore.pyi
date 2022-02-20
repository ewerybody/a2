#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################
"""
This file contains the exact signatures for all functions in module
PySide6.QtCore, except for defaults which are replaced by "...".
"""

# Module `PySide6.QtCore`

from shiboken6 import Shiboken

import os
from enum import Enum
from typing import Any, Callable, Optional, Tuple, Type, Union, Sequence, Dict, List, overload
from a2qt import QtWidgets

__version__: str

class ClassInfo(object):
    def __init__(self, **info: Dict[str, str]) -> None: ...

class MetaFunction(object):
    def __call__(self, *args: Any) -> Any: ...

class MetaSignal(type):
    def __instancecheck__(self, object: object) -> bool: ...

class Property(object):
    def __init__(
        self,
        type: type,
        fget: Optional[Callable] = ...,
        fset: Optional[Callable] = ...,
        freset: Optional[Callable] = ...,
        fdel: Optional[Callable] = ...,
        doc: str = ...,
        notify: Optional[Callable] = ...,
        designable: bool = ...,
        scriptable: bool = ...,
        stored: bool = ...,
        user: bool = ...,
        constant: bool = ...,
        final: bool = ...,
    ) -> Property: ...
    def deleter(self, fdel: Callable) -> Property: ...
    def getter(self, fget: Callable) -> Property: ...
    def read(self, fget: Callable) -> Property: ...
    def setter(self, fset: Callable) -> Property: ...
    def write(self, fset: Callable) -> Property: ...

class PyClassProperty(property):
    @classmethod
    def __init__(
        cls,
        fget: Optional[Callable[[Any], Any]] = ...,
        fset: Optional[Callable[[Any, Any], NoneType]] = ...,
        fdel: Optional[Callable[[Any], NoneType]] = ...,
        doc: Optional[str] = ...,
    ) -> PyClassProperty: ...

class QAbstractAnimation(QObject):

    KeepWhenStopped: QAbstractAnimation.DeletionPolicy = ...  # 0x0
    DeleteWhenStopped: QAbstractAnimation.DeletionPolicy = ...  # 0x1
    Forward: QAbstractAnimation.Direction = ...  # 0x0
    Backward: QAbstractAnimation.Direction = ...  # 0x1
    Stopped: QAbstractAnimation.State = ...  # 0x0
    Paused: QAbstractAnimation.State = ...  # 0x1
    Running: QAbstractAnimation.State = ...  # 0x2
    class DeletionPolicy(Enum):

        KeepWhenStopped: QAbstractAnimation.DeletionPolicy = ...  # 0x0
        DeleteWhenStopped: QAbstractAnimation.DeletionPolicy = ...  # 0x1
    class Direction(Enum):

        Forward: QAbstractAnimation.Direction = ...  # 0x0
        Backward: QAbstractAnimation.Direction = ...  # 0x1
    class State(Enum):

        Stopped: QAbstractAnimation.State = ...  # 0x0
        Paused: QAbstractAnimation.State = ...  # 0x1
        Running: QAbstractAnimation.State = ...  # 0x2
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def currentLoop(self) -> int: ...
    def currentLoopTime(self) -> int: ...
    def currentTime(self) -> int: ...
    def direction(self) -> QAbstractAnimation.Direction: ...
    def duration(self) -> int: ...
    def event(self, event: QEvent) -> bool: ...
    def group(self) -> QAnimationGroup: ...
    def loopCount(self) -> int: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def setCurrentTime(self, msecs: int) -> None: ...
    def setDirection(self, direction: QAbstractAnimation.Direction) -> None: ...
    def setLoopCount(self, loopCount: int) -> None: ...
    def setPaused(self, arg__1: bool) -> None: ...
    def start(self, policy: QAbstractAnimation.DeletionPolicy = ...) -> None: ...
    def state(self) -> QAbstractAnimation.State: ...
    def stop(self) -> None: ...
    def totalDuration(self) -> int: ...
    def updateCurrentTime(self, currentTime: int) -> None: ...
    def updateDirection(self, direction: QAbstractAnimation.Direction) -> None: ...
    def updateState(
        self, newState: QAbstractAnimation.State, oldState: QAbstractAnimation.State
    ) -> None: ...

class QAbstractEventDispatcher(QObject):
    class TimerInfo(Shiboken.Object):
        @overload
        def __init__(self, TimerInfo: QAbstractEventDispatcher.TimerInfo) -> None: ...
        @overload
        def __init__(self, id: int, i: int, t: Qt.TimerType) -> None: ...
        @staticmethod
        def __copy__() -> None: ...
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def closingDown(self) -> None: ...
    def filterNativeEvent(
        self, eventType: Union[QByteArray, bytes], message: int
    ) -> Tuple[bool, int]: ...
    def installNativeEventFilter(self, filterObj: QAbstractNativeEventFilter) -> None: ...
    @staticmethod
    def instance(thread: Optional[QThread] = ...) -> QAbstractEventDispatcher: ...
    def interrupt(self) -> None: ...
    def processEvents(self, flags: QEventLoop.ProcessEventsFlags) -> bool: ...
    def registerSocketNotifier(self, notifier: QSocketNotifier) -> None: ...
    @overload
    def registerTimer(self, interval: int, timerType: Qt.TimerType, object: QObject) -> int: ...
    @overload
    def registerTimer(
        self, timerId: int, interval: int, timerType: Qt.TimerType, object: QObject
    ) -> None: ...
    def registeredTimers(self, object: QObject) -> List[QAbstractEventDispatcher.TimerInfo]: ...
    def remainingTime(self, timerId: int) -> int: ...
    def removeNativeEventFilter(self, filterObj: QAbstractNativeEventFilter) -> None: ...
    def startingUp(self) -> None: ...
    def unregisterSocketNotifier(self, notifier: QSocketNotifier) -> None: ...
    def unregisterTimer(self, timerId: int) -> bool: ...
    def unregisterTimers(self, object: QObject) -> bool: ...
    def wakeUp(self) -> None: ...

class QAbstractItemModel(QObject):

    NoLayoutChangeHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x0
    VerticalSortHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x1
    HorizontalSortHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x2
    class CheckIndexOption(Enum):

        NoOption: QAbstractItemModel.CheckIndexOption = ...  # 0x0
        IndexIsValid: QAbstractItemModel.CheckIndexOption = ...  # 0x1
        DoNotUseParent: QAbstractItemModel.CheckIndexOption = ...  # 0x2
        ParentIsInvalid: QAbstractItemModel.CheckIndexOption = ...  # 0x4
    class CheckIndexOptions(object): ...
    class LayoutChangeHint(Enum):

        NoLayoutChangeHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x0
        VerticalSortHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x1
        HorizontalSortHint: QAbstractItemModel.LayoutChangeHint = ...  # 0x2
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def beginInsertColumns(
        self, parent: Union[QModelIndex, QPersistentModelIndex], first: int, last: int
    ) -> None: ...
    def beginInsertRows(
        self, parent: Union[QModelIndex, QPersistentModelIndex], first: int, last: int
    ) -> None: ...
    def beginMoveColumns(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceFirst: int,
        sourceLast: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationColumn: int,
    ) -> bool: ...
    def beginMoveRows(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceFirst: int,
        sourceLast: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationRow: int,
    ) -> bool: ...
    def beginRemoveColumns(
        self, parent: Union[QModelIndex, QPersistentModelIndex], first: int, last: int
    ) -> None: ...
    def beginRemoveRows(
        self, parent: Union[QModelIndex, QPersistentModelIndex], first: int, last: int
    ) -> None: ...
    def beginResetModel(self) -> None: ...
    def buddy(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def canDropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def canFetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def changePersistentIndex(
        self,
        from_: Union[QModelIndex, QPersistentModelIndex],
        to: Union[QModelIndex, QPersistentModelIndex],
    ) -> None: ...
    def changePersistentIndexList(self, from_: List[int], to: List[int]) -> None: ...
    def checkIndex(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        options: QAbstractItemModel.CheckIndexOptions = ...,
    ) -> bool: ...
    def clearItemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    @overload
    def createIndex(self, row: int, column: int, id: int = ...) -> QModelIndex: ...
    @overload
    def createIndex(self, row: int, column: int, ptr: object) -> QModelIndex: ...
    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any: ...
    def decodeData(
        self,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
        stream: QDataStream,
    ) -> bool: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def encodeData(self, indexes: List[int], stream: QDataStream) -> None: ...
    def endInsertColumns(self) -> None: ...
    def endInsertRows(self) -> None: ...
    def endMoveColumns(self) -> None: ...
    def endMoveRows(self) -> None: ...
    def endRemoveColumns(self) -> None: ...
    def endRemoveRows(self) -> None: ...
    def endResetModel(self) -> None: ...
    def fetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool: ...
    def hasIndex(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    def insertColumn(
        self, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertRow(
        self, row: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def itemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Dict[int, Any]: ...
    def match(
        self,
        start: Union[QModelIndex, QPersistentModelIndex],
        role: int,
        value: Any,
        hits: int = ...,
        flags: Qt.MatchFlags = ...,
    ) -> List[int]: ...
    def mimeData(self, indexes: List[int]) -> QMimeData: ...
    def mimeTypes(self) -> List[str]: ...
    def moveColumn(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceColumn: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def moveColumns(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceColumn: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def moveRow(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceRow: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def moveRows(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceRow: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, child: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def persistentIndexList(self) -> List[int]: ...
    def removeColumn(
        self, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeRow(
        self, row: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def resetInternalData(self) -> None: ...
    def revert(self) -> None: ...
    def roleNames(self) -> Dict[int, QByteArray]: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setData(
        self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = ...
    ) -> bool: ...
    def setHeaderData(
        self, section: int, orientation: Qt.Orientation, value: Any, role: int = ...
    ) -> bool: ...
    def setItemData(
        self, index: Union[QModelIndex, QPersistentModelIndex], roles: Dict[int, Any]
    ) -> bool: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def sort(self, column: int, order: Qt.SortOrder = ...) -> None: ...
    def span(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize: ...
    def submit(self) -> bool: ...
    def supportedDragActions(self) -> Qt.DropActions: ...
    def supportedDropActions(self) -> Qt.DropActions: ...

class QAbstractListModel(QAbstractItemModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> int: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def index(
        self, row: int, column: int = ..., parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, child: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...

class QAbstractNativeEventFilter(Shiboken.Object):
    def __init__(self) -> None: ...
    def nativeEventFilter(
        self, eventType: Union[QByteArray, bytes], message: int
    ) -> Tuple[object, int]: ...

class QAbstractProxyModel(QAbstractItemModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def buddy(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def canDropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def canFetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def clearItemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def createSourceIndex(self, row: int, col: int, internalPtr: int) -> QModelIndex: ...
    def data(
        self, proxyIndex: Union[QModelIndex, QPersistentModelIndex], role: int = ...
    ) -> Any: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def fetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def itemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Dict[int, Any]: ...
    def mapFromSource(
        self, sourceIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def mapSelectionFromSource(self, selection: QItemSelection) -> QItemSelection: ...
    def mapSelectionToSource(self, selection: QItemSelection) -> QItemSelection: ...
    def mapToSource(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def mimeData(self, indexes: List[int]) -> QMimeData: ...
    def mimeTypes(self) -> List[str]: ...
    def revert(self) -> None: ...
    def roleNames(self) -> Dict[int, QByteArray]: ...
    def setData(
        self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = ...
    ) -> bool: ...
    def setHeaderData(
        self, section: int, orientation: Qt.Orientation, value: Any, role: int = ...
    ) -> bool: ...
    def setItemData(
        self, index: Union[QModelIndex, QPersistentModelIndex], roles: Dict[int, Any]
    ) -> bool: ...
    def setSourceModel(self, sourceModel: QAbstractItemModel) -> None: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def sort(self, column: int, order: Qt.SortOrder = ...) -> None: ...
    def sourceModel(self) -> QAbstractItemModel: ...
    def span(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize: ...
    def submit(self) -> bool: ...
    def supportedDragActions(self) -> Qt.DropActions: ...
    def supportedDropActions(self) -> Qt.DropActions: ...

class QAbstractTableModel(QAbstractItemModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, child: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...

class QAnimationGroup(QAbstractAnimation):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def addAnimation(self, animation: QAbstractAnimation) -> None: ...
    def animationAt(self, index: int) -> QAbstractAnimation: ...
    def animationCount(self) -> int: ...
    def clear(self) -> None: ...
    def event(self, event: QEvent) -> bool: ...
    def indexOfAnimation(self, animation: QAbstractAnimation) -> int: ...
    def insertAnimation(self, index: int, animation: QAbstractAnimation) -> None: ...
    def removeAnimation(self, animation: QAbstractAnimation) -> None: ...
    def takeAnimation(self, index: int) -> QAbstractAnimation: ...

class QBasicMutex(Shiboken.Object):
    def __init__(self) -> None: ...
    def lock(self) -> None: ...
    def tryLock(self) -> bool: ...
    def try_lock(self) -> bool: ...
    def unlock(self) -> None: ...

class QBasicTimer(Shiboken.Object):
    def __init__(self) -> None: ...
    def isActive(self) -> bool: ...
    @overload
    def start(self, msec: int, obj: QObject) -> None: ...
    @overload
    def start(self, msec: int, timerType: Qt.TimerType, obj: QObject) -> None: ...
    def stop(self) -> None: ...
    def swap(self, other: QBasicTimer) -> None: ...
    def timerId(self) -> int: ...

class QBitArray(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: Union[QBitArray, int]) -> None: ...
    @overload
    def __init__(self, size: int, val: bool = ...) -> None: ...
    def __and__(self, arg__2: Union[QBitArray, int]) -> QBitArray: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iand__(self, arg__1: Union[QBitArray, int]) -> QBitArray: ...
    def __invert__(self) -> QBitArray: ...
    def __ior__(self, arg__1: Union[QBitArray, int]) -> QBitArray: ...
    def __ixor__(self, arg__1: Union[QBitArray, int]) -> QBitArray: ...
    def __or__(self, arg__2: Union[QBitArray, int]) -> QBitArray: ...
    def __xor__(self, arg__2: Union[QBitArray, int]) -> QBitArray: ...
    def at(self, i: int) -> bool: ...
    def bits(self) -> bytes: ...
    def clear(self) -> None: ...
    def clearBit(self, i: int) -> None: ...
    @overload
    def count(self) -> int: ...
    @overload
    def count(self, on: bool) -> int: ...
    @overload
    def fill(self, val: bool, first: int, last: int) -> None: ...
    @overload
    def fill(self, val: bool, size: int = ...) -> bool: ...
    @staticmethod
    def fromBits(data: bytes, len: int) -> QBitArray: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def resize(self, size: int) -> None: ...
    @overload
    def setBit(self, i: int) -> None: ...
    @overload
    def setBit(self, i: int, val: bool) -> None: ...
    def size(self) -> int: ...
    def swap(self, other: Union[QBitArray, int]) -> None: ...
    def testBit(self, i: int) -> bool: ...
    def toUInt32(self, endianness: QSysInfo.Endian) -> Tuple[int, bool]: ...
    def toggleBit(self, i: int) -> bool: ...
    def truncate(self, pos: int) -> None: ...

class QBuffer(QIODevice):
    @overload
    def __init__(self, buf: Union[QByteArray, bytes], parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def atEnd(self) -> bool: ...
    def buffer(self) -> QByteArray: ...
    def canReadLine(self) -> bool: ...
    def close(self) -> None: ...
    def connectNotify(self, arg__1: QMetaMethod) -> None: ...
    def data(self) -> QByteArray: ...
    def disconnectNotify(self, arg__1: QMetaMethod) -> None: ...
    def open(self, openMode: QIODeviceBase.OpenMode) -> bool: ...
    def pos(self) -> int: ...
    def readData(self, data: bytes, maxlen: int) -> object: ...
    def seek(self, off: int) -> bool: ...
    def setBuffer(self, a: Union[QByteArray, bytes]) -> None: ...
    def setData(self, data: Union[QByteArray, bytes]) -> None: ...
    def size(self) -> int: ...
    def writeData(self, data: bytes, len: int) -> int: ...

class QByteArray(Shiboken.Object):

    Base64Encoding: QByteArray.Base64Option = ...  # 0x0
    IgnoreBase64DecodingErrors: QByteArray.Base64Option = ...  # 0x0
    KeepTrailingEquals: QByteArray.Base64Option = ...  # 0x0
    Base64UrlEncoding: QByteArray.Base64Option = ...  # 0x1
    OmitTrailingEquals: QByteArray.Base64Option = ...  # 0x2
    AbortOnBase64DecodingErrors: QByteArray.Base64Option = ...  # 0x4
    class Base64DecodingStatus(Enum):

        Ok: QByteArray.Base64DecodingStatus = ...  # 0x0
        IllegalInputLength: QByteArray.Base64DecodingStatus = ...  # 0x1
        IllegalCharacter: QByteArray.Base64DecodingStatus = ...  # 0x2
        IllegalPadding: QByteArray.Base64DecodingStatus = ...  # 0x3
    class Base64Option(Enum):

        Base64Encoding: QByteArray.Base64Option = ...  # 0x0
        IgnoreBase64DecodingErrors: QByteArray.Base64Option = ...  # 0x0
        KeepTrailingEquals: QByteArray.Base64Option = ...  # 0x0
        Base64UrlEncoding: QByteArray.Base64Option = ...  # 0x1
        OmitTrailingEquals: QByteArray.Base64Option = ...  # 0x2
        AbortOnBase64DecodingErrors: QByteArray.Base64Option = ...  # 0x4
    class Base64Options(object): ...
    class FromBase64Result(Shiboken.Object):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, FromBase64Result: QByteArray.FromBase64Result) -> None: ...
        @staticmethod
        def __copy__() -> None: ...
        def swap(self, other: QByteArray.FromBase64Result) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg__1: bytearray) -> None: ...
    @overload
    def __init__(self, arg__1: bytes) -> None: ...
    @overload
    def __init__(self, arg__1: bytes, size: int = ...) -> None: ...
    @overload
    def __init__(self, arg__1: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, size: int, c: int) -> None: ...
    @overload
    def __add__(self, a2: int) -> QByteArray: ...
    @overload
    def __add__(self, a2: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def __add__(self, arg__1: bytearray) -> QByteArray: ...
    @overload
    def __add__(self, arg__1: bytes) -> None: ...
    @overload
    def __add__(self, s: str) -> str: ...
    @staticmethod
    def __copy__() -> None: ...
    @overload
    def __iadd__(self, a: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def __iadd__(self, arg__1: bytearray) -> QByteArray: ...
    @overload
    def __iadd__(self, c: int) -> QByteArray: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __str__(self) -> object: ...
    @overload
    def append(self, a: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def append(self, c: int) -> QByteArray: ...
    @overload
    def append(self, count: int, c: int) -> QByteArray: ...
    @overload
    def append(self, s: bytes, len: int) -> QByteArray: ...
    def at(self, i: int) -> int: ...
    def back(self) -> int: ...
    def capacity(self) -> int: ...
    def cbegin(self) -> bytes: ...
    def cend(self) -> bytes: ...
    def chop(self, n: int) -> None: ...
    def chopped(self, len: int) -> QByteArray: ...
    def clear(self) -> None: ...
    def compare(self, a: Union[QByteArray, bytes], cs: Qt.CaseSensitivity = ...) -> int: ...
    @overload
    def contains(self, bv: Union[QByteArray, bytes]) -> bool: ...
    @overload
    def contains(self, c: int) -> bool: ...
    @overload
    def count(self) -> int: ...
    @overload
    def count(self, bv: Union[QByteArray, bytes]) -> int: ...
    @overload
    def count(self, c: int) -> int: ...
    def data(self) -> bytes: ...
    @overload
    def endsWith(self, bv: Union[QByteArray, bytes]) -> bool: ...
    @overload
    def endsWith(self, c: int) -> bool: ...
    def erase(self, first: bytes, last: bytes) -> bytes: ...
    def fill(self, c: int, size: int = ...) -> QByteArray: ...
    def first(self, n: int) -> QByteArray: ...
    @staticmethod
    def fromBase64(
        base64: Union[QByteArray, bytes], options: QByteArray.Base64Options = ...
    ) -> QByteArray: ...
    @staticmethod
    def fromBase64Encoding(
        base64: Union[QByteArray, bytes], options: QByteArray.Base64Options = ...
    ) -> QByteArray.FromBase64Result: ...
    @staticmethod
    def fromHex(hexEncoded: Union[QByteArray, bytes]) -> QByteArray: ...
    @staticmethod
    def fromPercentEncoding(
        pctEncoded: Union[QByteArray, bytes], percent: int = ...
    ) -> QByteArray: ...
    @staticmethod
    def fromRawData(data: bytes, size: int) -> QByteArray: ...
    def front(self) -> int: ...
    @overload
    def indexOf(self, bv: Union[QByteArray, bytes], from_: int = ...) -> int: ...
    @overload
    def indexOf(self, c: int, from_: int = ...) -> int: ...
    @overload
    def insert(self, i: int, c: int) -> QByteArray: ...
    @overload
    def insert(self, i: int, count: int, c: int) -> QByteArray: ...
    @overload
    def insert(self, i: int, data: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def insert(self, i: int, s: bytes) -> QByteArray: ...
    @overload
    def insert(self, i: int, s: bytes, len: int) -> QByteArray: ...
    def isEmpty(self) -> bool: ...
    def isLower(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isSharedWith(self, other: Union[QByteArray, bytes]) -> bool: ...
    def isUpper(self) -> bool: ...
    def last(self, n: int) -> QByteArray: ...
    @overload
    def lastIndexOf(self, bv: Union[QByteArray, bytes]) -> int: ...
    @overload
    def lastIndexOf(self, bv: Union[QByteArray, bytes], from_: int) -> int: ...
    @overload
    def lastIndexOf(self, c: int, from_: int = ...) -> int: ...
    def left(self, len: int) -> QByteArray: ...
    def leftJustified(self, width: int, fill: int = ..., truncate: bool = ...) -> QByteArray: ...
    def length(self) -> int: ...
    def mid(self, index: int, len: int = ...) -> QByteArray: ...
    @overload
    @staticmethod
    def number(arg__1: float, format: int = ..., precision: int = ...) -> QByteArray: ...
    @overload
    @staticmethod
    def number(arg__1: int, base: int = ...) -> QByteArray: ...
    @overload
    @staticmethod
    def number(arg__1: int, base: int = ...) -> QByteArray: ...
    @overload
    def prepend(self, a: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def prepend(self, c: int) -> QByteArray: ...
    @overload
    def prepend(self, count: int, c: int) -> QByteArray: ...
    @overload
    def prepend(self, s: bytes, len: int) -> QByteArray: ...
    def push_back(self, a: Union[QByteArray, bytes]) -> None: ...
    def push_front(self, a: Union[QByteArray, bytes]) -> None: ...
    def remove(self, index: int, len: int) -> QByteArray: ...
    def repeated(self, times: int) -> QByteArray: ...
    @overload
    def replace(self, before: bytes, bsize: int, after: bytes, asize: int) -> QByteArray: ...
    @overload
    def replace(self, before: int, after: int) -> QByteArray: ...
    @overload
    def replace(self, before: int, after: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    def replace(
        self, before: Union[QByteArray, bytes], after: Union[QByteArray, bytes]
    ) -> QByteArray: ...
    @overload
    def replace(self, index: int, len: int, s: bytes, alen: int) -> QByteArray: ...
    @overload
    def replace(self, index: int, len: int, s: Union[QByteArray, bytes]) -> QByteArray: ...
    def reserve(self, size: int) -> None: ...
    def resize(self, size: int) -> None: ...
    def right(self, len: int) -> QByteArray: ...
    def rightJustified(self, width: int, fill: int = ..., truncate: bool = ...) -> QByteArray: ...
    @overload
    def setNum(self, arg__1: float, format: int = ..., precision: int = ...) -> QByteArray: ...
    @overload
    def setNum(self, arg__1: int, base: int = ...) -> QByteArray: ...
    @overload
    def setNum(self, arg__1: int, base: int = ...) -> QByteArray: ...
    def setRawData(self, a: bytes, n: int) -> QByteArray: ...
    def shrink_to_fit(self) -> None: ...
    def simplified(self) -> QByteArray: ...
    def size(self) -> int: ...
    @overload
    def sliced(self, pos: int) -> QByteArray: ...
    @overload
    def sliced(self, pos: int, n: int) -> QByteArray: ...
    def split(self, sep: int) -> List[QByteArray]: ...
    def squeeze(self) -> None: ...
    @overload
    def startsWith(self, bv: Union[QByteArray, bytes]) -> bool: ...
    @overload
    def startsWith(self, c: int) -> bool: ...
    def swap(self, other: Union[QByteArray, bytes]) -> None: ...
    def toBase64(self, options: QByteArray.Base64Options = ...) -> QByteArray: ...
    def toDouble(self) -> Tuple[float, bool]: ...
    def toFloat(self) -> Tuple[float, bool]: ...
    def toHex(self, separator: int = ...) -> QByteArray: ...
    def toInt(self, base: int = ...) -> Tuple[int, bool]: ...
    def toLong(self, base: int = ...) -> Tuple[int, bool]: ...
    def toLongLong(self, base: int = ...) -> Tuple[int, bool]: ...
    def toLower(self) -> QByteArray: ...
    def toPercentEncoding(
        self,
        exclude: Union[QByteArray, bytes] = ...,
        include: Union[QByteArray, bytes] = ...,
        percent: int = ...,
    ) -> QByteArray: ...
    def toShort(self, base: int = ...) -> Tuple[int, bool]: ...
    def toUInt(self, base: int = ...) -> Tuple[int, bool]: ...
    def toULong(self, base: int = ...) -> Tuple[int, bool]: ...
    def toULongLong(self, base: int = ...) -> Tuple[int, bool]: ...
    def toUShort(self, base: int = ...) -> Tuple[int, bool]: ...
    def toUpper(self) -> QByteArray: ...
    def trimmed(self) -> QByteArray: ...
    def truncate(self, pos: int) -> None: ...

class QByteArrayMatcher(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QByteArrayMatcher) -> None: ...
    @overload
    def __init__(self, pattern: bytes, length: int) -> None: ...
    @overload
    def __init__(self, pattern: Union[QByteArray, bytes]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @overload
    def indexIn(self, ba: Union[QByteArray, bytes], from_: int = ...) -> int: ...
    @overload
    def indexIn(self, str: bytes, len: int, from_: int = ...) -> int: ...
    def pattern(self) -> QByteArray: ...
    def setPattern(self, pattern: Union[QByteArray, bytes]) -> None: ...

class QCalendar(Shiboken.Object):
    class System(Enum):

        User: QCalendar.System = ...  # -0x1
        Gregorian: QCalendar.System = ...  # 0x0
        Julian: QCalendar.System = ...  # 0x8
        Milankovic: QCalendar.System = ...  # 0x9
        Jalali: QCalendar.System = ...  # 0xa
        IslamicCivil: QCalendar.System = ...  # 0xb
        Last: QCalendar.System = ...  # 0xb
    class SystemId(Shiboken.Object):
        def __init__(self) -> None: ...
        def index(self) -> int: ...
        def isValid(self) -> bool: ...
    class YearMonthDay(Shiboken.Object):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, YearMonthDay: Union[QCalendar.YearMonthDay, int]) -> None: ...
        @overload
        def __init__(self, y: int, m: int = ..., d: int = ...) -> None: ...
        @staticmethod
        def __copy__() -> None: ...
        def isValid(self) -> bool: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, id: QCalendar.SystemId) -> None: ...
    @overload
    def __init__(self, name: str) -> None: ...
    @overload
    def __init__(self, system: QCalendar.System) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def availableCalendars() -> List[str]: ...
    @overload
    def dateFromParts(self, parts: Union[QCalendar.YearMonthDay, int]) -> QDate: ...
    @overload
    def dateFromParts(self, year: int, month: int, day: int) -> QDate: ...
    def dateTimeToString(
        self,
        format: str,
        datetime: QDateTime,
        dateOnly: QDate,
        timeOnly: QTime,
        locale: Union[QLocale, QLocale.Language],
    ) -> str: ...
    def dayOfWeek(self, date: QDate) -> int: ...
    def daysInMonth(self, month: int, year: int = ...) -> int: ...
    def daysInYear(self, year: int) -> int: ...
    def hasYearZero(self) -> bool: ...
    def isDateValid(self, year: int, month: int, day: int) -> bool: ...
    def isGregorian(self) -> bool: ...
    def isLeapYear(self, year: int) -> bool: ...
    def isLunar(self) -> bool: ...
    def isLuniSolar(self) -> bool: ...
    def isProleptic(self) -> bool: ...
    def isSolar(self) -> bool: ...
    def isValid(self) -> bool: ...
    def maximumDaysInMonth(self) -> int: ...
    def maximumMonthsInYear(self) -> int: ...
    def minimumDaysInMonth(self) -> int: ...
    def monthName(
        self,
        locale: Union[QLocale, QLocale.Language],
        month: int,
        year: int = ...,
        format: QLocale.FormatType = ...,
    ) -> str: ...
    def monthsInYear(self, year: int) -> int: ...
    def name(self) -> str: ...
    def partsFromDate(self, date: QDate) -> QCalendar.YearMonthDay: ...
    def standaloneMonthName(
        self,
        locale: Union[QLocale, QLocale.Language],
        month: int,
        year: int = ...,
        format: QLocale.FormatType = ...,
    ) -> str: ...
    def standaloneWeekDayName(
        self, locale: Union[QLocale, QLocale.Language], day: int, format: QLocale.FormatType = ...
    ) -> str: ...
    def weekDayName(
        self, locale: Union[QLocale, QLocale.Language], day: int, format: QLocale.FormatType = ...
    ) -> str: ...

class QCborArray(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QCborArray) -> None: ...
    def __add__(
        self,
        v: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QCborArray: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(
        self,
        v: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QCborArray: ...
    def __lshift__(
        self,
        v: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QCborArray: ...
    def append(
        self,
        value: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def at(self, i: int) -> QCborValue: ...
    def clear(self) -> None: ...
    def compare(self, other: QCborArray) -> int: ...
    def contains(
        self,
        value: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> bool: ...
    def empty(self) -> bool: ...
    def first(self) -> QCborValue: ...
    @staticmethod
    def fromJsonArray(array: QJsonArray) -> QCborArray: ...
    @staticmethod
    def fromStringList(list: Sequence[str]) -> QCborArray: ...
    @staticmethod
    def fromVariantList(list: Sequence[Any]) -> QCborArray: ...
    def insert(
        self,
        i: int,
        value: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def isEmpty(self) -> bool: ...
    def last(self) -> QCborValue: ...
    def pop_back(self) -> None: ...
    def pop_front(self) -> None: ...
    def prepend(
        self,
        value: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def push_back(
        self,
        t: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def push_front(
        self,
        t: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def removeAt(self, i: int) -> None: ...
    def removeFirst(self) -> None: ...
    def removeLast(self) -> None: ...
    def size(self) -> int: ...
    def swap(self, other: QCborArray) -> None: ...
    def takeAt(self, i: int) -> QCborValue: ...
    def takeFirst(self) -> QCborValue: ...
    def takeLast(self) -> QCborValue: ...
    def toCborValue(self) -> QCborValue: ...
    def toJsonArray(self) -> QJsonArray: ...
    def toVariantList(self) -> List[Any]: ...

class QCborError(Shiboken.Object):

    NoError: QCborError.Code = ...  # 0x0
    UnknownError: QCborError.Code = ...  # 0x1
    AdvancePastEnd: QCborError.Code = ...  # 0x3
    InputOutputError: QCborError.Code = ...  # 0x4
    GarbageAtEnd: QCborError.Code = ...  # 0x100
    EndOfFile: QCborError.Code = ...  # 0x101
    UnexpectedBreak: QCborError.Code = ...  # 0x102
    UnknownType: QCborError.Code = ...  # 0x103
    IllegalType: QCborError.Code = ...  # 0x104
    IllegalNumber: QCborError.Code = ...  # 0x105
    IllegalSimpleType: QCborError.Code = ...  # 0x106
    InvalidUtf8String: QCborError.Code = ...  # 0x204
    DataTooLarge: QCborError.Code = ...  # 0x400
    NestingTooDeep: QCborError.Code = ...  # 0x401
    UnsupportedType: QCborError.Code = ...  # 0x402
    class Code(Enum):

        NoError: QCborError.Code = ...  # 0x0
        UnknownError: QCborError.Code = ...  # 0x1
        AdvancePastEnd: QCborError.Code = ...  # 0x3
        InputOutputError: QCborError.Code = ...  # 0x4
        GarbageAtEnd: QCborError.Code = ...  # 0x100
        EndOfFile: QCborError.Code = ...  # 0x101
        UnexpectedBreak: QCborError.Code = ...  # 0x102
        UnknownType: QCborError.Code = ...  # 0x103
        IllegalType: QCborError.Code = ...  # 0x104
        IllegalNumber: QCborError.Code = ...  # 0x105
        IllegalSimpleType: QCborError.Code = ...  # 0x106
        InvalidUtf8String: QCborError.Code = ...  # 0x204
        DataTooLarge: QCborError.Code = ...  # 0x400
        NestingTooDeep: QCborError.Code = ...  # 0x401
        UnsupportedType: QCborError.Code = ...  # 0x402
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QCborError: QCborError) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def toString(self) -> str: ...

class QCborKnownTags(Enum):

    DateTimeString: QCborKnownTags = ...  # 0x0
    UnixTime_t: QCborKnownTags = ...  # 0x1
    PositiveBignum: QCborKnownTags = ...  # 0x2
    NegativeBignum: QCborKnownTags = ...  # 0x3
    Decimal: QCborKnownTags = ...  # 0x4
    Bigfloat: QCborKnownTags = ...  # 0x5
    COSE_Encrypt0: QCborKnownTags = ...  # 0x10
    COSE_Mac0: QCborKnownTags = ...  # 0x11
    COSE_Sign1: QCborKnownTags = ...  # 0x12
    ExpectedBase64url: QCborKnownTags = ...  # 0x15
    ExpectedBase64: QCborKnownTags = ...  # 0x16
    ExpectedBase16: QCborKnownTags = ...  # 0x17
    EncodedCbor: QCborKnownTags = ...  # 0x18
    Url: QCborKnownTags = ...  # 0x20
    Base64url: QCborKnownTags = ...  # 0x21
    Base64: QCborKnownTags = ...  # 0x22
    RegularExpression: QCborKnownTags = ...  # 0x23
    MimeMessage: QCborKnownTags = ...  # 0x24
    Uuid: QCborKnownTags = ...  # 0x25
    COSE_Encrypt: QCborKnownTags = ...  # 0x60
    COSE_Mac: QCborKnownTags = ...  # 0x61
    COSE_Sign: QCborKnownTags = ...  # 0x62
    Signature: QCborKnownTags = ...  # 0xd9f7

class QCborMap(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QCborMap) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def clear(self) -> None: ...
    def compare(self, other: QCborMap) -> int: ...
    @overload
    def contains(self, key: str) -> bool: ...
    @overload
    def contains(self, key: int) -> bool: ...
    @overload
    def contains(
        self,
        key: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> bool: ...
    def empty(self) -> bool: ...
    @staticmethod
    def fromJsonObject(o: Dict[str, QJsonValue]) -> QCborMap: ...
    @staticmethod
    def fromVariantHash(hash: Dict[str, Any]) -> QCborMap: ...
    @staticmethod
    def fromVariantMap(map: Dict[str, Any]) -> QCborMap: ...
    def isEmpty(self) -> bool: ...
    def keys(self) -> List[QCborValue]: ...
    @overload
    def remove(self, key: str) -> None: ...
    @overload
    def remove(self, key: int) -> None: ...
    @overload
    def remove(
        self,
        key: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def size(self) -> int: ...
    def swap(self, other: QCborMap) -> None: ...
    @overload
    def take(self, key: str) -> QCborValue: ...
    @overload
    def take(self, key: int) -> QCborValue: ...
    @overload
    def take(
        self,
        key: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QCborValue: ...
    def toCborValue(self) -> QCborValue: ...
    def toJsonObject(self) -> Dict[str, QJsonValue]: ...
    def toVariantHash(self) -> Dict[str, Any]: ...
    def toVariantMap(self) -> Dict[str, Any]: ...
    @overload
    def value(self, key: str) -> QCborValue: ...
    @overload
    def value(self, key: int) -> QCborValue: ...
    @overload
    def value(
        self,
        key: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QCborValue: ...

class QCborParserError(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QCborParserError: QCborParserError) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def errorString(self) -> str: ...

class QCborSimpleType(Enum):

    False_: QCborSimpleType = ...  # 0x14
    True_: QCborSimpleType = ...  # 0x15
    Null: QCborSimpleType = ...  # 0x16
    Undefined: QCborSimpleType = ...  # 0x17

class QCborStreamReader(Shiboken.Object):

    Error: QCborStreamReader.StringResultCode = ...  # -0x1
    EndOfString: QCborStreamReader.StringResultCode = ...  # 0x0
    Ok: QCborStreamReader.StringResultCode = ...  # 0x1
    UnsignedInteger: QCborStreamReader.Type = ...  # 0x0
    NegativeInteger: QCborStreamReader.Type = ...  # 0x20
    ByteArray: QCborStreamReader.Type = ...  # 0x40
    ByteString: QCborStreamReader.Type = ...  # 0x40
    String: QCborStreamReader.Type = ...  # 0x60
    TextString: QCborStreamReader.Type = ...  # 0x60
    Array: QCborStreamReader.Type = ...  # 0x80
    Map: QCborStreamReader.Type = ...  # 0xa0
    Tag: QCborStreamReader.Type = ...  # 0xc0
    SimpleType: QCborStreamReader.Type = ...  # 0xe0
    Float16: QCborStreamReader.Type = ...  # 0xf9
    HalfFloat: QCborStreamReader.Type = ...  # 0xf9
    Float: QCborStreamReader.Type = ...  # 0xfa
    Double: QCborStreamReader.Type = ...  # 0xfb
    Invalid: QCborStreamReader.Type = ...  # 0xff
    class StringResultCode(Enum):

        Error: QCborStreamReader.StringResultCode = ...  # -0x1
        EndOfString: QCborStreamReader.StringResultCode = ...  # 0x0
        Ok: QCborStreamReader.StringResultCode = ...  # 0x1
    class Type(Enum):

        UnsignedInteger: QCborStreamReader.Type = ...  # 0x0
        NegativeInteger: QCborStreamReader.Type = ...  # 0x20
        ByteArray: QCborStreamReader.Type = ...  # 0x40
        ByteString: QCborStreamReader.Type = ...  # 0x40
        String: QCborStreamReader.Type = ...  # 0x60
        TextString: QCborStreamReader.Type = ...  # 0x60
        Array: QCborStreamReader.Type = ...  # 0x80
        Map: QCborStreamReader.Type = ...  # 0xa0
        Tag: QCborStreamReader.Type = ...  # 0xc0
        SimpleType: QCborStreamReader.Type = ...  # 0xe0
        Float16: QCborStreamReader.Type = ...  # 0xf9
        HalfFloat: QCborStreamReader.Type = ...  # 0xf9
        Float: QCborStreamReader.Type = ...  # 0xfa
        Double: QCborStreamReader.Type = ...  # 0xfb
        Invalid: QCborStreamReader.Type = ...  # 0xff
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, data: bytes, len: int) -> None: ...
    @overload
    def __init__(self, data: bytearray, len: int) -> None: ...
    @overload
    def __init__(self, data: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, device: QIODevice) -> None: ...
    @overload
    def addData(self, data: bytes, len: int) -> None: ...
    @overload
    def addData(self, data: bytearray, len: int) -> None: ...
    @overload
    def addData(self, data: Union[QByteArray, bytes]) -> None: ...
    def clear(self) -> None: ...
    def containerDepth(self) -> int: ...
    def currentOffset(self) -> int: ...
    def currentStringChunkSize(self) -> int: ...
    def device(self) -> QIODevice: ...
    def enterContainer(self) -> bool: ...
    def hasNext(self) -> bool: ...
    def isArray(self) -> bool: ...
    def isBool(self) -> bool: ...
    def isByteArray(self) -> bool: ...
    def isContainer(self) -> bool: ...
    def isDouble(self) -> bool: ...
    def isFalse(self) -> bool: ...
    def isFloat(self) -> bool: ...
    def isFloat16(self) -> bool: ...
    def isInteger(self) -> bool: ...
    def isInvalid(self) -> bool: ...
    def isLengthKnown(self) -> bool: ...
    def isMap(self) -> bool: ...
    def isNegativeInteger(self) -> bool: ...
    def isNull(self) -> bool: ...
    @overload
    def isSimpleType(self) -> bool: ...
    @overload
    def isSimpleType(self, st: QCborSimpleType) -> bool: ...
    def isString(self) -> bool: ...
    def isTag(self) -> bool: ...
    def isTrue(self) -> bool: ...
    def isUndefined(self) -> bool: ...
    def isUnsignedInteger(self) -> bool: ...
    def isValid(self) -> bool: ...
    def lastError(self) -> QCborError: ...
    def leaveContainer(self) -> bool: ...
    def length(self) -> int: ...
    def next(self, maxRecursion: int = ...) -> bool: ...
    def parentContainerType(self) -> QCborStreamReader.Type: ...
    def readByteArray(self) -> QCborStringResultByteArray: ...
    def readString(self) -> QCborStringResultString: ...
    def reparse(self) -> None: ...
    def reset(self) -> None: ...
    def setDevice(self, device: QIODevice) -> None: ...
    def toBool(self) -> bool: ...
    def toDouble(self) -> float: ...
    def toFloat(self) -> float: ...
    def toInteger(self) -> int: ...
    def toSimpleType(self) -> QCborSimpleType: ...
    def toTag(self) -> QCborTag: ...
    def toUnsignedInteger(self) -> int: ...
    def type(self) -> QCborStreamReader.Type: ...

class QCborStreamWriter(Shiboken.Object):
    @overload
    def __init__(self, data: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, device: QIODevice) -> None: ...
    @overload
    def append(self, b: bool) -> None: ...
    @overload
    def append(self, ba: Union[QByteArray, bytes]) -> None: ...
    @overload
    def append(self, d: float) -> None: ...
    @overload
    def append(self, f: float) -> None: ...
    @overload
    def append(self, i: int) -> None: ...
    @overload
    def append(self, i: int) -> None: ...
    @overload
    def append(self, st: QCborSimpleType) -> None: ...
    @overload
    def append(self, str: str) -> None: ...
    @overload
    def append(self, str: bytes, size: int = ...) -> None: ...
    @overload
    def append(self, tag: QCborKnownTags) -> None: ...
    @overload
    def append(self, tag: QCborTag) -> None: ...
    @overload
    def append(self, u: int) -> None: ...
    @overload
    def append(self, u: int) -> None: ...
    def appendByteString(self, data: bytes, len: int) -> None: ...
    def appendNull(self) -> None: ...
    def appendTextString(self, utf8: bytes, len: int) -> None: ...
    def appendUndefined(self) -> None: ...
    def device(self) -> QIODevice: ...
    def endArray(self) -> bool: ...
    def endMap(self) -> bool: ...
    def setDevice(self, device: QIODevice) -> None: ...
    @overload
    def startArray(self) -> None: ...
    @overload
    def startArray(self, count: int) -> None: ...
    @overload
    def startMap(self) -> None: ...
    @overload
    def startMap(self, count: int) -> None: ...

class QCborStringResultByteArray(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QCborStringResultByteArray: QCborStringResultByteArray) -> None: ...
    @staticmethod
    def __copy__() -> None: ...

class QCborStringResultString(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QCborStringResultString: QCborStringResultString) -> None: ...
    @staticmethod
    def __copy__() -> None: ...

class QCborTag(Enum): ...

class QCborValue(Shiboken.Object):

    Compact: QCborValue.DiagnosticNotationOption = ...  # 0x0
    LineWrapped: QCborValue.DiagnosticNotationOption = ...  # 0x1
    ExtendedFormat: QCborValue.DiagnosticNotationOption = ...  # 0x2
    NoTransformation: QCborValue.EncodingOption = ...  # 0x0
    SortKeysInMaps: QCborValue.EncodingOption = ...  # 0x1
    UseFloat: QCborValue.EncodingOption = ...  # 0x2
    UseFloat16: QCborValue.EncodingOption = ...  # 0x6
    UseIntegers: QCborValue.EncodingOption = ...  # 0x8
    Invalid: QCborValue.Type = ...  # -0x1
    Integer: QCborValue.Type = ...  # 0x0
    ByteArray: QCborValue.Type = ...  # 0x40
    String: QCborValue.Type = ...  # 0x60
    Array: QCborValue.Type = ...  # 0x80
    Map: QCborValue.Type = ...  # 0xa0
    Tag: QCborValue.Type = ...  # 0xc0
    SimpleType: QCborValue.Type = ...  # 0x100
    False_: QCborValue.Type = ...  # 0x114
    True_: QCborValue.Type = ...  # 0x115
    Null: QCborValue.Type = ...  # 0x116
    Undefined: QCborValue.Type = ...  # 0x117
    Double: QCborValue.Type = ...  # 0x202
    DateTime: QCborValue.Type = ...  # 0x10000
    Url: QCborValue.Type = ...  # 0x10020
    RegularExpression: QCborValue.Type = ...  # 0x10023
    Uuid: QCborValue.Type = ...  # 0x10025
    class DiagnosticNotationOption(Enum):

        Compact: QCborValue.DiagnosticNotationOption = ...  # 0x0
        LineWrapped: QCborValue.DiagnosticNotationOption = ...  # 0x1
        ExtendedFormat: QCborValue.DiagnosticNotationOption = ...  # 0x2
    class DiagnosticNotationOptions(object): ...
    class EncodingOption(Enum):

        NoTransformation: QCborValue.EncodingOption = ...  # 0x0
        SortKeysInMaps: QCborValue.EncodingOption = ...  # 0x1
        UseFloat: QCborValue.EncodingOption = ...  # 0x2
        UseFloat16: QCborValue.EncodingOption = ...  # 0x6
        UseIntegers: QCborValue.EncodingOption = ...  # 0x8
    class EncodingOptions(object): ...
    class Type(Enum):

        Invalid: QCborValue.Type = ...  # -0x1
        Integer: QCborValue.Type = ...  # 0x0
        ByteArray: QCborValue.Type = ...  # 0x40
        String: QCborValue.Type = ...  # 0x60
        Array: QCborValue.Type = ...  # 0x80
        Map: QCborValue.Type = ...  # 0xa0
        Tag: QCborValue.Type = ...  # 0xc0
        SimpleType: QCborValue.Type = ...  # 0x100
        False_: QCborValue.Type = ...  # 0x114
        True_: QCborValue.Type = ...  # 0x115
        Null: QCborValue.Type = ...  # 0x116
        Undefined: QCborValue.Type = ...  # 0x117
        Double: QCborValue.Type = ...  # 0x202
        DateTime: QCborValue.Type = ...  # 0x10000
        Url: QCborValue.Type = ...  # 0x10020
        RegularExpression: QCborValue.Type = ...  # 0x10023
        Uuid: QCborValue.Type = ...  # 0x10025
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, a: QCborArray) -> None: ...
    @overload
    def __init__(self, b_: bool) -> None: ...
    @overload
    def __init__(self, ba: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, dt: QDateTime) -> None: ...
    @overload
    def __init__(self, i: int) -> None: ...
    @overload
    def __init__(self, i: int) -> None: ...
    @overload
    def __init__(self, m: QCborMap) -> None: ...
    @overload
    def __init__(
        self,
        other: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    @overload
    def __init__(self, rx: Union[QRegularExpression, str]) -> None: ...
    @overload
    def __init__(self, s: str) -> None: ...
    @overload
    def __init__(self, s: bytes) -> None: ...
    @overload
    def __init__(self, st: QCborSimpleType) -> None: ...
    @overload
    def __init__(
        self,
        t_: QCborKnownTags,
        tv: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ] = ...,
    ) -> None: ...
    @overload
    def __init__(self, t_: QCborValue.Type) -> None: ...
    @overload
    def __init__(
        self,
        tag: QCborTag,
        taggedValue: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ] = ...,
    ) -> None: ...
    @overload
    def __init__(self, u: int) -> None: ...
    @overload
    def __init__(self, url: Union[QUrl, str]) -> None: ...
    @overload
    def __init__(self, uuid: QUuid) -> None: ...
    @overload
    def __init__(self, v: float) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def compare(
        self,
        other: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> int: ...
    @overload
    @staticmethod
    def fromCbor(
        ba: Union[QByteArray, bytes], error: Optional[QCborParserError] = ...
    ) -> QCborValue: ...
    @overload
    @staticmethod
    def fromCbor(data: bytes, len: int, error: Optional[QCborParserError] = ...) -> QCborValue: ...
    @overload
    @staticmethod
    def fromCbor(
        data: bytearray, len: int, error: Optional[QCborParserError] = ...
    ) -> QCborValue: ...
    @overload
    @staticmethod
    def fromCbor(reader: QCborStreamReader) -> QCborValue: ...
    @staticmethod
    def fromJsonValue(
        v: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ]
    ) -> QCborValue: ...
    @staticmethod
    def fromVariant(variant: Any) -> QCborValue: ...
    def isArray(self) -> bool: ...
    def isBool(self) -> bool: ...
    def isByteArray(self) -> bool: ...
    def isContainer(self) -> bool: ...
    def isDateTime(self) -> bool: ...
    def isDouble(self) -> bool: ...
    def isFalse(self) -> bool: ...
    def isInteger(self) -> bool: ...
    def isInvalid(self) -> bool: ...
    def isMap(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isRegularExpression(self) -> bool: ...
    @overload
    def isSimpleType(self) -> bool: ...
    @overload
    def isSimpleType(self, st: QCborSimpleType) -> bool: ...
    def isString(self) -> bool: ...
    def isTag(self) -> bool: ...
    def isTrue(self) -> bool: ...
    def isUndefined(self) -> bool: ...
    def isUrl(self) -> bool: ...
    def isUuid(self) -> bool: ...
    def swap(
        self,
        other: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> None: ...
    def tag(self, defaultValue: QCborTag = ...) -> QCborTag: ...
    def taggedValue(
        self,
        defaultValue: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ] = ...,
    ) -> QCborValue: ...
    @overload
    def toArray(self) -> QCborArray: ...
    @overload
    def toArray(self, defaultValue: QCborArray) -> QCborArray: ...
    def toBool(self, defaultValue: bool = ...) -> bool: ...
    def toByteArray(self, defaultValue: Union[QByteArray, bytes] = ...) -> QByteArray: ...
    @overload
    def toCbor(self, opt: QCborValue.EncodingOptions = ...) -> QByteArray: ...
    @overload
    def toCbor(self, writer: QCborStreamWriter, opt: QCborValue.EncodingOptions = ...) -> None: ...
    def toDateTime(self, defaultValue: QDateTime = ...) -> QDateTime: ...
    def toDiagnosticNotation(self, opts: QCborValue.DiagnosticNotationOptions = ...) -> str: ...
    def toDouble(self, defaultValue: float = ...) -> float: ...
    def toInteger(self, defaultValue: int = ...) -> int: ...
    def toJsonValue(self) -> QJsonValue: ...
    @overload
    def toMap(self) -> QCborMap: ...
    @overload
    def toMap(self, defaultValue: QCborMap) -> QCborMap: ...
    def toRegularExpression(
        self, defaultValue: Union[QRegularExpression, str] = ...
    ) -> QRegularExpression: ...
    def toSimpleType(self, defaultValue: QCborSimpleType = ...) -> QCborSimpleType: ...
    def toString(self, defaultValue: str = ...) -> str: ...
    def toUrl(self, defaultValue: Union[QUrl, str] = ...) -> QUrl: ...
    def toUuid(self, defaultValue: QUuid = ...) -> QUuid: ...
    def toVariant(self) -> Any: ...
    def type(self) -> QCborValue.Type: ...

class QChildEvent(QEvent):
    @overload
    def __init__(self, arg__1: QChildEvent) -> None: ...
    @overload
    def __init__(self, type: QEvent.Type, child: QObject) -> None: ...
    def added(self) -> bool: ...
    def child(self) -> QObject: ...
    def clone(self) -> QChildEvent: ...
    def polished(self) -> bool: ...
    def removed(self) -> bool: ...

class QCollator(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg__1: QCollator) -> None: ...
    @overload
    def __init__(self, locale: Union[QLocale, QLocale.Language]) -> None: ...
    def __call__(self, s1: str, s2: str) -> bool: ...
    def caseSensitivity(self) -> Qt.CaseSensitivity: ...
    @overload
    def compare(self, s1: bytes, len1: int, s2: bytes, len2: int) -> int: ...
    @overload
    def compare(self, s1: str, s2: str) -> int: ...
    def ignorePunctuation(self) -> bool: ...
    def locale(self) -> QLocale: ...
    def numericMode(self) -> bool: ...
    def setCaseSensitivity(self, cs: Qt.CaseSensitivity) -> None: ...
    def setIgnorePunctuation(self, on: bool) -> None: ...
    def setLocale(self, locale: Union[QLocale, QLocale.Language]) -> None: ...
    def setNumericMode(self, on: bool) -> None: ...
    def sortKey(self, string: str) -> QCollatorSortKey: ...
    def swap(self, other: QCollator) -> None: ...

class QCollatorSortKey(Shiboken.Object):
    def __init__(self, other: QCollatorSortKey) -> None: ...
    def compare(self, key: QCollatorSortKey) -> int: ...
    def swap(self, other: QCollatorSortKey) -> None: ...

class QCommandLineOption(Shiboken.Object):

    HiddenFromHelp: QCommandLineOption.Flag = ...  # 0x1
    ShortOptionStyle: QCommandLineOption.Flag = ...  # 0x2
    class Flag(Enum):

        HiddenFromHelp: QCommandLineOption.Flag = ...  # 0x1
        ShortOptionStyle: QCommandLineOption.Flag = ...  # 0x2
    class Flags(object): ...
    @overload
    def __init__(self, name: str) -> None: ...
    @overload
    def __init__(
        self, name: str, description: str, valueName: str = ..., defaultValue: str = ...
    ) -> None: ...
    @overload
    def __init__(self, names: Sequence[str]) -> None: ...
    @overload
    def __init__(
        self, names: Sequence[str], description: str, valueName: str = ..., defaultValue: str = ...
    ) -> None: ...
    @overload
    def __init__(self, other: QCommandLineOption) -> None: ...
    def defaultValues(self) -> List[str]: ...
    def description(self) -> str: ...
    def flags(self) -> QCommandLineOption.Flags: ...
    def names(self) -> List[str]: ...
    def setDefaultValue(self, defaultValue: str) -> None: ...
    def setDefaultValues(self, defaultValues: Sequence[str]) -> None: ...
    def setDescription(self, description: str) -> None: ...
    def setFlags(self, aflags: QCommandLineOption.Flags) -> None: ...
    def setValueName(self, name: str) -> None: ...
    def swap(self, other: QCommandLineOption) -> None: ...
    def valueName(self) -> str: ...

class QCommandLineParser(Shiboken.Object):

    ParseAsOptions: QCommandLineParser.OptionsAfterPositionalArgumentsMode = ...  # 0x0
    ParseAsPositionalArguments: QCommandLineParser.OptionsAfterPositionalArgumentsMode = ...  # 0x1
    ParseAsCompactedShortOptions: QCommandLineParser.SingleDashWordOptionMode = ...  # 0x0
    ParseAsLongOptions: QCommandLineParser.SingleDashWordOptionMode = ...  # 0x1
    class OptionsAfterPositionalArgumentsMode(Enum):

        ParseAsOptions: QCommandLineParser.OptionsAfterPositionalArgumentsMode = ...  # 0x0
        ParseAsPositionalArguments: QCommandLineParser.OptionsAfterPositionalArgumentsMode = (
            ...
        )  # 0x1
    class SingleDashWordOptionMode(Enum):

        ParseAsCompactedShortOptions: QCommandLineParser.SingleDashWordOptionMode = ...  # 0x0
        ParseAsLongOptions: QCommandLineParser.SingleDashWordOptionMode = ...  # 0x1
    def __init__(self) -> None: ...
    def addHelpOption(self) -> QCommandLineOption: ...
    def addOption(self, commandLineOption: QCommandLineOption) -> bool: ...
    def addOptions(self, options: Sequence[QCommandLineOption]) -> bool: ...
    def addPositionalArgument(self, name: str, description: str, syntax: str = ...) -> None: ...
    def addVersionOption(self) -> QCommandLineOption: ...
    def applicationDescription(self) -> str: ...
    def clearPositionalArguments(self) -> None: ...
    def errorText(self) -> str: ...
    def helpText(self) -> str: ...
    @overload
    def isSet(self, name: str) -> bool: ...
    @overload
    def isSet(self, option: QCommandLineOption) -> bool: ...
    def optionNames(self) -> List[str]: ...
    def parse(self, arguments: Sequence[str]) -> bool: ...
    def positionalArguments(self) -> List[str]: ...
    @overload
    def process(self, app: QCoreApplication) -> None: ...
    @overload
    def process(self, arguments: Sequence[str]) -> None: ...
    def setApplicationDescription(self, description: str) -> None: ...
    def setOptionsAfterPositionalArgumentsMode(
        self, mode: QCommandLineParser.OptionsAfterPositionalArgumentsMode
    ) -> None: ...
    def setSingleDashWordOptionMode(
        self, parsingMode: QCommandLineParser.SingleDashWordOptionMode
    ) -> None: ...
    def showHelp(self, exitCode: int = ...) -> None: ...
    def showVersion(self) -> None: ...
    def unknownOptionNames(self) -> List[str]: ...
    @overload
    def value(self, name: str) -> str: ...
    @overload
    def value(self, option: QCommandLineOption) -> str: ...
    @overload
    def values(self, name: str) -> List[str]: ...
    @overload
    def values(self, option: QCommandLineOption) -> List[str]: ...

class QConcatenateTablesProxyModel(QAbstractItemModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def addSourceModel(self, sourceModel: QAbstractItemModel) -> None: ...
    def canDropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    def itemData(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> Dict[int, Any]: ...
    def mapFromSource(
        self, sourceIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def mapToSource(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def mimeData(self, indexes: List[int]) -> QMimeData: ...
    def mimeTypes(self) -> List[str]: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def removeSourceModel(self, sourceModel: QAbstractItemModel) -> None: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setData(
        self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = ...
    ) -> bool: ...
    def setItemData(
        self, index: Union[QModelIndex, QPersistentModelIndex], roles: Dict[int, Any]
    ) -> bool: ...
    def sourceModels(self) -> List[QAbstractItemModel]: ...
    def span(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize: ...

class QCoreApplication(QObject):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg__1: Sequence[str]) -> None: ...
    @staticmethod
    def addLibraryPath(arg__1: str) -> None: ...
    @staticmethod
    def applicationDirPath() -> str: ...
    @staticmethod
    def applicationFilePath() -> str: ...
    @staticmethod
    def applicationName() -> str: ...
    @staticmethod
    def applicationPid() -> int: ...
    @staticmethod
    def applicationVersion() -> str: ...
    @staticmethod
    def arguments() -> List[str]: ...
    @staticmethod
    def closingDown() -> bool: ...
    def event(self, arg__1: QEvent) -> bool: ...
    @staticmethod
    def eventDispatcher() -> QAbstractEventDispatcher: ...
    @staticmethod
    def exec() -> int: ...
    def exec_(self) -> int: ...
    @staticmethod
    def exit(retcode: int = ...) -> None: ...
    def installNativeEventFilter(self, filterObj: QAbstractNativeEventFilter) -> None: ...
    @staticmethod
    def installTranslator(messageFile: QTranslator) -> bool: ...
    @staticmethod
    def instance() -> Optional[QCoreApplication | QtWidgets.QApplication]: ...
    @staticmethod
    def isQuitLockEnabled() -> bool: ...
    @staticmethod
    def isSetuidAllowed() -> bool: ...
    @staticmethod
    def libraryPaths() -> List[str]: ...
    def notify(self, arg__1: QObject, arg__2: QEvent) -> bool: ...
    @staticmethod
    def organizationDomain() -> str: ...
    @staticmethod
    def organizationName() -> str: ...
    @staticmethod
    def postEvent(receiver: QObject, event: QEvent, priority: int = ...) -> None: ...
    @overload
    @staticmethod
    def processEvents(flags: QEventLoop.ProcessEventsFlags, maxtime: int) -> None: ...
    @overload
    @staticmethod
    def processEvents(flags: QEventLoop.ProcessEventsFlags = ...) -> None: ...
    @staticmethod
    def quit() -> None: ...
    @staticmethod
    def removeLibraryPath(arg__1: str) -> None: ...
    def removeNativeEventFilter(self, filterObj: QAbstractNativeEventFilter) -> None: ...
    @staticmethod
    def removePostedEvents(receiver: QObject, eventType: int = ...) -> None: ...
    @staticmethod
    def removeTranslator(messageFile: QTranslator) -> bool: ...
    def resolveInterface(self, name: bytes, revision: int) -> int: ...
    @staticmethod
    def sendEvent(receiver: QObject, event: QEvent) -> bool: ...
    @staticmethod
    def sendPostedEvents(receiver: Optional[QObject] = ..., event_type: int = ...) -> None: ...
    @staticmethod
    def setApplicationName(application: str) -> None: ...
    @staticmethod
    def setApplicationVersion(version: str) -> None: ...
    @staticmethod
    def setAttribute(attribute: Qt.ApplicationAttribute, on: bool = ...) -> None: ...
    @staticmethod
    def setEventDispatcher(eventDispatcher: QAbstractEventDispatcher) -> None: ...
    @staticmethod
    def setLibraryPaths(arg__1: Sequence[str]) -> None: ...
    @staticmethod
    def setOrganizationDomain(orgDomain: str) -> None: ...
    @staticmethod
    def setOrganizationName(orgName: str) -> None: ...
    @staticmethod
    def setQuitLockEnabled(enabled: bool) -> None: ...
    @staticmethod
    def setSetuidAllowed(allow: bool) -> None: ...
    def shutdown(self) -> None: ...
    @staticmethod
    def startingUp() -> bool: ...
    @staticmethod
    def testAttribute(attribute: Qt.ApplicationAttribute) -> bool: ...
    @staticmethod
    def translate(
        context: str | bytes, key: str | bytes, disambiguation: Optional[bytes] = ..., n: int = ...
    ) -> str: ...

class QCryptographicHash(Shiboken.Object):

    Md4: QCryptographicHash.Algorithm = ...  # 0x0
    Md5: QCryptographicHash.Algorithm = ...  # 0x1
    Sha1: QCryptographicHash.Algorithm = ...  # 0x2
    Sha224: QCryptographicHash.Algorithm = ...  # 0x3
    Sha256: QCryptographicHash.Algorithm = ...  # 0x4
    Sha384: QCryptographicHash.Algorithm = ...  # 0x5
    Sha512: QCryptographicHash.Algorithm = ...  # 0x6
    Keccak_224: QCryptographicHash.Algorithm = ...  # 0x7
    Keccak_256: QCryptographicHash.Algorithm = ...  # 0x8
    Keccak_384: QCryptographicHash.Algorithm = ...  # 0x9
    Keccak_512: QCryptographicHash.Algorithm = ...  # 0xa
    RealSha3_224: QCryptographicHash.Algorithm = ...  # 0xb
    Sha3_224: QCryptographicHash.Algorithm = ...  # 0xb
    RealSha3_256: QCryptographicHash.Algorithm = ...  # 0xc
    Sha3_256: QCryptographicHash.Algorithm = ...  # 0xc
    RealSha3_384: QCryptographicHash.Algorithm = ...  # 0xd
    Sha3_384: QCryptographicHash.Algorithm = ...  # 0xd
    RealSha3_512: QCryptographicHash.Algorithm = ...  # 0xe
    Sha3_512: QCryptographicHash.Algorithm = ...  # 0xe
    Blake2b_160: QCryptographicHash.Algorithm = ...  # 0xf
    Blake2b_256: QCryptographicHash.Algorithm = ...  # 0x10
    Blake2b_384: QCryptographicHash.Algorithm = ...  # 0x11
    Blake2b_512: QCryptographicHash.Algorithm = ...  # 0x12
    Blake2s_128: QCryptographicHash.Algorithm = ...  # 0x13
    Blake2s_160: QCryptographicHash.Algorithm = ...  # 0x14
    Blake2s_224: QCryptographicHash.Algorithm = ...  # 0x15
    Blake2s_256: QCryptographicHash.Algorithm = ...  # 0x16
    class Algorithm(Enum):

        Md4: QCryptographicHash.Algorithm = ...  # 0x0
        Md5: QCryptographicHash.Algorithm = ...  # 0x1
        Sha1: QCryptographicHash.Algorithm = ...  # 0x2
        Sha224: QCryptographicHash.Algorithm = ...  # 0x3
        Sha256: QCryptographicHash.Algorithm = ...  # 0x4
        Sha384: QCryptographicHash.Algorithm = ...  # 0x5
        Sha512: QCryptographicHash.Algorithm = ...  # 0x6
        Keccak_224: QCryptographicHash.Algorithm = ...  # 0x7
        Keccak_256: QCryptographicHash.Algorithm = ...  # 0x8
        Keccak_384: QCryptographicHash.Algorithm = ...  # 0x9
        Keccak_512: QCryptographicHash.Algorithm = ...  # 0xa
        RealSha3_224: QCryptographicHash.Algorithm = ...  # 0xb
        Sha3_224: QCryptographicHash.Algorithm = ...  # 0xb
        RealSha3_256: QCryptographicHash.Algorithm = ...  # 0xc
        Sha3_256: QCryptographicHash.Algorithm = ...  # 0xc
        RealSha3_384: QCryptographicHash.Algorithm = ...  # 0xd
        Sha3_384: QCryptographicHash.Algorithm = ...  # 0xd
        RealSha3_512: QCryptographicHash.Algorithm = ...  # 0xe
        Sha3_512: QCryptographicHash.Algorithm = ...  # 0xe
        Blake2b_160: QCryptographicHash.Algorithm = ...  # 0xf
        Blake2b_256: QCryptographicHash.Algorithm = ...  # 0x10
        Blake2b_384: QCryptographicHash.Algorithm = ...  # 0x11
        Blake2b_512: QCryptographicHash.Algorithm = ...  # 0x12
        Blake2s_128: QCryptographicHash.Algorithm = ...  # 0x13
        Blake2s_160: QCryptographicHash.Algorithm = ...  # 0x14
        Blake2s_224: QCryptographicHash.Algorithm = ...  # 0x15
        Blake2s_256: QCryptographicHash.Algorithm = ...  # 0x16
    def __init__(self, method: QCryptographicHash.Algorithm) -> None: ...
    @overload
    def addData(self, data: bytes, length: int) -> None: ...
    @overload
    def addData(self, data: Union[QByteArray, bytes]) -> None: ...
    @overload
    def addData(self, device: QIODevice) -> bool: ...
    @staticmethod
    def hash(
        data: Union[QByteArray, bytes], method: QCryptographicHash.Algorithm
    ) -> QByteArray: ...
    @staticmethod
    def hashLength(method: QCryptographicHash.Algorithm) -> int: ...
    def reset(self) -> None: ...
    def result(self) -> QByteArray: ...

class QDataStream(QIODeviceBase):

    BigEndian: QDataStream.ByteOrder = ...  # 0x0
    LittleEndian: QDataStream.ByteOrder = ...  # 0x1
    SinglePrecision: QDataStream.FloatingPointPrecision = ...  # 0x0
    DoublePrecision: QDataStream.FloatingPointPrecision = ...  # 0x1
    Ok: QDataStream.Status = ...  # 0x0
    ReadPastEnd: QDataStream.Status = ...  # 0x1
    ReadCorruptData: QDataStream.Status = ...  # 0x2
    WriteFailed: QDataStream.Status = ...  # 0x3
    Qt_1_0: QDataStream.Version = ...  # 0x1
    Qt_2_0: QDataStream.Version = ...  # 0x2
    Qt_2_1: QDataStream.Version = ...  # 0x3
    Qt_3_0: QDataStream.Version = ...  # 0x4
    Qt_3_1: QDataStream.Version = ...  # 0x5
    Qt_3_3: QDataStream.Version = ...  # 0x6
    Qt_4_0: QDataStream.Version = ...  # 0x7
    Qt_4_1: QDataStream.Version = ...  # 0x7
    Qt_4_2: QDataStream.Version = ...  # 0x8
    Qt_4_3: QDataStream.Version = ...  # 0x9
    Qt_4_4: QDataStream.Version = ...  # 0xa
    Qt_4_5: QDataStream.Version = ...  # 0xb
    Qt_4_6: QDataStream.Version = ...  # 0xc
    Qt_4_7: QDataStream.Version = ...  # 0xc
    Qt_4_8: QDataStream.Version = ...  # 0xc
    Qt_4_9: QDataStream.Version = ...  # 0xc
    Qt_5_0: QDataStream.Version = ...  # 0xd
    Qt_5_1: QDataStream.Version = ...  # 0xe
    Qt_5_2: QDataStream.Version = ...  # 0xf
    Qt_5_3: QDataStream.Version = ...  # 0xf
    Qt_5_4: QDataStream.Version = ...  # 0x10
    Qt_5_5: QDataStream.Version = ...  # 0x10
    Qt_5_10: QDataStream.Version = ...  # 0x11
    Qt_5_11: QDataStream.Version = ...  # 0x11
    Qt_5_6: QDataStream.Version = ...  # 0x11
    Qt_5_7: QDataStream.Version = ...  # 0x11
    Qt_5_8: QDataStream.Version = ...  # 0x11
    Qt_5_9: QDataStream.Version = ...  # 0x11
    Qt_5_12: QDataStream.Version = ...  # 0x12
    Qt_5_13: QDataStream.Version = ...  # 0x13
    Qt_5_14: QDataStream.Version = ...  # 0x13
    Qt_5_15: QDataStream.Version = ...  # 0x13
    Qt_6_0: QDataStream.Version = ...  # 0x14
    Qt_6_1: QDataStream.Version = ...  # 0x14
    Qt_6_2: QDataStream.Version = ...  # 0x14
    Qt_DefaultCompiledVersion: QDataStream.Version = ...  # 0x14
    class ByteOrder(Enum):

        BigEndian: QDataStream.ByteOrder = ...  # 0x0
        LittleEndian: QDataStream.ByteOrder = ...  # 0x1
    class FloatingPointPrecision(Enum):

        SinglePrecision: QDataStream.FloatingPointPrecision = ...  # 0x0
        DoublePrecision: QDataStream.FloatingPointPrecision = ...  # 0x1
    class Status(Enum):

        Ok: QDataStream.Status = ...  # 0x0
        ReadPastEnd: QDataStream.Status = ...  # 0x1
        ReadCorruptData: QDataStream.Status = ...  # 0x2
        WriteFailed: QDataStream.Status = ...  # 0x3
    class Version(Enum):

        Qt_1_0: QDataStream.Version = ...  # 0x1
        Qt_2_0: QDataStream.Version = ...  # 0x2
        Qt_2_1: QDataStream.Version = ...  # 0x3
        Qt_3_0: QDataStream.Version = ...  # 0x4
        Qt_3_1: QDataStream.Version = ...  # 0x5
        Qt_3_3: QDataStream.Version = ...  # 0x6
        Qt_4_0: QDataStream.Version = ...  # 0x7
        Qt_4_1: QDataStream.Version = ...  # 0x7
        Qt_4_2: QDataStream.Version = ...  # 0x8
        Qt_4_3: QDataStream.Version = ...  # 0x9
        Qt_4_4: QDataStream.Version = ...  # 0xa
        Qt_4_5: QDataStream.Version = ...  # 0xb
        Qt_4_6: QDataStream.Version = ...  # 0xc
        Qt_4_7: QDataStream.Version = ...  # 0xc
        Qt_4_8: QDataStream.Version = ...  # 0xc
        Qt_4_9: QDataStream.Version = ...  # 0xc
        Qt_5_0: QDataStream.Version = ...  # 0xd
        Qt_5_1: QDataStream.Version = ...  # 0xe
        Qt_5_2: QDataStream.Version = ...  # 0xf
        Qt_5_3: QDataStream.Version = ...  # 0xf
        Qt_5_4: QDataStream.Version = ...  # 0x10
        Qt_5_5: QDataStream.Version = ...  # 0x10
        Qt_5_10: QDataStream.Version = ...  # 0x11
        Qt_5_11: QDataStream.Version = ...  # 0x11
        Qt_5_6: QDataStream.Version = ...  # 0x11
        Qt_5_7: QDataStream.Version = ...  # 0x11
        Qt_5_8: QDataStream.Version = ...  # 0x11
        Qt_5_9: QDataStream.Version = ...  # 0x11
        Qt_5_12: QDataStream.Version = ...  # 0x12
        Qt_5_13: QDataStream.Version = ...  # 0x13
        Qt_5_14: QDataStream.Version = ...  # 0x13
        Qt_5_15: QDataStream.Version = ...  # 0x13
        Qt_6_0: QDataStream.Version = ...  # 0x14
        Qt_6_1: QDataStream.Version = ...  # 0x14
        Qt_6_2: QDataStream.Version = ...  # 0x14
        Qt_DefaultCompiledVersion: QDataStream.Version = ...  # 0x14
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg__1: QIODevice) -> None: ...
    @overload
    def __init__(self, arg__1: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, arg__1: Union[QByteArray, bytes], flags: QIODeviceBase.OpenMode) -> None: ...
    @overload
    def __lshift__(self, arg__1: str) -> None: ...
    @overload
    def __lshift__(self, arg__2: QCborArray) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QCborMap) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QDate) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QDateTime) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QJsonArray) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QJsonDocument) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QLine) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QMargins) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QPoint) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QRect) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QSize) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QTime) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: QUuid) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: str) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Dict[str, QJsonValue]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: str) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QBitArray, int]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QByteArray, bytes]) -> QDataStream: ...
    @overload
    def __lshift__(
        self,
        arg__2: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QEasingCurve, QEasingCurve.Type]) -> QDataStream: ...
    @overload
    def __lshift__(
        self,
        arg__2: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QLineF, QLine]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QLocale, QLocale.Language]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QMarginsF, QMargins]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QPointF, QPoint]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QRectF, QRect]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QSizeF, QSize]) -> QDataStream: ...
    @overload
    def __lshift__(self, arg__2: Union[QUrl, str]) -> QDataStream: ...
    @overload
    def __lshift__(
        self, combination: Union[QKeyCombination, Qt.KeyboardModifiers, Qt.Key]
    ) -> QDataStream: ...
    @overload
    def __lshift__(self, i: int) -> QDataStream: ...
    @overload
    def __lshift__(self, p: Any) -> QDataStream: ...
    @overload
    def __lshift__(self, re: Union[QRegularExpression, str]) -> QDataStream: ...
    @overload
    def __lshift__(self, st: QCborSimpleType) -> QDataStream: ...
    @overload
    def __lshift__(self, tz: QTimeZone) -> QDataStream: ...
    @overload
    def __lshift__(self, version: QVersionNumber) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QCborArray) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QCborMap) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QDate) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QDateTime) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QJsonArray) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QJsonDocument) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QLine) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QMargins) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QPoint) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QRect) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QSize) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QTime) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: QUuid) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: str) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Dict[str, QJsonValue]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: str) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QBitArray, int]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QByteArray, bytes]) -> QDataStream: ...
    @overload
    def __rshift__(
        self,
        arg__2: Union[
            QCborValue,
            QCborKnownTags,
            QCborSimpleType,
            QCborTag,
            QCborValue.Type,
            str,
            QByteArray,
            QCborArray,
            QCborMap,
            bytes,
            float,
            int,
        ],
    ) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QEasingCurve, QEasingCurve.Type]) -> QDataStream: ...
    @overload
    def __rshift__(
        self,
        arg__2: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QLineF, QLine]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QLocale, QLocale.Language]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QMarginsF, QMargins]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QPointF, QPoint]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QRectF, QRect]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QSizeF, QSize]) -> QDataStream: ...
    @overload
    def __rshift__(self, arg__2: Union[QUrl, str]) -> QDataStream: ...
    @overload
    def __rshift__(
        self, combination: Union[QKeyCombination, Qt.KeyboardModifiers, Qt.Key]
    ) -> QDataStream: ...
    @overload
    def __rshift__(self, i: int) -> QDataStream: ...
    @overload
    def __rshift__(self, p: Any) -> QDataStream: ...
    @overload
    def __rshift__(self, re: Union[QRegularExpression, str]) -> QDataStream: ...
    @overload
    def __rshift__(self, st: QCborSimpleType) -> QDataStream: ...
    @overload
    def __rshift__(self, tz: QTimeZone) -> QDataStream: ...
    @overload
    def __rshift__(self, version: QVersionNumber) -> QDataStream: ...
    def abortTransaction(self) -> None: ...
    def atEnd(self) -> bool: ...
    def byteOrder(self) -> QDataStream.ByteOrder: ...
    def commitTransaction(self) -> bool: ...
    def device(self) -> QIODevice: ...
    def floatingPointPrecision(self) -> QDataStream.FloatingPointPrecision: ...
    def isDeviceTransactionStarted(self) -> bool: ...
    def readBool(self) -> bool: ...
    def readDouble(self) -> float: ...
    def readFloat(self) -> float: ...
    def readInt16(self) -> int: ...
    def readInt32(self) -> int: ...
    def readInt64(self) -> int: ...
    def readInt8(self) -> int: ...
    def readQChar(self) -> str: ...
    def readQString(self) -> str: ...
    def readQStringList(self) -> List[str]: ...
    def readQVariant(self) -> Any: ...
    def readRawData(self, arg__1: bytes, len: int) -> int: ...
    def readString(self) -> str: ...
    def readUInt16(self) -> int: ...
    def readUInt32(self) -> int: ...
    def readUInt64(self) -> int: ...
    def readUInt8(self) -> int: ...
    def resetStatus(self) -> None: ...
    def rollbackTransaction(self) -> None: ...
    def setByteOrder(self, arg__1: QDataStream.ByteOrder) -> None: ...
    def setDevice(self, arg__1: QIODevice) -> None: ...
    def setFloatingPointPrecision(self, precision: QDataStream.FloatingPointPrecision) -> None: ...
    def setStatus(self, status: QDataStream.Status) -> None: ...
    def setVersion(self, arg__1: int) -> None: ...
    def skipRawData(self, len: int) -> int: ...
    def startTransaction(self) -> None: ...
    def status(self) -> QDataStream.Status: ...
    def version(self) -> int: ...
    def writeBool(self, arg__1: bool) -> None: ...
    def writeDouble(self, arg__1: float) -> None: ...
    def writeFloat(self, arg__1: float) -> None: ...
    def writeInt16(self, arg__1: int) -> None: ...
    def writeInt32(self, arg__1: int) -> None: ...
    def writeInt64(self, arg__1: int) -> None: ...
    def writeInt8(self, arg__1: int) -> None: ...
    def writeQChar(self, arg__1: str) -> None: ...
    def writeQString(self, arg__1: str) -> None: ...
    def writeQStringList(self, arg__1: Sequence[str]) -> None: ...
    def writeQVariant(self, arg__1: Any) -> None: ...
    def writeRawData(self, arg__1: bytes, len: int) -> int: ...
    def writeString(self, arg__1: str) -> None: ...
    def writeUInt16(self, arg__1: int) -> None: ...
    def writeUInt32(self, arg__1: int) -> None: ...
    def writeUInt64(self, arg__1: int) -> None: ...
    def writeUInt8(self, arg__1: int) -> None: ...

class QDate(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QDate: QDate) -> None: ...
    @overload
    def __init__(self, y: int, m: int, d: int) -> None: ...
    @overload
    def __init__(self, y: int, m: int, d: int, cal: QCalendar) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def addDays(self, days: int) -> QDate: ...
    @overload
    def addMonths(self, months: int) -> QDate: ...
    @overload
    def addMonths(self, months: int, cal: QCalendar) -> QDate: ...
    @overload
    def addYears(self, years: int) -> QDate: ...
    @overload
    def addYears(self, years: int, cal: QCalendar) -> QDate: ...
    @staticmethod
    def currentDate() -> QDate: ...
    @overload
    def day(self) -> int: ...
    @overload
    def day(self, cal: QCalendar) -> int: ...
    @overload
    def dayOfWeek(self) -> int: ...
    @overload
    def dayOfWeek(self, cal: QCalendar) -> int: ...
    @overload
    def dayOfYear(self) -> int: ...
    @overload
    def dayOfYear(self, cal: QCalendar) -> int: ...
    @overload
    def daysInMonth(self) -> int: ...
    @overload
    def daysInMonth(self, cal: QCalendar) -> int: ...
    @overload
    def daysInYear(self) -> int: ...
    @overload
    def daysInYear(self, cal: QCalendar) -> int: ...
    def daysTo(self, d: QDate) -> int: ...
    @overload
    def endOfDay(self, spec: Qt.TimeSpec = ..., offsetSeconds: int = ...) -> QDateTime: ...
    @overload
    def endOfDay(self, zone: QTimeZone) -> QDateTime: ...
    @staticmethod
    def fromJulianDay(jd_: int) -> QDate: ...
    @overload
    @staticmethod
    def fromString(string: str, format: Qt.DateFormat = ...) -> QDate: ...
    @overload
    @staticmethod
    def fromString(string: str, format: str, cal: QCalendar = ...) -> QDate: ...
    def getDate(self) -> Tuple[int, int, int]: ...
    @staticmethod
    def isLeapYear(year: int) -> bool: ...
    def isNull(self) -> bool: ...
    @overload
    def isValid(self) -> bool: ...
    @overload
    @staticmethod
    def isValid(y: int, m: int, d: int) -> bool: ...
    @overload
    def month(self) -> int: ...
    @overload
    def month(self, cal: QCalendar) -> int: ...
    @overload
    def setDate(self, year: int, month: int, day: int) -> bool: ...
    @overload
    def setDate(self, year: int, month: int, day: int, cal: QCalendar) -> bool: ...
    @overload
    def startOfDay(self, spec: Qt.TimeSpec = ..., offsetSeconds: int = ...) -> QDateTime: ...
    @overload
    def startOfDay(self, zone: QTimeZone) -> QDateTime: ...
    def toJulianDay(self) -> int: ...
    def toPython(self) -> object: ...
    @overload
    def toString(self, format: Qt.DateFormat = ...) -> str: ...
    @overload
    def toString(self, format: str, cal: QCalendar = ...) -> str: ...
    def weekNumber(self) -> Tuple[Tuple, int]: ...
    @overload
    def year(self) -> int: ...
    @overload
    def year(self, cal: QCalendar) -> int: ...

class QDateTime(Shiboken.Object):
    class YearRange(Enum):

        First: QDateTime.YearRange = ...  # -0x116bc370
        Last: QDateTime.YearRange = ...  # 0x116bd2d2
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, arg__1: int, arg__2: int, arg__3: int, arg__4: int, arg__5: int, arg__6: int
    ) -> None: ...
    @overload
    def __init__(
        self,
        arg__1: int,
        arg__2: int,
        arg__3: int,
        arg__4: int,
        arg__5: int,
        arg__6: int,
        arg__7: int,
        arg__8: int = ...,
    ) -> None: ...
    @overload
    def __init__(
        self, date: QDate, time: QTime, spec: Qt.TimeSpec = ..., offsetSeconds: int = ...
    ) -> None: ...
    @overload
    def __init__(self, date: QDate, time: QTime, timeZone: QTimeZone) -> None: ...
    @overload
    def __init__(self, other: QDateTime) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def addDays(self, days: int) -> QDateTime: ...
    def addMSecs(self, msecs: int) -> QDateTime: ...
    def addMonths(self, months: int) -> QDateTime: ...
    def addSecs(self, secs: int) -> QDateTime: ...
    def addYears(self, years: int) -> QDateTime: ...
    @staticmethod
    def currentDateTime() -> QDateTime: ...
    @staticmethod
    def currentDateTimeUtc() -> QDateTime: ...
    @staticmethod
    def currentMSecsSinceEpoch() -> int: ...
    @staticmethod
    def currentSecsSinceEpoch() -> int: ...
    def date(self) -> QDate: ...
    def daysTo(self, arg__1: QDateTime) -> int: ...
    @overload
    @staticmethod
    def fromMSecsSinceEpoch(
        msecs: int, spec: Qt.TimeSpec = ..., offsetFromUtc: int = ...
    ) -> QDateTime: ...
    @overload
    @staticmethod
    def fromMSecsSinceEpoch(msecs: int, timeZone: QTimeZone) -> QDateTime: ...
    @overload
    @staticmethod
    def fromSecsSinceEpoch(
        secs: int, spec: Qt.TimeSpec = ..., offsetFromUtc: int = ...
    ) -> QDateTime: ...
    @overload
    @staticmethod
    def fromSecsSinceEpoch(secs: int, timeZone: QTimeZone) -> QDateTime: ...
    @overload
    @staticmethod
    def fromString(string: str, format: Qt.DateFormat = ...) -> QDateTime: ...
    @overload
    @staticmethod
    def fromString(string: str, format: str, cal: QCalendar = ...) -> QDateTime: ...
    def isDaylightTime(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isValid(self) -> bool: ...
    def msecsTo(self, arg__1: QDateTime) -> int: ...
    def offsetFromUtc(self) -> int: ...
    def secsTo(self, arg__1: QDateTime) -> int: ...
    def setDate(self, date: QDate) -> None: ...
    def setMSecsSinceEpoch(self, msecs: int) -> None: ...
    def setOffsetFromUtc(self, offsetSeconds: int) -> None: ...
    def setSecsSinceEpoch(self, secs: int) -> None: ...
    def setTime(self, time: QTime) -> None: ...
    def setTimeSpec(self, spec: Qt.TimeSpec) -> None: ...
    def setTimeZone(self, toZone: QTimeZone) -> None: ...
    def swap(self, other: QDateTime) -> None: ...
    def time(self) -> QTime: ...
    def timeSpec(self) -> Qt.TimeSpec: ...
    def timeZone(self) -> QTimeZone: ...
    def timeZoneAbbreviation(self) -> str: ...
    def toLocalTime(self) -> QDateTime: ...
    def toMSecsSinceEpoch(self) -> int: ...
    def toOffsetFromUtc(self, offsetSeconds: int) -> QDateTime: ...
    def toPython(self) -> object: ...
    def toSecsSinceEpoch(self) -> int: ...
    @overload
    def toString(self, format: Qt.DateFormat = ...) -> str: ...
    @overload
    def toString(self, format: str, cal: QCalendar = ...) -> str: ...
    def toTimeSpec(self, spec: Qt.TimeSpec) -> QDateTime: ...
    def toTimeZone(self, toZone: QTimeZone) -> QDateTime: ...
    def toUTC(self) -> QDateTime: ...

class QDeadlineTimer(Shiboken.Object):

    Forever: QDeadlineTimer.ForeverConstant = ...  # 0x0
    class ForeverConstant(Enum):

        Forever: QDeadlineTimer.ForeverConstant = ...  # 0x0
    @overload
    def __init__(
        self,
        QDeadlineTimer: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int],
    ) -> None: ...
    @overload
    def __init__(
        self, arg__1: QDeadlineTimer.ForeverConstant, type_: Qt.TimerType = ...
    ) -> None: ...
    @overload
    def __init__(self, msecs: int, type: Qt.TimerType = ...) -> None: ...
    @overload
    def __init__(self, type_: Qt.TimerType = ...) -> None: ...
    def __add__(self, msecs: int) -> QDeadlineTimer: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, msecs: int) -> QDeadlineTimer: ...
    def __isub__(self, msecs: int) -> QDeadlineTimer: ...
    @overload
    def __sub__(
        self, dt2: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int]
    ) -> int: ...
    @overload
    def __sub__(self, msecs: int) -> QDeadlineTimer: ...
    def _q_data(self) -> Tuple[int, int]: ...
    @staticmethod
    def addNSecs(
        dt: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int], nsecs: int
    ) -> QDeadlineTimer: ...
    @staticmethod
    def current(timerType: Qt.TimerType = ...) -> QDeadlineTimer: ...
    def deadline(self) -> int: ...
    def deadlineNSecs(self) -> int: ...
    def hasExpired(self) -> bool: ...
    def isForever(self) -> bool: ...
    def remainingTime(self) -> int: ...
    def remainingTimeNSecs(self) -> int: ...
    def setDeadline(self, msecs: int, timerType: Qt.TimerType = ...) -> None: ...
    def setPreciseDeadline(self, secs: int, nsecs: int = ..., type: Qt.TimerType = ...) -> None: ...
    def setPreciseRemainingTime(
        self, secs: int, nsecs: int = ..., type: Qt.TimerType = ...
    ) -> None: ...
    def setRemainingTime(self, msecs: int, type: Qt.TimerType = ...) -> None: ...
    def setTimerType(self, type: Qt.TimerType) -> None: ...
    def swap(
        self, other: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int]
    ) -> None: ...
    def timerType(self) -> Qt.TimerType: ...

class QDir(Shiboken.Object):

    NoFilter: QDir.Filter = ...  # -0x1
    Dirs: QDir.Filter = ...  # 0x1
    Files: QDir.Filter = ...  # 0x2
    Drives: QDir.Filter = ...  # 0x4
    AllEntries: QDir.Filter = ...  # 0x7
    NoSymLinks: QDir.Filter = ...  # 0x8
    TypeMask: QDir.Filter = ...  # 0xf
    Readable: QDir.Filter = ...  # 0x10
    Writable: QDir.Filter = ...  # 0x20
    Executable: QDir.Filter = ...  # 0x40
    PermissionMask: QDir.Filter = ...  # 0x70
    Modified: QDir.Filter = ...  # 0x80
    Hidden: QDir.Filter = ...  # 0x100
    System: QDir.Filter = ...  # 0x200
    AccessMask: QDir.Filter = ...  # 0x3f0
    AllDirs: QDir.Filter = ...  # 0x400
    CaseSensitive: QDir.Filter = ...  # 0x800
    NoDot: QDir.Filter = ...  # 0x2000
    NoDotDot: QDir.Filter = ...  # 0x4000
    NoDotAndDotDot: QDir.Filter = ...  # 0x6000
    NoSort: QDir.SortFlag = ...  # -0x1
    Name: QDir.SortFlag = ...  # 0x0
    Time: QDir.SortFlag = ...  # 0x1
    Size: QDir.SortFlag = ...  # 0x2
    SortByMask: QDir.SortFlag = ...  # 0x3
    Unsorted: QDir.SortFlag = ...  # 0x3
    DirsFirst: QDir.SortFlag = ...  # 0x4
    Reversed: QDir.SortFlag = ...  # 0x8
    IgnoreCase: QDir.SortFlag = ...  # 0x10
    DirsLast: QDir.SortFlag = ...  # 0x20
    LocaleAware: QDir.SortFlag = ...  # 0x40
    Type: QDir.SortFlag = ...  # 0x80
    class Filter(Enum):

        NoFilter: QDir.Filter = ...  # -0x1
        Dirs: QDir.Filter = ...  # 0x1
        Files: QDir.Filter = ...  # 0x2
        Drives: QDir.Filter = ...  # 0x4
        AllEntries: QDir.Filter = ...  # 0x7
        NoSymLinks: QDir.Filter = ...  # 0x8
        TypeMask: QDir.Filter = ...  # 0xf
        Readable: QDir.Filter = ...  # 0x10
        Writable: QDir.Filter = ...  # 0x20
        Executable: QDir.Filter = ...  # 0x40
        PermissionMask: QDir.Filter = ...  # 0x70
        Modified: QDir.Filter = ...  # 0x80
        Hidden: QDir.Filter = ...  # 0x100
        System: QDir.Filter = ...  # 0x200
        AccessMask: QDir.Filter = ...  # 0x3f0
        AllDirs: QDir.Filter = ...  # 0x400
        CaseSensitive: QDir.Filter = ...  # 0x800
        NoDot: QDir.Filter = ...  # 0x2000
        NoDotDot: QDir.Filter = ...  # 0x4000
        NoDotAndDotDot: QDir.Filter = ...  # 0x6000
    class Filters(object): ...
    class SortFlag(Enum):

        NoSort: QDir.SortFlag = ...  # -0x1
        Name: QDir.SortFlag = ...  # 0x0
        Time: QDir.SortFlag = ...  # 0x1
        Size: QDir.SortFlag = ...  # 0x2
        SortByMask: QDir.SortFlag = ...  # 0x3
        Unsorted: QDir.SortFlag = ...  # 0x3
        DirsFirst: QDir.SortFlag = ...  # 0x4
        Reversed: QDir.SortFlag = ...  # 0x8
        IgnoreCase: QDir.SortFlag = ...  # 0x10
        DirsLast: QDir.SortFlag = ...  # 0x20
        LocaleAware: QDir.SortFlag = ...  # 0x40
        Type: QDir.SortFlag = ...  # 0x80
    class SortFlags(object): ...
    @overload
    def __init__(self, arg__1: Union[QDir, str]) -> None: ...
    @overload
    def __init__(self, path: Union[str, bytes, os.PathLike, NoneType]) -> None: ...
    @overload
    def __init__(
        self,
        path: Union[str, bytes, os.PathLike],
        nameFilter: str,
        sort: QDir.SortFlags = ...,
        filter: QDir.Filters = ...,
    ) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def absoluteFilePath(self, fileName: str) -> str: ...
    def absolutePath(self) -> str: ...
    @staticmethod
    def addSearchPath(prefix: str, path: Union[str, bytes, os.PathLike]) -> None: ...
    def canonicalPath(self) -> str: ...
    def cd(self, dirName: str) -> bool: ...
    def cdUp(self) -> bool: ...
    @staticmethod
    def cleanPath(path: str) -> str: ...
    def count(self) -> int: ...
    @staticmethod
    def current() -> QDir: ...
    @staticmethod
    def currentPath() -> str: ...
    def dirName(self) -> str: ...
    @staticmethod
    def drives() -> List[QFileInfo]: ...
    @overload
    def entryInfoList(
        self, filters: QDir.Filters = ..., sort: QDir.SortFlags = ...
    ) -> List[QFileInfo]: ...
    @overload
    def entryInfoList(
        self, nameFilters: Sequence[str], filters: QDir.Filters = ..., sort: QDir.SortFlags = ...
    ) -> List[QFileInfo]: ...
    @overload
    def entryList(self, filters: QDir.Filters = ..., sort: QDir.SortFlags = ...) -> List[str]: ...
    @overload
    def entryList(
        self, nameFilters: Sequence[str], filters: QDir.Filters = ..., sort: QDir.SortFlags = ...
    ) -> List[str]: ...
    @overload
    def exists(self) -> bool: ...
    @overload
    def exists(self, name: str) -> bool: ...
    def filePath(self, fileName: str) -> str: ...
    def filter(self) -> QDir.Filters: ...
    @staticmethod
    def fromNativeSeparators(pathName: str) -> str: ...
    @staticmethod
    def home() -> QDir: ...
    @staticmethod
    def homePath() -> str: ...
    def isAbsolute(self) -> bool: ...
    @staticmethod
    def isAbsolutePath(path: str) -> bool: ...
    def isEmpty(self, filters: QDir.Filters = ...) -> bool: ...
    def isReadable(self) -> bool: ...
    def isRelative(self) -> bool: ...
    @staticmethod
    def isRelativePath(path: str) -> bool: ...
    def isRoot(self) -> bool: ...
    @staticmethod
    def listSeparator() -> str: ...
    def makeAbsolute(self) -> bool: ...
    @overload
    @staticmethod
    def match(filter: str, fileName: str) -> bool: ...
    @overload
    @staticmethod
    def match(filters: Sequence[str], fileName: str) -> bool: ...
    def mkdir(self, dirName: str) -> bool: ...
    def mkpath(self, dirPath: str) -> bool: ...
    def nameFilters(self) -> List[str]: ...
    @staticmethod
    def nameFiltersFromString(nameFilter: str) -> List[str]: ...
    def path(self) -> str: ...
    def refresh(self) -> None: ...
    def relativeFilePath(self, fileName: str) -> str: ...
    def remove(self, fileName: str) -> bool: ...
    def removeRecursively(self) -> bool: ...
    def rename(self, oldName: str, newName: str) -> bool: ...
    def rmdir(self, dirName: str) -> bool: ...
    def rmpath(self, dirPath: str) -> bool: ...
    @staticmethod
    def root() -> QDir: ...
    @staticmethod
    def rootPath() -> str: ...
    @staticmethod
    def searchPaths(prefix: str) -> List[str]: ...
    @staticmethod
    def separator() -> str: ...
    @staticmethod
    def setCurrent(path: str) -> bool: ...
    def setFilter(self, filter: QDir.Filters) -> None: ...
    def setNameFilters(self, nameFilters: Sequence[str]) -> None: ...
    def setPath(self, path: Union[str, bytes, os.PathLike]) -> None: ...
    @staticmethod
    def setSearchPaths(prefix: str, searchPaths: Sequence[str]) -> None: ...
    def setSorting(self, sort: QDir.SortFlags) -> None: ...
    def sorting(self) -> QDir.SortFlags: ...
    def swap(self, other: Union[QDir, str]) -> None: ...
    @staticmethod
    def temp() -> QDir: ...
    @staticmethod
    def tempPath() -> str: ...
    @staticmethod
    def toNativeSeparators(pathName: str) -> str: ...

class QDirIterator(Shiboken.Object):

    NoIteratorFlags: QDirIterator.IteratorFlag = ...  # 0x0
    FollowSymlinks: QDirIterator.IteratorFlag = ...  # 0x1
    Subdirectories: QDirIterator.IteratorFlag = ...  # 0x2
    class IteratorFlag(Enum):

        NoIteratorFlags: QDirIterator.IteratorFlag = ...  # 0x0
        FollowSymlinks: QDirIterator.IteratorFlag = ...  # 0x1
        Subdirectories: QDirIterator.IteratorFlag = ...  # 0x2
    class IteratorFlags(object): ...
    @overload
    def __init__(self, dir: Union[QDir, str], flags: QDirIterator.IteratorFlags = ...) -> None: ...
    @overload
    def __init__(
        self, path: str, filter: QDir.Filters, flags: QDirIterator.IteratorFlags = ...
    ) -> None: ...
    @overload
    def __init__(self, path: str, flags: QDirIterator.IteratorFlags = ...) -> None: ...
    @overload
    def __init__(
        self,
        path: str,
        nameFilters: Sequence[str],
        filters: QDir.Filters = ...,
        flags: QDirIterator.IteratorFlags = ...,
    ) -> None: ...
    def fileInfo(self) -> QFileInfo: ...
    def fileName(self) -> str: ...
    def filePath(self) -> str: ...
    def hasNext(self) -> bool: ...
    def next(self) -> str: ...
    def path(self) -> str: ...

class QDynamicPropertyChangeEvent(QEvent):
    @overload
    def __init__(self, arg__1: QDynamicPropertyChangeEvent) -> None: ...
    @overload
    def __init__(self, name: Union[QByteArray, bytes]) -> None: ...
    def clone(self) -> QDynamicPropertyChangeEvent: ...
    def propertyName(self) -> QByteArray: ...

class QEasingCurve(Shiboken.Object):

    Linear: QEasingCurve.Type = ...  # 0x0
    InQuad: QEasingCurve.Type = ...  # 0x1
    OutQuad: QEasingCurve.Type = ...  # 0x2
    InOutQuad: QEasingCurve.Type = ...  # 0x3
    OutInQuad: QEasingCurve.Type = ...  # 0x4
    InCubic: QEasingCurve.Type = ...  # 0x5
    OutCubic: QEasingCurve.Type = ...  # 0x6
    InOutCubic: QEasingCurve.Type = ...  # 0x7
    OutInCubic: QEasingCurve.Type = ...  # 0x8
    InQuart: QEasingCurve.Type = ...  # 0x9
    OutQuart: QEasingCurve.Type = ...  # 0xa
    InOutQuart: QEasingCurve.Type = ...  # 0xb
    OutInQuart: QEasingCurve.Type = ...  # 0xc
    InQuint: QEasingCurve.Type = ...  # 0xd
    OutQuint: QEasingCurve.Type = ...  # 0xe
    InOutQuint: QEasingCurve.Type = ...  # 0xf
    OutInQuint: QEasingCurve.Type = ...  # 0x10
    InSine: QEasingCurve.Type = ...  # 0x11
    OutSine: QEasingCurve.Type = ...  # 0x12
    InOutSine: QEasingCurve.Type = ...  # 0x13
    OutInSine: QEasingCurve.Type = ...  # 0x14
    InExpo: QEasingCurve.Type = ...  # 0x15
    OutExpo: QEasingCurve.Type = ...  # 0x16
    InOutExpo: QEasingCurve.Type = ...  # 0x17
    OutInExpo: QEasingCurve.Type = ...  # 0x18
    InCirc: QEasingCurve.Type = ...  # 0x19
    OutCirc: QEasingCurve.Type = ...  # 0x1a
    InOutCirc: QEasingCurve.Type = ...  # 0x1b
    OutInCirc: QEasingCurve.Type = ...  # 0x1c
    InElastic: QEasingCurve.Type = ...  # 0x1d
    OutElastic: QEasingCurve.Type = ...  # 0x1e
    InOutElastic: QEasingCurve.Type = ...  # 0x1f
    OutInElastic: QEasingCurve.Type = ...  # 0x20
    InBack: QEasingCurve.Type = ...  # 0x21
    OutBack: QEasingCurve.Type = ...  # 0x22
    InOutBack: QEasingCurve.Type = ...  # 0x23
    OutInBack: QEasingCurve.Type = ...  # 0x24
    InBounce: QEasingCurve.Type = ...  # 0x25
    OutBounce: QEasingCurve.Type = ...  # 0x26
    InOutBounce: QEasingCurve.Type = ...  # 0x27
    OutInBounce: QEasingCurve.Type = ...  # 0x28
    InCurve: QEasingCurve.Type = ...  # 0x29
    OutCurve: QEasingCurve.Type = ...  # 0x2a
    SineCurve: QEasingCurve.Type = ...  # 0x2b
    CosineCurve: QEasingCurve.Type = ...  # 0x2c
    BezierSpline: QEasingCurve.Type = ...  # 0x2d
    TCBSpline: QEasingCurve.Type = ...  # 0x2e
    Custom: QEasingCurve.Type = ...  # 0x2f
    NCurveTypes: QEasingCurve.Type = ...  # 0x30
    class Type(Enum):

        Linear: QEasingCurve.Type = ...  # 0x0
        InQuad: QEasingCurve.Type = ...  # 0x1
        OutQuad: QEasingCurve.Type = ...  # 0x2
        InOutQuad: QEasingCurve.Type = ...  # 0x3
        OutInQuad: QEasingCurve.Type = ...  # 0x4
        InCubic: QEasingCurve.Type = ...  # 0x5
        OutCubic: QEasingCurve.Type = ...  # 0x6
        InOutCubic: QEasingCurve.Type = ...  # 0x7
        OutInCubic: QEasingCurve.Type = ...  # 0x8
        InQuart: QEasingCurve.Type = ...  # 0x9
        OutQuart: QEasingCurve.Type = ...  # 0xa
        InOutQuart: QEasingCurve.Type = ...  # 0xb
        OutInQuart: QEasingCurve.Type = ...  # 0xc
        InQuint: QEasingCurve.Type = ...  # 0xd
        OutQuint: QEasingCurve.Type = ...  # 0xe
        InOutQuint: QEasingCurve.Type = ...  # 0xf
        OutInQuint: QEasingCurve.Type = ...  # 0x10
        InSine: QEasingCurve.Type = ...  # 0x11
        OutSine: QEasingCurve.Type = ...  # 0x12
        InOutSine: QEasingCurve.Type = ...  # 0x13
        OutInSine: QEasingCurve.Type = ...  # 0x14
        InExpo: QEasingCurve.Type = ...  # 0x15
        OutExpo: QEasingCurve.Type = ...  # 0x16
        InOutExpo: QEasingCurve.Type = ...  # 0x17
        OutInExpo: QEasingCurve.Type = ...  # 0x18
        InCirc: QEasingCurve.Type = ...  # 0x19
        OutCirc: QEasingCurve.Type = ...  # 0x1a
        InOutCirc: QEasingCurve.Type = ...  # 0x1b
        OutInCirc: QEasingCurve.Type = ...  # 0x1c
        InElastic: QEasingCurve.Type = ...  # 0x1d
        OutElastic: QEasingCurve.Type = ...  # 0x1e
        InOutElastic: QEasingCurve.Type = ...  # 0x1f
        OutInElastic: QEasingCurve.Type = ...  # 0x20
        InBack: QEasingCurve.Type = ...  # 0x21
        OutBack: QEasingCurve.Type = ...  # 0x22
        InOutBack: QEasingCurve.Type = ...  # 0x23
        OutInBack: QEasingCurve.Type = ...  # 0x24
        InBounce: QEasingCurve.Type = ...  # 0x25
        OutBounce: QEasingCurve.Type = ...  # 0x26
        InOutBounce: QEasingCurve.Type = ...  # 0x27
        OutInBounce: QEasingCurve.Type = ...  # 0x28
        InCurve: QEasingCurve.Type = ...  # 0x29
        OutCurve: QEasingCurve.Type = ...  # 0x2a
        SineCurve: QEasingCurve.Type = ...  # 0x2b
        CosineCurve: QEasingCurve.Type = ...  # 0x2c
        BezierSpline: QEasingCurve.Type = ...  # 0x2d
        TCBSpline: QEasingCurve.Type = ...  # 0x2e
        Custom: QEasingCurve.Type = ...  # 0x2f
        NCurveTypes: QEasingCurve.Type = ...  # 0x30
    @overload
    def __init__(self, other: Union[QEasingCurve, QEasingCurve.Type]) -> None: ...
    @overload
    def __init__(self, type: QEasingCurve.Type = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def addCubicBezierSegment(
        self,
        c1: Union[QPointF, QPoint],
        c2: Union[QPointF, QPoint],
        endPoint: Union[QPointF, QPoint],
    ) -> None: ...
    def addTCBSegment(
        self, nextPoint: Union[QPointF, QPoint], t: float, c: float, b: float
    ) -> None: ...
    def amplitude(self) -> float: ...
    def customType(self) -> object: ...
    def overshoot(self) -> float: ...
    def period(self) -> float: ...
    def setAmplitude(self, amplitude: float) -> None: ...
    def setCustomType(self, arg__1: object) -> None: ...
    def setOvershoot(self, overshoot: float) -> None: ...
    def setPeriod(self, period: float) -> None: ...
    def setType(self, type: QEasingCurve.Type) -> None: ...
    def swap(self, other: Union[QEasingCurve, QEasingCurve.Type]) -> None: ...
    def toCubicSpline(self) -> List[QPointF]: ...
    def type(self) -> QEasingCurve.Type: ...
    def valueForProgress(self, progress: float) -> float: ...

class QElapsedTimer(Shiboken.Object):

    SystemTime: QElapsedTimer.ClockType = ...  # 0x0
    MonotonicClock: QElapsedTimer.ClockType = ...  # 0x1
    TickCounter: QElapsedTimer.ClockType = ...  # 0x2
    MachAbsoluteTime: QElapsedTimer.ClockType = ...  # 0x3
    PerformanceCounter: QElapsedTimer.ClockType = ...  # 0x4
    class ClockType(Enum):

        SystemTime: QElapsedTimer.ClockType = ...  # 0x0
        MonotonicClock: QElapsedTimer.ClockType = ...  # 0x1
        TickCounter: QElapsedTimer.ClockType = ...  # 0x2
        MachAbsoluteTime: QElapsedTimer.ClockType = ...  # 0x3
        PerformanceCounter: QElapsedTimer.ClockType = ...  # 0x4
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QElapsedTimer: QElapsedTimer) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def clockType() -> QElapsedTimer.ClockType: ...
    def elapsed(self) -> int: ...
    def hasExpired(self, timeout: int) -> bool: ...
    def invalidate(self) -> None: ...
    @staticmethod
    def isMonotonic() -> bool: ...
    def isValid(self) -> bool: ...
    def msecsSinceReference(self) -> int: ...
    def msecsTo(self, other: QElapsedTimer) -> int: ...
    def nsecsElapsed(self) -> int: ...
    def restart(self) -> int: ...
    def secsTo(self, other: QElapsedTimer) -> int: ...
    def start(self) -> None: ...

class QEvent(Shiboken.Object):

    None_: QEvent.Type = ...  # 0x0
    Timer: QEvent.Type = ...  # 0x1
    MouseButtonPress: QEvent.Type = ...  # 0x2
    MouseButtonRelease: QEvent.Type = ...  # 0x3
    MouseButtonDblClick: QEvent.Type = ...  # 0x4
    MouseMove: QEvent.Type = ...  # 0x5
    KeyPress: QEvent.Type = ...  # 0x6
    KeyRelease: QEvent.Type = ...  # 0x7
    FocusIn: QEvent.Type = ...  # 0x8
    FocusOut: QEvent.Type = ...  # 0x9
    Enter: QEvent.Type = ...  # 0xa
    Leave: QEvent.Type = ...  # 0xb
    Paint: QEvent.Type = ...  # 0xc
    Move: QEvent.Type = ...  # 0xd
    Resize: QEvent.Type = ...  # 0xe
    Create: QEvent.Type = ...  # 0xf
    Destroy: QEvent.Type = ...  # 0x10
    Show: QEvent.Type = ...  # 0x11
    Hide: QEvent.Type = ...  # 0x12
    Close: QEvent.Type = ...  # 0x13
    Quit: QEvent.Type = ...  # 0x14
    ParentChange: QEvent.Type = ...  # 0x15
    ThreadChange: QEvent.Type = ...  # 0x16
    FocusAboutToChange: QEvent.Type = ...  # 0x17
    WindowActivate: QEvent.Type = ...  # 0x18
    WindowDeactivate: QEvent.Type = ...  # 0x19
    ShowToParent: QEvent.Type = ...  # 0x1a
    HideToParent: QEvent.Type = ...  # 0x1b
    Wheel: QEvent.Type = ...  # 0x1f
    WindowTitleChange: QEvent.Type = ...  # 0x21
    WindowIconChange: QEvent.Type = ...  # 0x22
    ApplicationWindowIconChange: QEvent.Type = ...  # 0x23
    ApplicationFontChange: QEvent.Type = ...  # 0x24
    ApplicationLayoutDirectionChange: QEvent.Type = ...  # 0x25
    ApplicationPaletteChange: QEvent.Type = ...  # 0x26
    PaletteChange: QEvent.Type = ...  # 0x27
    Clipboard: QEvent.Type = ...  # 0x28
    Speech: QEvent.Type = ...  # 0x2a
    MetaCall: QEvent.Type = ...  # 0x2b
    SockAct: QEvent.Type = ...  # 0x32
    ShortcutOverride: QEvent.Type = ...  # 0x33
    DeferredDelete: QEvent.Type = ...  # 0x34
    DragEnter: QEvent.Type = ...  # 0x3c
    DragMove: QEvent.Type = ...  # 0x3d
    DragLeave: QEvent.Type = ...  # 0x3e
    Drop: QEvent.Type = ...  # 0x3f
    DragResponse: QEvent.Type = ...  # 0x40
    ChildAdded: QEvent.Type = ...  # 0x44
    ChildPolished: QEvent.Type = ...  # 0x45
    ChildRemoved: QEvent.Type = ...  # 0x47
    ShowWindowRequest: QEvent.Type = ...  # 0x49
    PolishRequest: QEvent.Type = ...  # 0x4a
    Polish: QEvent.Type = ...  # 0x4b
    LayoutRequest: QEvent.Type = ...  # 0x4c
    UpdateRequest: QEvent.Type = ...  # 0x4d
    UpdateLater: QEvent.Type = ...  # 0x4e
    EmbeddingControl: QEvent.Type = ...  # 0x4f
    ActivateControl: QEvent.Type = ...  # 0x50
    DeactivateControl: QEvent.Type = ...  # 0x51
    ContextMenu: QEvent.Type = ...  # 0x52
    InputMethod: QEvent.Type = ...  # 0x53
    TabletMove: QEvent.Type = ...  # 0x57
    LocaleChange: QEvent.Type = ...  # 0x58
    LanguageChange: QEvent.Type = ...  # 0x59
    LayoutDirectionChange: QEvent.Type = ...  # 0x5a
    Style: QEvent.Type = ...  # 0x5b
    TabletPress: QEvent.Type = ...  # 0x5c
    TabletRelease: QEvent.Type = ...  # 0x5d
    OkRequest: QEvent.Type = ...  # 0x5e
    HelpRequest: QEvent.Type = ...  # 0x5f
    IconDrag: QEvent.Type = ...  # 0x60
    FontChange: QEvent.Type = ...  # 0x61
    EnabledChange: QEvent.Type = ...  # 0x62
    ActivationChange: QEvent.Type = ...  # 0x63
    StyleChange: QEvent.Type = ...  # 0x64
    IconTextChange: QEvent.Type = ...  # 0x65
    ModifiedChange: QEvent.Type = ...  # 0x66
    WindowBlocked: QEvent.Type = ...  # 0x67
    WindowUnblocked: QEvent.Type = ...  # 0x68
    WindowStateChange: QEvent.Type = ...  # 0x69
    ReadOnlyChange: QEvent.Type = ...  # 0x6a
    MouseTrackingChange: QEvent.Type = ...  # 0x6d
    ToolTip: QEvent.Type = ...  # 0x6e
    WhatsThis: QEvent.Type = ...  # 0x6f
    StatusTip: QEvent.Type = ...  # 0x70
    ActionChanged: QEvent.Type = ...  # 0x71
    ActionAdded: QEvent.Type = ...  # 0x72
    ActionRemoved: QEvent.Type = ...  # 0x73
    FileOpen: QEvent.Type = ...  # 0x74
    Shortcut: QEvent.Type = ...  # 0x75
    WhatsThisClicked: QEvent.Type = ...  # 0x76
    ToolBarChange: QEvent.Type = ...  # 0x78
    ApplicationActivate: QEvent.Type = ...  # 0x79
    ApplicationActivated: QEvent.Type = ...  # 0x79
    ApplicationDeactivate: QEvent.Type = ...  # 0x7a
    ApplicationDeactivated: QEvent.Type = ...  # 0x7a
    QueryWhatsThis: QEvent.Type = ...  # 0x7b
    EnterWhatsThisMode: QEvent.Type = ...  # 0x7c
    LeaveWhatsThisMode: QEvent.Type = ...  # 0x7d
    ZOrderChange: QEvent.Type = ...  # 0x7e
    HoverEnter: QEvent.Type = ...  # 0x7f
    HoverLeave: QEvent.Type = ...  # 0x80
    HoverMove: QEvent.Type = ...  # 0x81
    ParentAboutToChange: QEvent.Type = ...  # 0x83
    WinEventAct: QEvent.Type = ...  # 0x84
    AcceptDropsChange: QEvent.Type = ...  # 0x98
    ZeroTimerEvent: QEvent.Type = ...  # 0x9a
    GraphicsSceneMouseMove: QEvent.Type = ...  # 0x9b
    GraphicsSceneMousePress: QEvent.Type = ...  # 0x9c
    GraphicsSceneMouseRelease: QEvent.Type = ...  # 0x9d
    GraphicsSceneMouseDoubleClick: QEvent.Type = ...  # 0x9e
    GraphicsSceneContextMenu: QEvent.Type = ...  # 0x9f
    GraphicsSceneHoverEnter: QEvent.Type = ...  # 0xa0
    GraphicsSceneHoverMove: QEvent.Type = ...  # 0xa1
    GraphicsSceneHoverLeave: QEvent.Type = ...  # 0xa2
    GraphicsSceneHelp: QEvent.Type = ...  # 0xa3
    GraphicsSceneDragEnter: QEvent.Type = ...  # 0xa4
    GraphicsSceneDragMove: QEvent.Type = ...  # 0xa5
    GraphicsSceneDragLeave: QEvent.Type = ...  # 0xa6
    GraphicsSceneDrop: QEvent.Type = ...  # 0xa7
    GraphicsSceneWheel: QEvent.Type = ...  # 0xa8
    KeyboardLayoutChange: QEvent.Type = ...  # 0xa9
    DynamicPropertyChange: QEvent.Type = ...  # 0xaa
    TabletEnterProximity: QEvent.Type = ...  # 0xab
    TabletLeaveProximity: QEvent.Type = ...  # 0xac
    NonClientAreaMouseMove: QEvent.Type = ...  # 0xad
    NonClientAreaMouseButtonPress: QEvent.Type = ...  # 0xae
    NonClientAreaMouseButtonRelease: QEvent.Type = ...  # 0xaf
    NonClientAreaMouseButtonDblClick: QEvent.Type = ...  # 0xb0
    MacSizeChange: QEvent.Type = ...  # 0xb1
    ContentsRectChange: QEvent.Type = ...  # 0xb2
    MacGLWindowChange: QEvent.Type = ...  # 0xb3
    FutureCallOut: QEvent.Type = ...  # 0xb4
    GraphicsSceneResize: QEvent.Type = ...  # 0xb5
    GraphicsSceneMove: QEvent.Type = ...  # 0xb6
    CursorChange: QEvent.Type = ...  # 0xb7
    ToolTipChange: QEvent.Type = ...  # 0xb8
    NetworkReplyUpdated: QEvent.Type = ...  # 0xb9
    GrabMouse: QEvent.Type = ...  # 0xba
    UngrabMouse: QEvent.Type = ...  # 0xbb
    GrabKeyboard: QEvent.Type = ...  # 0xbc
    UngrabKeyboard: QEvent.Type = ...  # 0xbd
    StateMachineSignal: QEvent.Type = ...  # 0xc0
    StateMachineWrapped: QEvent.Type = ...  # 0xc1
    TouchBegin: QEvent.Type = ...  # 0xc2
    TouchUpdate: QEvent.Type = ...  # 0xc3
    TouchEnd: QEvent.Type = ...  # 0xc4
    NativeGesture: QEvent.Type = ...  # 0xc5
    Gesture: QEvent.Type = ...  # 0xc6
    RequestSoftwareInputPanel: QEvent.Type = ...  # 0xc7
    CloseSoftwareInputPanel: QEvent.Type = ...  # 0xc8
    GestureOverride: QEvent.Type = ...  # 0xca
    WinIdChange: QEvent.Type = ...  # 0xcb
    ScrollPrepare: QEvent.Type = ...  # 0xcc
    Scroll: QEvent.Type = ...  # 0xcd
    Expose: QEvent.Type = ...  # 0xce
    InputMethodQuery: QEvent.Type = ...  # 0xcf
    OrientationChange: QEvent.Type = ...  # 0xd0
    TouchCancel: QEvent.Type = ...  # 0xd1
    ThemeChange: QEvent.Type = ...  # 0xd2
    SockClose: QEvent.Type = ...  # 0xd3
    PlatformPanel: QEvent.Type = ...  # 0xd4
    StyleAnimationUpdate: QEvent.Type = ...  # 0xd5
    ApplicationStateChange: QEvent.Type = ...  # 0xd6
    WindowChangeInternal: QEvent.Type = ...  # 0xd7
    ScreenChangeInternal: QEvent.Type = ...  # 0xd8
    PlatformSurface: QEvent.Type = ...  # 0xd9
    Pointer: QEvent.Type = ...  # 0xda
    TabletTrackingChange: QEvent.Type = ...  # 0xdb
    GraphicsSceneLeave: QEvent.Type = ...  # 0xdc
    User: QEvent.Type = ...  # 0x3e8
    MaxUser: QEvent.Type = ...  # 0xffff
    class Type(Enum):

        None_: QEvent.Type = ...  # 0x0
        Timer: QEvent.Type = ...  # 0x1
        MouseButtonPress: QEvent.Type = ...  # 0x2
        MouseButtonRelease: QEvent.Type = ...  # 0x3
        MouseButtonDblClick: QEvent.Type = ...  # 0x4
        MouseMove: QEvent.Type = ...  # 0x5
        KeyPress: QEvent.Type = ...  # 0x6
        KeyRelease: QEvent.Type = ...  # 0x7
        FocusIn: QEvent.Type = ...  # 0x8
        FocusOut: QEvent.Type = ...  # 0x9
        Enter: QEvent.Type = ...  # 0xa
        Leave: QEvent.Type = ...  # 0xb
        Paint: QEvent.Type = ...  # 0xc
        Move: QEvent.Type = ...  # 0xd
        Resize: QEvent.Type = ...  # 0xe
        Create: QEvent.Type = ...  # 0xf
        Destroy: QEvent.Type = ...  # 0x10
        Show: QEvent.Type = ...  # 0x11
        Hide: QEvent.Type = ...  # 0x12
        Close: QEvent.Type = ...  # 0x13
        Quit: QEvent.Type = ...  # 0x14
        ParentChange: QEvent.Type = ...  # 0x15
        ThreadChange: QEvent.Type = ...  # 0x16
        FocusAboutToChange: QEvent.Type = ...  # 0x17
        WindowActivate: QEvent.Type = ...  # 0x18
        WindowDeactivate: QEvent.Type = ...  # 0x19
        ShowToParent: QEvent.Type = ...  # 0x1a
        HideToParent: QEvent.Type = ...  # 0x1b
        Wheel: QEvent.Type = ...  # 0x1f
        WindowTitleChange: QEvent.Type = ...  # 0x21
        WindowIconChange: QEvent.Type = ...  # 0x22
        ApplicationWindowIconChange: QEvent.Type = ...  # 0x23
        ApplicationFontChange: QEvent.Type = ...  # 0x24
        ApplicationLayoutDirectionChange: QEvent.Type = ...  # 0x25
        ApplicationPaletteChange: QEvent.Type = ...  # 0x26
        PaletteChange: QEvent.Type = ...  # 0x27
        Clipboard: QEvent.Type = ...  # 0x28
        Speech: QEvent.Type = ...  # 0x2a
        MetaCall: QEvent.Type = ...  # 0x2b
        SockAct: QEvent.Type = ...  # 0x32
        ShortcutOverride: QEvent.Type = ...  # 0x33
        DeferredDelete: QEvent.Type = ...  # 0x34
        DragEnter: QEvent.Type = ...  # 0x3c
        DragMove: QEvent.Type = ...  # 0x3d
        DragLeave: QEvent.Type = ...  # 0x3e
        Drop: QEvent.Type = ...  # 0x3f
        DragResponse: QEvent.Type = ...  # 0x40
        ChildAdded: QEvent.Type = ...  # 0x44
        ChildPolished: QEvent.Type = ...  # 0x45
        ChildRemoved: QEvent.Type = ...  # 0x47
        ShowWindowRequest: QEvent.Type = ...  # 0x49
        PolishRequest: QEvent.Type = ...  # 0x4a
        Polish: QEvent.Type = ...  # 0x4b
        LayoutRequest: QEvent.Type = ...  # 0x4c
        UpdateRequest: QEvent.Type = ...  # 0x4d
        UpdateLater: QEvent.Type = ...  # 0x4e
        EmbeddingControl: QEvent.Type = ...  # 0x4f
        ActivateControl: QEvent.Type = ...  # 0x50
        DeactivateControl: QEvent.Type = ...  # 0x51
        ContextMenu: QEvent.Type = ...  # 0x52
        InputMethod: QEvent.Type = ...  # 0x53
        TabletMove: QEvent.Type = ...  # 0x57
        LocaleChange: QEvent.Type = ...  # 0x58
        LanguageChange: QEvent.Type = ...  # 0x59
        LayoutDirectionChange: QEvent.Type = ...  # 0x5a
        Style: QEvent.Type = ...  # 0x5b
        TabletPress: QEvent.Type = ...  # 0x5c
        TabletRelease: QEvent.Type = ...  # 0x5d
        OkRequest: QEvent.Type = ...  # 0x5e
        HelpRequest: QEvent.Type = ...  # 0x5f
        IconDrag: QEvent.Type = ...  # 0x60
        FontChange: QEvent.Type = ...  # 0x61
        EnabledChange: QEvent.Type = ...  # 0x62
        ActivationChange: QEvent.Type = ...  # 0x63
        StyleChange: QEvent.Type = ...  # 0x64
        IconTextChange: QEvent.Type = ...  # 0x65
        ModifiedChange: QEvent.Type = ...  # 0x66
        WindowBlocked: QEvent.Type = ...  # 0x67
        WindowUnblocked: QEvent.Type = ...  # 0x68
        WindowStateChange: QEvent.Type = ...  # 0x69
        ReadOnlyChange: QEvent.Type = ...  # 0x6a
        MouseTrackingChange: QEvent.Type = ...  # 0x6d
        ToolTip: QEvent.Type = ...  # 0x6e
        WhatsThis: QEvent.Type = ...  # 0x6f
        StatusTip: QEvent.Type = ...  # 0x70
        ActionChanged: QEvent.Type = ...  # 0x71
        ActionAdded: QEvent.Type = ...  # 0x72
        ActionRemoved: QEvent.Type = ...  # 0x73
        FileOpen: QEvent.Type = ...  # 0x74
        Shortcut: QEvent.Type = ...  # 0x75
        WhatsThisClicked: QEvent.Type = ...  # 0x76
        ToolBarChange: QEvent.Type = ...  # 0x78
        ApplicationActivate: QEvent.Type = ...  # 0x79
        ApplicationActivated: QEvent.Type = ...  # 0x79
        ApplicationDeactivate: QEvent.Type = ...  # 0x7a
        ApplicationDeactivated: QEvent.Type = ...  # 0x7a
        QueryWhatsThis: QEvent.Type = ...  # 0x7b
        EnterWhatsThisMode: QEvent.Type = ...  # 0x7c
        LeaveWhatsThisMode: QEvent.Type = ...  # 0x7d
        ZOrderChange: QEvent.Type = ...  # 0x7e
        HoverEnter: QEvent.Type = ...  # 0x7f
        HoverLeave: QEvent.Type = ...  # 0x80
        HoverMove: QEvent.Type = ...  # 0x81
        ParentAboutToChange: QEvent.Type = ...  # 0x83
        WinEventAct: QEvent.Type = ...  # 0x84
        AcceptDropsChange: QEvent.Type = ...  # 0x98
        ZeroTimerEvent: QEvent.Type = ...  # 0x9a
        GraphicsSceneMouseMove: QEvent.Type = ...  # 0x9b
        GraphicsSceneMousePress: QEvent.Type = ...  # 0x9c
        GraphicsSceneMouseRelease: QEvent.Type = ...  # 0x9d
        GraphicsSceneMouseDoubleClick: QEvent.Type = ...  # 0x9e
        GraphicsSceneContextMenu: QEvent.Type = ...  # 0x9f
        GraphicsSceneHoverEnter: QEvent.Type = ...  # 0xa0
        GraphicsSceneHoverMove: QEvent.Type = ...  # 0xa1
        GraphicsSceneHoverLeave: QEvent.Type = ...  # 0xa2
        GraphicsSceneHelp: QEvent.Type = ...  # 0xa3
        GraphicsSceneDragEnter: QEvent.Type = ...  # 0xa4
        GraphicsSceneDragMove: QEvent.Type = ...  # 0xa5
        GraphicsSceneDragLeave: QEvent.Type = ...  # 0xa6
        GraphicsSceneDrop: QEvent.Type = ...  # 0xa7
        GraphicsSceneWheel: QEvent.Type = ...  # 0xa8
        KeyboardLayoutChange: QEvent.Type = ...  # 0xa9
        DynamicPropertyChange: QEvent.Type = ...  # 0xaa
        TabletEnterProximity: QEvent.Type = ...  # 0xab
        TabletLeaveProximity: QEvent.Type = ...  # 0xac
        NonClientAreaMouseMove: QEvent.Type = ...  # 0xad
        NonClientAreaMouseButtonPress: QEvent.Type = ...  # 0xae
        NonClientAreaMouseButtonRelease: QEvent.Type = ...  # 0xaf
        NonClientAreaMouseButtonDblClick: QEvent.Type = ...  # 0xb0
        MacSizeChange: QEvent.Type = ...  # 0xb1
        ContentsRectChange: QEvent.Type = ...  # 0xb2
        MacGLWindowChange: QEvent.Type = ...  # 0xb3
        FutureCallOut: QEvent.Type = ...  # 0xb4
        GraphicsSceneResize: QEvent.Type = ...  # 0xb5
        GraphicsSceneMove: QEvent.Type = ...  # 0xb6
        CursorChange: QEvent.Type = ...  # 0xb7
        ToolTipChange: QEvent.Type = ...  # 0xb8
        NetworkReplyUpdated: QEvent.Type = ...  # 0xb9
        GrabMouse: QEvent.Type = ...  # 0xba
        UngrabMouse: QEvent.Type = ...  # 0xbb
        GrabKeyboard: QEvent.Type = ...  # 0xbc
        UngrabKeyboard: QEvent.Type = ...  # 0xbd
        StateMachineSignal: QEvent.Type = ...  # 0xc0
        StateMachineWrapped: QEvent.Type = ...  # 0xc1
        TouchBegin: QEvent.Type = ...  # 0xc2
        TouchUpdate: QEvent.Type = ...  # 0xc3
        TouchEnd: QEvent.Type = ...  # 0xc4
        NativeGesture: QEvent.Type = ...  # 0xc5
        Gesture: QEvent.Type = ...  # 0xc6
        RequestSoftwareInputPanel: QEvent.Type = ...  # 0xc7
        CloseSoftwareInputPanel: QEvent.Type = ...  # 0xc8
        GestureOverride: QEvent.Type = ...  # 0xca
        WinIdChange: QEvent.Type = ...  # 0xcb
        ScrollPrepare: QEvent.Type = ...  # 0xcc
        Scroll: QEvent.Type = ...  # 0xcd
        Expose: QEvent.Type = ...  # 0xce
        InputMethodQuery: QEvent.Type = ...  # 0xcf
        OrientationChange: QEvent.Type = ...  # 0xd0
        TouchCancel: QEvent.Type = ...  # 0xd1
        ThemeChange: QEvent.Type = ...  # 0xd2
        SockClose: QEvent.Type = ...  # 0xd3
        PlatformPanel: QEvent.Type = ...  # 0xd4
        StyleAnimationUpdate: QEvent.Type = ...  # 0xd5
        ApplicationStateChange: QEvent.Type = ...  # 0xd6
        WindowChangeInternal: QEvent.Type = ...  # 0xd7
        ScreenChangeInternal: QEvent.Type = ...  # 0xd8
        PlatformSurface: QEvent.Type = ...  # 0xd9
        Pointer: QEvent.Type = ...  # 0xda
        TabletTrackingChange: QEvent.Type = ...  # 0xdb
        GraphicsSceneLeave: QEvent.Type = ...  # 0xdc
        User: QEvent.Type = ...  # 0x3e8
        MaxUser: QEvent.Type = ...  # 0xffff
    @overload
    def __init__(self, arg__1: QEvent) -> None: ...
    @overload
    def __init__(self, type: QEvent.Type) -> None: ...
    def accept(self) -> None: ...
    def clone(self) -> QEvent: ...
    def ignore(self) -> None: ...
    def isAccepted(self) -> bool: ...
    def isInputEvent(self) -> bool: ...
    def isPointerEvent(self) -> bool: ...
    def isSinglePointEvent(self) -> bool: ...
    @staticmethod
    def registerEventType(hint: int = ...) -> int: ...
    def setAccepted(self, accepted: bool) -> None: ...
    def spontaneous(self) -> bool: ...
    def type(self) -> QEvent.Type: ...

class QEventLoop(QObject):

    AllEvents: QEventLoop.ProcessEventsFlag = ...  # 0x0
    ExcludeUserInputEvents: QEventLoop.ProcessEventsFlag = ...  # 0x1
    ExcludeSocketNotifiers: QEventLoop.ProcessEventsFlag = ...  # 0x2
    WaitForMoreEvents: QEventLoop.ProcessEventsFlag = ...  # 0x4
    X11ExcludeTimers: QEventLoop.ProcessEventsFlag = ...  # 0x8
    EventLoopExec: QEventLoop.ProcessEventsFlag = ...  # 0x20
    DialogExec: QEventLoop.ProcessEventsFlag = ...  # 0x40
    class ProcessEventsFlag(Enum):

        AllEvents: QEventLoop.ProcessEventsFlag = ...  # 0x0
        ExcludeUserInputEvents: QEventLoop.ProcessEventsFlag = ...  # 0x1
        ExcludeSocketNotifiers: QEventLoop.ProcessEventsFlag = ...  # 0x2
        WaitForMoreEvents: QEventLoop.ProcessEventsFlag = ...  # 0x4
        X11ExcludeTimers: QEventLoop.ProcessEventsFlag = ...  # 0x8
        EventLoopExec: QEventLoop.ProcessEventsFlag = ...  # 0x20
        DialogExec: QEventLoop.ProcessEventsFlag = ...  # 0x40
    class ProcessEventsFlags(object): ...
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def event(self, event: QEvent) -> bool: ...
    def exec(self, flags: QEventLoop.ProcessEventsFlags = ...) -> int: ...
    def exec_(self, flags: QEventLoop.ProcessEventsFlags = ...) -> int: ...
    def exit(self, returnCode: int = ...) -> None: ...
    def isRunning(self) -> bool: ...
    @overload
    def processEvents(self, flags: QEventLoop.ProcessEventsFlags, maximumTime: int) -> None: ...
    @overload
    def processEvents(self, flags: QEventLoop.ProcessEventsFlags = ...) -> bool: ...
    def quit(self) -> None: ...
    def wakeUp(self) -> None: ...

class QFactoryInterface(Shiboken.Object):
    def __init__(self) -> None: ...
    def keys(self) -> List[str]: ...

class QFile(QFileDevice):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, name: Union[str, bytes, os.PathLike]) -> None: ...
    @overload
    def __init__(self, name: Union[str, bytes, os.PathLike], parent: QObject) -> None: ...
    @overload
    def __init__(self, parent: QObject) -> None: ...
    @overload
    @staticmethod
    def copy(fileName: str, newName: str) -> bool: ...
    @overload
    def copy(self, newName: Union[str, bytes, os.PathLike]) -> bool: ...
    @overload
    @staticmethod
    def decodeName(localFileName: bytes) -> str: ...
    @overload
    @staticmethod
    def decodeName(localFileName: Union[QByteArray, bytes]) -> str: ...
    @staticmethod
    def encodeName(fileName: str) -> QByteArray: ...
    @overload
    @staticmethod
    def exists(fileName: str) -> bool: ...
    @overload
    def exists(self) -> bool: ...
    def fileName(self) -> str: ...
    @overload
    @staticmethod
    def link(oldname: str, newName: str) -> bool: ...
    @overload
    def link(self, newName: Union[str, bytes, os.PathLike]) -> bool: ...
    @overload
    @staticmethod
    def moveToTrash(fileName: str) -> Tuple[bool, str]: ...
    @overload
    def moveToTrash(self) -> bool: ...
    @overload
    def open(
        self,
        fd: int,
        ioFlags: QIODeviceBase.OpenMode,
        handleFlags: QFileDevice.FileHandleFlags = ...,
    ) -> bool: ...
    @overload
    def open(self, flags: QIODeviceBase.OpenMode) -> bool: ...
    @overload
    @staticmethod
    def permissions(filename: Union[str, bytes, os.PathLike]) -> QFileDevice.Permissions: ...
    @overload
    def permissions(self) -> QFileDevice.Permissions: ...
    @overload
    @staticmethod
    def remove(fileName: str) -> bool: ...
    @overload
    def remove(self) -> bool: ...
    @overload
    @staticmethod
    def rename(oldName: str, newName: str) -> bool: ...
    @overload
    def rename(self, newName: Union[str, bytes, os.PathLike]) -> bool: ...
    @overload
    @staticmethod
    def resize(filename: str, sz: int) -> bool: ...
    @overload
    def resize(self, sz: int) -> bool: ...
    def setFileName(self, name: Union[str, bytes, os.PathLike]) -> None: ...
    @overload
    @staticmethod
    def setPermissions(
        filename: Union[str, bytes, os.PathLike], permissionSpec: QFileDevice.Permissions
    ) -> bool: ...
    @overload
    def setPermissions(self, permissionSpec: QFileDevice.Permissions) -> bool: ...
    def size(self) -> int: ...
    @overload
    @staticmethod
    def symLinkTarget(fileName: str) -> str: ...
    @overload
    def symLinkTarget(self) -> str: ...

class QFileDevice(QIODevice):

    NoError: QFileDevice.FileError = ...  # 0x0
    ReadError: QFileDevice.FileError = ...  # 0x1
    WriteError: QFileDevice.FileError = ...  # 0x2
    FatalError: QFileDevice.FileError = ...  # 0x3
    ResourceError: QFileDevice.FileError = ...  # 0x4
    OpenError: QFileDevice.FileError = ...  # 0x5
    AbortError: QFileDevice.FileError = ...  # 0x6
    TimeOutError: QFileDevice.FileError = ...  # 0x7
    UnspecifiedError: QFileDevice.FileError = ...  # 0x8
    RemoveError: QFileDevice.FileError = ...  # 0x9
    RenameError: QFileDevice.FileError = ...  # 0xa
    PositionError: QFileDevice.FileError = ...  # 0xb
    ResizeError: QFileDevice.FileError = ...  # 0xc
    PermissionsError: QFileDevice.FileError = ...  # 0xd
    CopyError: QFileDevice.FileError = ...  # 0xe
    DontCloseHandle: QFileDevice.FileHandleFlag = ...  # 0x0
    AutoCloseHandle: QFileDevice.FileHandleFlag = ...  # 0x1
    FileAccessTime: QFileDevice.FileTime = ...  # 0x0
    FileBirthTime: QFileDevice.FileTime = ...  # 0x1
    FileMetadataChangeTime: QFileDevice.FileTime = ...  # 0x2
    FileModificationTime: QFileDevice.FileTime = ...  # 0x3
    NoOptions: QFileDevice.MemoryMapFlag = ...  # 0x0
    MapPrivateOption: QFileDevice.MemoryMapFlag = ...  # 0x1
    ExeOther: QFileDevice.Permission = ...  # 0x1
    WriteOther: QFileDevice.Permission = ...  # 0x2
    ReadOther: QFileDevice.Permission = ...  # 0x4
    ExeGroup: QFileDevice.Permission = ...  # 0x10
    WriteGroup: QFileDevice.Permission = ...  # 0x20
    ReadGroup: QFileDevice.Permission = ...  # 0x40
    ExeUser: QFileDevice.Permission = ...  # 0x100
    WriteUser: QFileDevice.Permission = ...  # 0x200
    ReadUser: QFileDevice.Permission = ...  # 0x400
    ExeOwner: QFileDevice.Permission = ...  # 0x1000
    WriteOwner: QFileDevice.Permission = ...  # 0x2000
    ReadOwner: QFileDevice.Permission = ...  # 0x4000
    class FileError(Enum):

        NoError: QFileDevice.FileError = ...  # 0x0
        ReadError: QFileDevice.FileError = ...  # 0x1
        WriteError: QFileDevice.FileError = ...  # 0x2
        FatalError: QFileDevice.FileError = ...  # 0x3
        ResourceError: QFileDevice.FileError = ...  # 0x4
        OpenError: QFileDevice.FileError = ...  # 0x5
        AbortError: QFileDevice.FileError = ...  # 0x6
        TimeOutError: QFileDevice.FileError = ...  # 0x7
        UnspecifiedError: QFileDevice.FileError = ...  # 0x8
        RemoveError: QFileDevice.FileError = ...  # 0x9
        RenameError: QFileDevice.FileError = ...  # 0xa
        PositionError: QFileDevice.FileError = ...  # 0xb
        ResizeError: QFileDevice.FileError = ...  # 0xc
        PermissionsError: QFileDevice.FileError = ...  # 0xd
        CopyError: QFileDevice.FileError = ...  # 0xe
    class FileHandleFlag(Enum):

        DontCloseHandle: QFileDevice.FileHandleFlag = ...  # 0x0
        AutoCloseHandle: QFileDevice.FileHandleFlag = ...  # 0x1
    class FileHandleFlags(object): ...
    class FileTime(Enum):

        FileAccessTime: QFileDevice.FileTime = ...  # 0x0
        FileBirthTime: QFileDevice.FileTime = ...  # 0x1
        FileMetadataChangeTime: QFileDevice.FileTime = ...  # 0x2
        FileModificationTime: QFileDevice.FileTime = ...  # 0x3
    class MemoryMapFlag(Enum):

        NoOptions: QFileDevice.MemoryMapFlag = ...  # 0x0
        MapPrivateOption: QFileDevice.MemoryMapFlag = ...  # 0x1
    class MemoryMapFlags(object): ...
    class Permission(Enum):

        ExeOther: QFileDevice.Permission = ...  # 0x1
        WriteOther: QFileDevice.Permission = ...  # 0x2
        ReadOther: QFileDevice.Permission = ...  # 0x4
        ExeGroup: QFileDevice.Permission = ...  # 0x10
        WriteGroup: QFileDevice.Permission = ...  # 0x20
        ReadGroup: QFileDevice.Permission = ...  # 0x40
        ExeUser: QFileDevice.Permission = ...  # 0x100
        WriteUser: QFileDevice.Permission = ...  # 0x200
        ReadUser: QFileDevice.Permission = ...  # 0x400
        ExeOwner: QFileDevice.Permission = ...  # 0x1000
        WriteOwner: QFileDevice.Permission = ...  # 0x2000
        ReadOwner: QFileDevice.Permission = ...  # 0x4000
    class Permissions(object): ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, parent: QObject) -> None: ...
    def atEnd(self) -> bool: ...
    def close(self) -> None: ...
    def error(self) -> QFileDevice.FileError: ...
    def fileName(self) -> str: ...
    def fileTime(self, time: QFileDevice.FileTime) -> QDateTime: ...
    def flush(self) -> bool: ...
    def handle(self) -> int: ...
    def isSequential(self) -> bool: ...
    def map(self, offset: int, size: int, flags: QFileDevice.MemoryMapFlags = ...) -> object: ...
    def permissions(self) -> QFileDevice.Permissions: ...
    def pos(self) -> int: ...
    def readData(self, data: bytes, maxlen: int) -> object: ...
    def readLineData(self, data: bytes, maxlen: int) -> object: ...
    def resize(self, sz: int) -> bool: ...
    def seek(self, offset: int) -> bool: ...
    def setFileTime(self, newDate: QDateTime, fileTime: QFileDevice.FileTime) -> bool: ...
    def setPermissions(self, permissionSpec: QFileDevice.Permissions) -> bool: ...
    def size(self) -> int: ...
    def unmap(self, address: bytes) -> bool: ...
    def unsetError(self) -> None: ...
    def writeData(self, data: bytes, len: int) -> int: ...

class QFileInfo(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, dir: Union[QDir, str], file: Union[str, bytes, os.PathLike]) -> None: ...
    @overload
    def __init__(self, file: Union[str, bytes, os.PathLike]) -> None: ...
    @overload
    def __init__(self, file: QFileDevice) -> None: ...
    @overload
    def __init__(self, fileinfo: QFileInfo) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def absoluteDir(self) -> QDir: ...
    def absoluteFilePath(self) -> str: ...
    def absolutePath(self) -> str: ...
    def baseName(self) -> str: ...
    def birthTime(self) -> QDateTime: ...
    def bundleName(self) -> str: ...
    def caching(self) -> bool: ...
    def canonicalFilePath(self) -> str: ...
    def canonicalPath(self) -> str: ...
    def completeBaseName(self) -> str: ...
    def completeSuffix(self) -> str: ...
    def dir(self) -> QDir: ...
    @overload
    @staticmethod
    def exists(file: str) -> bool: ...
    @overload
    def exists(self) -> bool: ...
    def fileName(self) -> str: ...
    def filePath(self) -> str: ...
    def group(self) -> str: ...
    def groupId(self) -> int: ...
    def isAbsolute(self) -> bool: ...
    def isBundle(self) -> bool: ...
    def isDir(self) -> bool: ...
    def isExecutable(self) -> bool: ...
    def isFile(self) -> bool: ...
    def isHidden(self) -> bool: ...
    def isJunction(self) -> bool: ...
    def isNativePath(self) -> bool: ...
    def isReadable(self) -> bool: ...
    def isRelative(self) -> bool: ...
    def isRoot(self) -> bool: ...
    def isShortcut(self) -> bool: ...
    def isSymLink(self) -> bool: ...
    def isSymbolicLink(self) -> bool: ...
    def isWritable(self) -> bool: ...
    def junctionTarget(self) -> str: ...
    def lastModified(self) -> QDateTime: ...
    def lastRead(self) -> QDateTime: ...
    def makeAbsolute(self) -> bool: ...
    def metadataChangeTime(self) -> QDateTime: ...
    def owner(self) -> str: ...
    def ownerId(self) -> int: ...
    def path(self) -> str: ...
    def refresh(self) -> None: ...
    def setCaching(self, on: bool) -> None: ...
    @overload
    def setFile(self, dir: Union[QDir, str], file: str) -> None: ...
    @overload
    def setFile(self, file: Union[str, bytes, os.PathLike]) -> None: ...
    @overload
    def setFile(self, file: QFileDevice) -> None: ...
    def size(self) -> int: ...
    def stat(self) -> None: ...
    def suffix(self) -> str: ...
    def swap(self, other: QFileInfo) -> None: ...
    def symLinkTarget(self) -> str: ...

class QFileSelector(QObject):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def allSelectors(self) -> List[str]: ...
    def extraSelectors(self) -> List[str]: ...
    @overload
    def select(self, filePath: str) -> str: ...
    @overload
    def select(self, filePath: Union[QUrl, str]) -> QUrl: ...
    def setExtraSelectors(self, list: Sequence[str]) -> None: ...

class QFileSystemWatcher(QObject):
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, paths: Sequence[str], parent: Optional[QObject] = ...) -> None: ...
    def addPath(self, file: str) -> bool: ...
    def addPaths(self, files: Sequence[str]) -> List[str]: ...
    def directories(self) -> List[str]: ...
    def files(self) -> List[str]: ...
    def removePath(self, file: str) -> bool: ...
    def removePaths(self, files: Sequence[str]) -> List[str]: ...

class QFutureInterfaceBase(Shiboken.Object):

    NoState: QFutureInterfaceBase.State = ...  # 0x0
    Running: QFutureInterfaceBase.State = ...  # 0x1
    Started: QFutureInterfaceBase.State = ...  # 0x2
    Finished: QFutureInterfaceBase.State = ...  # 0x4
    Canceled: QFutureInterfaceBase.State = ...  # 0x8
    Suspending: QFutureInterfaceBase.State = ...  # 0x10
    Suspended: QFutureInterfaceBase.State = ...  # 0x20
    Throttled: QFutureInterfaceBase.State = ...  # 0x40
    Pending: QFutureInterfaceBase.State = ...  # 0x80
    class State(Enum):

        NoState: QFutureInterfaceBase.State = ...  # 0x0
        Running: QFutureInterfaceBase.State = ...  # 0x1
        Started: QFutureInterfaceBase.State = ...  # 0x2
        Finished: QFutureInterfaceBase.State = ...  # 0x4
        Canceled: QFutureInterfaceBase.State = ...  # 0x8
        Suspending: QFutureInterfaceBase.State = ...  # 0x10
        Suspended: QFutureInterfaceBase.State = ...  # 0x20
        Throttled: QFutureInterfaceBase.State = ...  # 0x40
        Pending: QFutureInterfaceBase.State = ...  # 0x80
    @overload
    def __init__(self, initialState: QFutureInterfaceBase.State = ...) -> None: ...
    @overload
    def __init__(self, other: QFutureInterfaceBase) -> None: ...
    def cancel(self) -> None: ...
    def derefT(self) -> bool: ...
    def expectedResultCount(self) -> int: ...
    def isCanceled(self) -> bool: ...
    def isFinished(self) -> bool: ...
    def isPaused(self) -> bool: ...
    def isProgressUpdateNeeded(self) -> bool: ...
    def isResultReadyAt(self, index: int) -> bool: ...
    def isRunning(self) -> bool: ...
    def isRunningOrPending(self) -> bool: ...
    def isStarted(self) -> bool: ...
    def isSuspended(self) -> bool: ...
    def isSuspending(self) -> bool: ...
    def isThrottled(self) -> bool: ...
    def isValid(self) -> bool: ...
    def launchAsync(self) -> bool: ...
    def loadState(self) -> int: ...
    def mutex(self) -> QMutex: ...
    def progressMaximum(self) -> int: ...
    def progressMinimum(self) -> int: ...
    def progressText(self) -> str: ...
    def progressValue(self) -> int: ...
    def queryState(self, state: QFutureInterfaceBase.State) -> bool: ...
    def refT(self) -> bool: ...
    def reportCanceled(self) -> None: ...
    def reportFinished(self) -> None: ...
    def reportResultsReady(self, beginIndex: int, endIndex: int) -> None: ...
    def reportStarted(self) -> None: ...
    def reportSuspended(self) -> None: ...
    def reset(self) -> None: ...
    def resultCount(self) -> int: ...
    def rethrowPossibleException(self) -> None: ...
    def runContinuation(self) -> None: ...
    def setExpectedResultCount(self, resultCount: int) -> None: ...
    def setFilterMode(self, enable: bool) -> None: ...
    def setLaunchAsync(self, value: bool) -> None: ...
    def setPaused(self, paused: bool) -> None: ...
    def setProgressRange(self, minimum: int, maximum: int) -> None: ...
    def setProgressValue(self, progressValue: int) -> None: ...
    def setProgressValueAndText(self, progressValue: int, progressText: str) -> None: ...
    def setRunnable(self, runnable: QRunnable) -> None: ...
    def setSuspended(self, suspend: bool) -> None: ...
    def setThreadPool(self, pool: QThreadPool) -> None: ...
    def setThrottled(self, enable: bool) -> None: ...
    def suspendIfRequested(self) -> None: ...
    def swap(self, other: QFutureInterfaceBase) -> None: ...
    def threadPool(self) -> QThreadPool: ...
    def togglePaused(self) -> None: ...
    def toggleSuspended(self) -> None: ...
    def waitForFinished(self) -> None: ...
    def waitForNextResult(self) -> bool: ...
    def waitForResult(self, resultIndex: int) -> None: ...
    def waitForResume(self) -> None: ...

class QGenericArgument(Shiboken.Object):
    @overload
    def __init__(self, QGenericArgument: QGenericArgument) -> None: ...
    @overload
    def __init__(self, aName: Optional[bytes] = ..., aData: Optional[int] = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def data(self) -> int: ...
    def name(self) -> bytes: ...

class QGenericReturnArgument(QGenericArgument):
    @overload
    def __init__(self, QGenericReturnArgument: QGenericReturnArgument) -> None: ...
    @overload
    def __init__(self, aName: Optional[bytes] = ..., aData: Optional[int] = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...

class QIODevice(QObject, QIODeviceBase):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, parent: QObject) -> None: ...
    def atEnd(self) -> bool: ...
    def bytesAvailable(self) -> int: ...
    def bytesToWrite(self) -> int: ...
    def canReadLine(self) -> bool: ...
    def close(self) -> None: ...
    def commitTransaction(self) -> None: ...
    def currentReadChannel(self) -> int: ...
    def currentWriteChannel(self) -> int: ...
    def errorString(self) -> str: ...
    def getChar(self, c: bytes) -> bool: ...
    def isOpen(self) -> bool: ...
    def isReadable(self) -> bool: ...
    def isSequential(self) -> bool: ...
    def isTextModeEnabled(self) -> bool: ...
    def isTransactionStarted(self) -> bool: ...
    def isWritable(self) -> bool: ...
    def open(self, mode: QIODeviceBase.OpenMode) -> bool: ...
    def openMode(self) -> QIODeviceBase.OpenMode: ...
    def peek(self, maxlen: int) -> QByteArray: ...
    def pos(self) -> int: ...
    def putChar(self, c: int) -> bool: ...
    def read(self, maxlen: int) -> QByteArray: ...
    def readAll(self) -> QByteArray: ...
    def readChannelCount(self) -> int: ...
    def readData(self, data: bytes, maxlen: int) -> object: ...
    def readLine(self, maxlen: int = ...) -> QByteArray: ...
    def readLineData(self, data: bytes, maxlen: int) -> object: ...
    def reset(self) -> bool: ...
    def rollbackTransaction(self) -> None: ...
    def seek(self, pos: int) -> bool: ...
    def setCurrentReadChannel(self, channel: int) -> None: ...
    def setCurrentWriteChannel(self, channel: int) -> None: ...
    def setErrorString(self, errorString: str) -> None: ...
    def setOpenMode(self, openMode: QIODeviceBase.OpenMode) -> None: ...
    def setTextModeEnabled(self, enabled: bool) -> None: ...
    def size(self) -> int: ...
    def skip(self, maxSize: int) -> int: ...
    def skipData(self, maxSize: int) -> int: ...
    def startTransaction(self) -> None: ...
    def ungetChar(self, c: int) -> None: ...
    def waitForBytesWritten(self, msecs: int) -> bool: ...
    def waitForReadyRead(self, msecs: int) -> bool: ...
    def write(self, data: Union[QByteArray, bytes]) -> int: ...
    def writeChannelCount(self) -> int: ...
    def writeData(self, data: bytes, len: int) -> int: ...

class QIODeviceBase(Shiboken.Object):

    NotOpen: QIODeviceBase.OpenModeFlag = ...  # 0x0
    ReadOnly: QIODeviceBase.OpenModeFlag = ...  # 0x1
    WriteOnly: QIODeviceBase.OpenModeFlag = ...  # 0x2
    ReadWrite: QIODeviceBase.OpenModeFlag = ...  # 0x3
    Append: QIODeviceBase.OpenModeFlag = ...  # 0x4
    Truncate: QIODeviceBase.OpenModeFlag = ...  # 0x8
    Text: QIODeviceBase.OpenModeFlag = ...  # 0x10
    Unbuffered: QIODeviceBase.OpenModeFlag = ...  # 0x20
    NewOnly: QIODeviceBase.OpenModeFlag = ...  # 0x40
    ExistingOnly: QIODeviceBase.OpenModeFlag = ...  # 0x80
    class OpenMode(object): ...
    class OpenModeFlag(Enum):

        NotOpen: QIODeviceBase.OpenModeFlag = ...  # 0x0
        ReadOnly: QIODeviceBase.OpenModeFlag = ...  # 0x1
        WriteOnly: QIODeviceBase.OpenModeFlag = ...  # 0x2
        ReadWrite: QIODeviceBase.OpenModeFlag = ...  # 0x3
        Append: QIODeviceBase.OpenModeFlag = ...  # 0x4
        Truncate: QIODeviceBase.OpenModeFlag = ...  # 0x8
        Text: QIODeviceBase.OpenModeFlag = ...  # 0x10
        Unbuffered: QIODeviceBase.OpenModeFlag = ...  # 0x20
        NewOnly: QIODeviceBase.OpenModeFlag = ...  # 0x40
        ExistingOnly: QIODeviceBase.OpenModeFlag = ...  # 0x80
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QIODeviceBase: QIODeviceBase) -> None: ...
    @staticmethod
    def __copy__() -> None: ...

class QIdentityProxyModel(QAbstractProxyModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    def insertColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def mapFromSource(
        self, sourceIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def mapSelectionFromSource(self, selection: QItemSelection) -> QItemSelection: ...
    def mapSelectionToSource(self, selection: QItemSelection) -> QItemSelection: ...
    def mapToSource(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def match(
        self,
        start: Union[QModelIndex, QPersistentModelIndex],
        role: int,
        value: Any,
        hits: int = ...,
        flags: Qt.MatchFlags = ...,
    ) -> List[int]: ...
    def moveColumns(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceColumn: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def moveRows(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceRow: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, child: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def removeColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setSourceModel(self, sourceModel: QAbstractItemModel) -> None: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...

class QIntList(object): ...

class QItemSelection(Shiboken.Object):
    @overload
    def __init__(self) -> QItemSelection: ...
    @overload
    def __init__(self, QItemSelection: QItemSelection) -> None: ...
    @overload
    def __init__(
        self,
        topLeft: Union[QModelIndex, QPersistentModelIndex],
        bottomRight: Union[QModelIndex, QPersistentModelIndex],
    ) -> None: ...
    def __add__(self, arg__1: QItemSelection) -> QItemSelection: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, l: Sequence[QItemSelectionRange]) -> List[QItemSelectionRange]: ...
    def __lshift__(self, l: Sequence[QItemSelectionRange]) -> List[QItemSelectionRange]: ...
    @overload
    def append(self, arg__1: QItemSelectionRange) -> None: ...
    @overload
    def append(self, l: Sequence[QItemSelectionRange]) -> None: ...
    def at(self, i: int) -> QItemSelectionRange: ...
    def back(self) -> QItemSelectionRange: ...
    def capacity(self) -> int: ...
    def clear(self) -> None: ...
    def constData(self) -> QItemSelectionRange: ...
    def constFirst(self) -> QItemSelectionRange: ...
    def constLast(self) -> QItemSelectionRange: ...
    def contains(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def count(self) -> int: ...
    def data(self) -> QItemSelectionRange: ...
    def empty(self) -> bool: ...
    @overload
    def first(self) -> QItemSelectionRange: ...
    @overload
    def first(self, n: int) -> List[QItemSelectionRange]: ...
    @staticmethod
    def fromList(list: Sequence[QItemSelectionRange]) -> List[QItemSelectionRange]: ...
    @staticmethod
    def fromVector(vector: Sequence[QItemSelectionRange]) -> List[QItemSelectionRange]: ...
    def front(self) -> QItemSelectionRange: ...
    def indexes(self) -> List[int]: ...
    def insert(self, arg__1: int, arg__2: QItemSelectionRange) -> None: ...
    def isEmpty(self) -> bool: ...
    def isSharedWith(self, other: Sequence[QItemSelectionRange]) -> bool: ...
    @overload
    def last(self) -> QItemSelectionRange: ...
    @overload
    def last(self, n: int) -> List[QItemSelectionRange]: ...
    def length(self) -> int: ...
    def merge(self, other: QItemSelection, command: QItemSelectionModel.SelectionFlags) -> None: ...
    def mid(self, pos: int, len: int = ...) -> List[QItemSelectionRange]: ...
    def move(self, from_: int, to: int) -> None: ...
    def pop_back(self) -> None: ...
    def pop_front(self) -> None: ...
    def prepend(self, arg__1: QItemSelectionRange) -> None: ...
    def push_back(self, arg__1: QItemSelectionRange) -> None: ...
    def push_front(self, arg__1: QItemSelectionRange) -> None: ...
    def remove(self, i: int, n: int = ...) -> None: ...
    def removeAll(self, arg__1: QItemSelectionRange) -> None: ...
    def removeAt(self, i: int) -> None: ...
    def removeFirst(self) -> None: ...
    def removeLast(self) -> None: ...
    def removeOne(self, arg__1: QItemSelectionRange) -> None: ...
    def reserve(self, size: int) -> None: ...
    def resize(self, size: int) -> None: ...
    def select(
        self,
        topLeft: Union[QModelIndex, QPersistentModelIndex],
        bottomRight: Union[QModelIndex, QPersistentModelIndex],
    ) -> None: ...
    def shrink_to_fit(self) -> None: ...
    def size(self) -> int: ...
    @overload
    def sliced(self, pos: int) -> List[QItemSelectionRange]: ...
    @overload
    def sliced(self, pos: int, n: int) -> List[QItemSelectionRange]: ...
    @staticmethod
    def split(
        range: QItemSelectionRange, other: QItemSelectionRange, result: QItemSelection
    ) -> None: ...
    def squeeze(self) -> None: ...
    def swap(self, other: Sequence[QItemSelectionRange]) -> None: ...
    def swapItemsAt(self, i: int, j: int) -> None: ...
    def takeAt(self, i: int) -> QItemSelectionRange: ...
    def toList(self) -> List[QItemSelectionRange]: ...
    def toVector(self) -> List[QItemSelectionRange]: ...
    def value(self, i: int) -> QItemSelectionRange: ...

class QItemSelectionModel(QObject):

    NoUpdate: QItemSelectionModel.SelectionFlag = ...  # 0x0
    Clear: QItemSelectionModel.SelectionFlag = ...  # 0x1
    Select: QItemSelectionModel.SelectionFlag = ...  # 0x2
    ClearAndSelect: QItemSelectionModel.SelectionFlag = ...  # 0x3
    Deselect: QItemSelectionModel.SelectionFlag = ...  # 0x4
    Toggle: QItemSelectionModel.SelectionFlag = ...  # 0x8
    Current: QItemSelectionModel.SelectionFlag = ...  # 0x10
    SelectCurrent: QItemSelectionModel.SelectionFlag = ...  # 0x12
    ToggleCurrent: QItemSelectionModel.SelectionFlag = ...  # 0x18
    Rows: QItemSelectionModel.SelectionFlag = ...  # 0x20
    Columns: QItemSelectionModel.SelectionFlag = ...  # 0x40
    class SelectionFlag(Enum):

        NoUpdate: QItemSelectionModel.SelectionFlag = ...  # 0x0
        Clear: QItemSelectionModel.SelectionFlag = ...  # 0x1
        Select: QItemSelectionModel.SelectionFlag = ...  # 0x2
        ClearAndSelect: QItemSelectionModel.SelectionFlag = ...  # 0x3
        Deselect: QItemSelectionModel.SelectionFlag = ...  # 0x4
        Toggle: QItemSelectionModel.SelectionFlag = ...  # 0x8
        Current: QItemSelectionModel.SelectionFlag = ...  # 0x10
        SelectCurrent: QItemSelectionModel.SelectionFlag = ...  # 0x12
        ToggleCurrent: QItemSelectionModel.SelectionFlag = ...  # 0x18
        Rows: QItemSelectionModel.SelectionFlag = ...  # 0x20
        Columns: QItemSelectionModel.SelectionFlag = ...  # 0x40
    class SelectionFlags(object): ...
    @overload
    def __init__(self, model: QAbstractItemModel, parent: QObject) -> None: ...
    @overload
    def __init__(self, model: Optional[QAbstractItemModel] = ...) -> None: ...
    def clear(self) -> None: ...
    def clearCurrentIndex(self) -> None: ...
    def clearSelection(self) -> None: ...
    def columnIntersectsSelection(
        self, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def currentIndex(self) -> QModelIndex: ...
    def emitSelectionChanged(
        self, newSelection: QItemSelection, oldSelection: QItemSelection
    ) -> None: ...
    def hasSelection(self) -> bool: ...
    def isColumnSelected(
        self, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def isRowSelected(
        self, row: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def isSelected(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def model(self) -> QAbstractItemModel: ...
    def reset(self) -> None: ...
    def rowIntersectsSelection(
        self, row: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    @overload
    def select(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        command: QItemSelectionModel.SelectionFlags,
    ) -> None: ...
    @overload
    def select(
        self, selection: QItemSelection, command: QItemSelectionModel.SelectionFlags
    ) -> None: ...
    def selectedColumns(self, row: int = ...) -> List[int]: ...
    def selectedIndexes(self) -> List[int]: ...
    def selectedRows(self, column: int = ...) -> List[int]: ...
    def selection(self) -> QItemSelection: ...
    def setCurrentIndex(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        command: QItemSelectionModel.SelectionFlags,
    ) -> None: ...
    def setModel(self, model: QAbstractItemModel) -> None: ...

class QItemSelectionRange(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QItemSelectionRange: QItemSelectionRange) -> None: ...
    @overload
    def __init__(self, index: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    @overload
    def __init__(
        self,
        topL: Union[QModelIndex, QPersistentModelIndex],
        bottomR: Union[QModelIndex, QPersistentModelIndex],
    ) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def bottom(self) -> int: ...
    def bottomRight(self) -> QPersistentModelIndex: ...
    @overload
    def contains(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    @overload
    def contains(
        self, row: int, column: int, parentIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool: ...
    def height(self) -> int: ...
    def indexes(self) -> List[int]: ...
    def intersected(self, other: QItemSelectionRange) -> QItemSelectionRange: ...
    def intersects(self, other: QItemSelectionRange) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isValid(self) -> bool: ...
    def left(self) -> int: ...
    def model(self) -> QAbstractItemModel: ...
    def parent(self) -> QModelIndex: ...
    def right(self) -> int: ...
    def swap(self, other: QItemSelectionRange) -> None: ...
    def top(self) -> int: ...
    def topLeft(self) -> QPersistentModelIndex: ...
    def width(self) -> int: ...

class QJsonArray(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QJsonArray) -> None: ...
    def __add__(
        self,
        v: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> QJsonArray: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(
        self,
        v: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> QJsonArray: ...
    def __lshift__(
        self,
        v: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> QJsonArray: ...
    def append(
        self,
        value: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def at(self, i: int) -> QJsonValue: ...
    def contains(
        self,
        element: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> bool: ...
    def count(self) -> int: ...
    def empty(self) -> bool: ...
    def first(self) -> QJsonValue: ...
    @staticmethod
    def fromStringList(list: Sequence[str]) -> QJsonArray: ...
    @staticmethod
    def fromVariantList(list: Sequence[Any]) -> QJsonArray: ...
    def insert(
        self,
        i: int,
        value: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def isEmpty(self) -> bool: ...
    def last(self) -> QJsonValue: ...
    def pop_back(self) -> None: ...
    def pop_front(self) -> None: ...
    def prepend(
        self,
        value: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def push_back(
        self,
        t: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def push_front(
        self,
        t: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def removeAt(self, i: int) -> None: ...
    def removeFirst(self) -> None: ...
    def removeLast(self) -> None: ...
    def replace(
        self,
        i: int,
        value: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    def size(self) -> int: ...
    def swap(self, other: QJsonArray) -> None: ...
    def takeAt(self, i: int) -> QJsonValue: ...
    def toVariantList(self) -> List[Any]: ...

class QJsonDocument(Shiboken.Object):

    Indented: QJsonDocument.JsonFormat = ...  # 0x0
    Compact: QJsonDocument.JsonFormat = ...  # 0x1
    class JsonFormat(Enum):

        Indented: QJsonDocument.JsonFormat = ...  # 0x0
        Compact: QJsonDocument.JsonFormat = ...  # 0x1
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, array: QJsonArray) -> None: ...
    @overload
    def __init__(self, object: Dict[str, QJsonValue]) -> None: ...
    @overload
    def __init__(self, other: QJsonDocument) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def array(self) -> QJsonArray: ...
    @staticmethod
    def fromJson(
        json: Union[QByteArray, bytes], error: Optional[QJsonParseError] = ...
    ) -> QJsonDocument: ...
    @staticmethod
    def fromVariant(variant: Any) -> QJsonDocument: ...
    def isArray(self) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isObject(self) -> bool: ...
    def object(self) -> Dict[str, QJsonValue]: ...
    def setArray(self, array: QJsonArray) -> None: ...
    def setObject(self, object: Dict[str, QJsonValue]) -> None: ...
    def swap(self, other: QJsonDocument) -> None: ...
    def toJson(self, format: QJsonDocument.JsonFormat = ...) -> QByteArray: ...
    def toVariant(self) -> Any: ...

class QJsonParseError(Shiboken.Object):

    NoError: QJsonParseError.ParseError = ...  # 0x0
    UnterminatedObject: QJsonParseError.ParseError = ...  # 0x1
    MissingNameSeparator: QJsonParseError.ParseError = ...  # 0x2
    UnterminatedArray: QJsonParseError.ParseError = ...  # 0x3
    MissingValueSeparator: QJsonParseError.ParseError = ...  # 0x4
    IllegalValue: QJsonParseError.ParseError = ...  # 0x5
    TerminationByNumber: QJsonParseError.ParseError = ...  # 0x6
    IllegalNumber: QJsonParseError.ParseError = ...  # 0x7
    IllegalEscapeSequence: QJsonParseError.ParseError = ...  # 0x8
    IllegalUTF8String: QJsonParseError.ParseError = ...  # 0x9
    UnterminatedString: QJsonParseError.ParseError = ...  # 0xa
    MissingObject: QJsonParseError.ParseError = ...  # 0xb
    DeepNesting: QJsonParseError.ParseError = ...  # 0xc
    DocumentTooLarge: QJsonParseError.ParseError = ...  # 0xd
    GarbageAtEnd: QJsonParseError.ParseError = ...  # 0xe
    class ParseError(Enum):

        NoError: QJsonParseError.ParseError = ...  # 0x0
        UnterminatedObject: QJsonParseError.ParseError = ...  # 0x1
        MissingNameSeparator: QJsonParseError.ParseError = ...  # 0x2
        UnterminatedArray: QJsonParseError.ParseError = ...  # 0x3
        MissingValueSeparator: QJsonParseError.ParseError = ...  # 0x4
        IllegalValue: QJsonParseError.ParseError = ...  # 0x5
        TerminationByNumber: QJsonParseError.ParseError = ...  # 0x6
        IllegalNumber: QJsonParseError.ParseError = ...  # 0x7
        IllegalEscapeSequence: QJsonParseError.ParseError = ...  # 0x8
        IllegalUTF8String: QJsonParseError.ParseError = ...  # 0x9
        UnterminatedString: QJsonParseError.ParseError = ...  # 0xa
        MissingObject: QJsonParseError.ParseError = ...  # 0xb
        DeepNesting: QJsonParseError.ParseError = ...  # 0xc
        DocumentTooLarge: QJsonParseError.ParseError = ...  # 0xd
        GarbageAtEnd: QJsonParseError.ParseError = ...  # 0xe
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QJsonParseError: QJsonParseError) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def errorString(self) -> str: ...

class QJsonValue(Shiboken.Object):

    Null: QJsonValue.Type = ...  # 0x0
    Bool: QJsonValue.Type = ...  # 0x1
    Double: QJsonValue.Type = ...  # 0x2
    String: QJsonValue.Type = ...  # 0x3
    Array: QJsonValue.Type = ...  # 0x4
    Object: QJsonValue.Type = ...  # 0x5
    Undefined: QJsonValue.Type = ...  # 0x80
    class Type(Enum):

        Null: QJsonValue.Type = ...  # 0x0
        Bool: QJsonValue.Type = ...  # 0x1
        Double: QJsonValue.Type = ...  # 0x2
        String: QJsonValue.Type = ...  # 0x3
        Array: QJsonValue.Type = ...  # 0x4
        Object: QJsonValue.Type = ...  # 0x5
        Undefined: QJsonValue.Type = ...  # 0x80
    @overload
    def __init__(self, a: QJsonArray) -> None: ...
    @overload
    def __init__(self, arg__1: QJsonValue.Type = ...) -> None: ...
    @overload
    def __init__(self, b: bool) -> None: ...
    @overload
    def __init__(self, n: float) -> None: ...
    @overload
    def __init__(self, n: int) -> None: ...
    @overload
    def __init__(self, o: Dict[str, QJsonValue]) -> None: ...
    @overload
    def __init__(
        self,
        other: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    @overload
    def __init__(self, s: str) -> None: ...
    @overload
    def __init__(self, s: bytes) -> None: ...
    @overload
    def __init__(self, v: int) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def fromVariant(variant: Any) -> QJsonValue: ...
    def isArray(self) -> bool: ...
    def isBool(self) -> bool: ...
    def isDouble(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isObject(self) -> bool: ...
    def isString(self) -> bool: ...
    def isUndefined(self) -> bool: ...
    def swap(
        self,
        other: Union[
            QJsonValue, QJsonValue.Type, QJsonArray, Dict[str, QJsonValue], str, bytes, float, int
        ],
    ) -> None: ...
    @overload
    def toArray(self) -> QJsonArray: ...
    @overload
    def toArray(self, defaultValue: QJsonArray) -> QJsonArray: ...
    def toBool(self, defaultValue: bool = ...) -> bool: ...
    def toDouble(self, defaultValue: float = ...) -> float: ...
    def toInt(self, defaultValue: int = ...) -> int: ...
    def toInteger(self, defaultValue: int = ...) -> int: ...
    @overload
    def toObject(self) -> Dict[str, QJsonValue]: ...
    @overload
    def toObject(self, defaultValue: Dict[str, QJsonValue]) -> Dict[str, QJsonValue]: ...
    @overload
    def toString(self) -> str: ...
    @overload
    def toString(self, defaultValue: str) -> str: ...
    def toVariant(self) -> Any: ...
    def type(self) -> QJsonValue.Type: ...

class QKeyCombination(Shiboken.Object):
    @overload
    def __init__(self, key: Qt.Key = ...) -> None: ...
    @overload
    def __init__(self, modifiers: Qt.KeyboardModifiers, key: Qt.Key = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def fromCombined(combined: int) -> QKeyCombination: ...
    def key(self) -> Qt.Key: ...
    def keyboardModifiers(self) -> Qt.KeyboardModifiers: ...
    def toCombined(self) -> int: ...

class QLibrary(QObject):

    ResolveAllSymbolsHint: QLibrary.LoadHint = ...  # 0x1
    ExportExternalSymbolsHint: QLibrary.LoadHint = ...  # 0x2
    LoadArchiveMemberHint: QLibrary.LoadHint = ...  # 0x4
    PreventUnloadHint: QLibrary.LoadHint = ...  # 0x8
    DeepBindHint: QLibrary.LoadHint = ...  # 0x10
    class LoadHint(Enum):

        ResolveAllSymbolsHint: QLibrary.LoadHint = ...  # 0x1
        ExportExternalSymbolsHint: QLibrary.LoadHint = ...  # 0x2
        LoadArchiveMemberHint: QLibrary.LoadHint = ...  # 0x4
        PreventUnloadHint: QLibrary.LoadHint = ...  # 0x8
        DeepBindHint: QLibrary.LoadHint = ...  # 0x10
    class LoadHints(object): ...
    @overload
    def __init__(self, fileName: str, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, fileName: str, verNum: int, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, fileName: str, version: str, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def errorString(self) -> str: ...
    def fileName(self) -> str: ...
    @staticmethod
    def isLibrary(fileName: str) -> bool: ...
    def isLoaded(self) -> bool: ...
    def load(self) -> bool: ...
    def loadHints(self) -> QLibrary.LoadHints: ...
    def setFileName(self, fileName: str) -> None: ...
    @overload
    def setFileNameAndVersion(self, fileName: str, verNum: int) -> None: ...
    @overload
    def setFileNameAndVersion(self, fileName: str, version: str) -> None: ...
    def setLoadHints(self, hints: QLibrary.LoadHints) -> None: ...
    def unload(self) -> bool: ...

class QLibraryInfo(Shiboken.Object):

    PrefixPath: QLibraryInfo.LibraryPath = ...  # 0x0
    DocumentationPath: QLibraryInfo.LibraryPath = ...  # 0x1
    HeadersPath: QLibraryInfo.LibraryPath = ...  # 0x2
    LibrariesPath: QLibraryInfo.LibraryPath = ...  # 0x3
    LibraryExecutablesPath: QLibraryInfo.LibraryPath = ...  # 0x4
    BinariesPath: QLibraryInfo.LibraryPath = ...  # 0x5
    PluginsPath: QLibraryInfo.LibraryPath = ...  # 0x6
    Qml2ImportsPath: QLibraryInfo.LibraryPath = ...  # 0x7
    QmlImportsPath: QLibraryInfo.LibraryPath = ...  # 0x7
    ArchDataPath: QLibraryInfo.LibraryPath = ...  # 0x8
    DataPath: QLibraryInfo.LibraryPath = ...  # 0x9
    TranslationsPath: QLibraryInfo.LibraryPath = ...  # 0xa
    ExamplesPath: QLibraryInfo.LibraryPath = ...  # 0xb
    TestsPath: QLibraryInfo.LibraryPath = ...  # 0xc
    SettingsPath: QLibraryInfo.LibraryPath = ...  # 0x64
    class LibraryPath(Enum):

        PrefixPath: QLibraryInfo.LibraryPath = ...  # 0x0
        DocumentationPath: QLibraryInfo.LibraryPath = ...  # 0x1
        HeadersPath: QLibraryInfo.LibraryPath = ...  # 0x2
        LibrariesPath: QLibraryInfo.LibraryPath = ...  # 0x3
        LibraryExecutablesPath: QLibraryInfo.LibraryPath = ...  # 0x4
        BinariesPath: QLibraryInfo.LibraryPath = ...  # 0x5
        PluginsPath: QLibraryInfo.LibraryPath = ...  # 0x6
        Qml2ImportsPath: QLibraryInfo.LibraryPath = ...  # 0x7
        QmlImportsPath: QLibraryInfo.LibraryPath = ...  # 0x7
        ArchDataPath: QLibraryInfo.LibraryPath = ...  # 0x8
        DataPath: QLibraryInfo.LibraryPath = ...  # 0x9
        TranslationsPath: QLibraryInfo.LibraryPath = ...  # 0xa
        ExamplesPath: QLibraryInfo.LibraryPath = ...  # 0xb
        TestsPath: QLibraryInfo.LibraryPath = ...  # 0xc
        SettingsPath: QLibraryInfo.LibraryPath = ...  # 0x64
    @staticmethod
    def build() -> bytes: ...
    @staticmethod
    def isDebugBuild() -> bool: ...
    @staticmethod
    def location(location: QLibraryInfo.LibraryPath) -> str: ...
    @staticmethod
    def path(p: QLibraryInfo.LibraryPath) -> str: ...
    @staticmethod
    def platformPluginArguments(platformName: str) -> List[str]: ...
    @staticmethod
    def version() -> QVersionNumber: ...

class QLine(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QLine: QLine) -> None: ...
    @overload
    def __init__(self, pt1: QPoint, pt2: QPoint) -> None: ...
    @overload
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def center(self) -> QPoint: ...
    def dx(self) -> int: ...
    def dy(self) -> int: ...
    def isNull(self) -> bool: ...
    def p1(self) -> QPoint: ...
    def p2(self) -> QPoint: ...
    def setLine(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def setP1(self, p1: QPoint) -> None: ...
    def setP2(self, p2: QPoint) -> None: ...
    def setPoints(self, p1: QPoint, p2: QPoint) -> None: ...
    def toTuple(self) -> object: ...
    @overload
    def translate(self, dx: int, dy: int) -> None: ...
    @overload
    def translate(self, p: QPoint) -> None: ...
    @overload
    def translated(self, dx: int, dy: int) -> QLine: ...
    @overload
    def translated(self, p: QPoint) -> QLine: ...
    def x1(self) -> int: ...
    def x2(self) -> int: ...
    def y1(self) -> int: ...
    def y2(self) -> int: ...

class QLineF(Shiboken.Object):

    NoIntersection: QLineF.IntersectionType = ...  # 0x0
    BoundedIntersection: QLineF.IntersectionType = ...  # 0x1
    UnboundedIntersection: QLineF.IntersectionType = ...  # 0x2
    class IntersectionType(Enum):

        NoIntersection: QLineF.IntersectionType = ...  # 0x0
        BoundedIntersection: QLineF.IntersectionType = ...  # 0x1
        UnboundedIntersection: QLineF.IntersectionType = ...  # 0x2
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QLineF: Union[QLineF, QLine]) -> None: ...
    @overload
    def __init__(self, line: QLine) -> None: ...
    @overload
    def __init__(self, pt1: Union[QPointF, QPoint], pt2: Union[QPointF, QPoint]) -> None: ...
    @overload
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def angle(self) -> float: ...
    def angleTo(self, l: Union[QLineF, QLine]) -> float: ...
    def center(self) -> QPointF: ...
    def dx(self) -> float: ...
    def dy(self) -> float: ...
    @staticmethod
    def fromPolar(length: float, angle: float) -> QLineF: ...
    def intersects(
        self, l: Union[QLineF, QLine], intersectionPoint: Union[QPointF, QPoint, NoneType] = ...
    ) -> Tuple: ...
    def isNull(self) -> bool: ...
    def length(self) -> float: ...
    def normalVector(self) -> QLineF: ...
    def p1(self) -> QPointF: ...
    def p2(self) -> QPointF: ...
    def pointAt(self, t: float) -> QPointF: ...
    def setAngle(self, angle: float) -> None: ...
    def setLength(self, len: float) -> None: ...
    def setLine(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    def setP1(self, p1: Union[QPointF, QPoint]) -> None: ...
    def setP2(self, p2: Union[QPointF, QPoint]) -> None: ...
    def setPoints(self, p1: Union[QPointF, QPoint], p2: Union[QPointF, QPoint]) -> None: ...
    def toLine(self) -> QLine: ...
    def toTuple(self) -> object: ...
    @overload
    def translate(self, dx: float, dy: float) -> None: ...
    @overload
    def translate(self, p: Union[QPointF, QPoint]) -> None: ...
    @overload
    def translated(self, dx: float, dy: float) -> QLineF: ...
    @overload
    def translated(self, p: Union[QPointF, QPoint]) -> QLineF: ...
    def unitVector(self) -> QLineF: ...
    def x1(self) -> float: ...
    def x2(self) -> float: ...
    def y1(self) -> float: ...
    def y2(self) -> float: ...

class QLocale(Shiboken.Object):

    AnyCountry: QLocale.Country = ...  # 0x0
    AnyTerritory: QLocale.Country = ...  # 0x0
    Afghanistan: QLocale.Country = ...  # 0x1
    AlandIslands: QLocale.Country = ...  # 0x2
    Albania: QLocale.Country = ...  # 0x3
    Algeria: QLocale.Country = ...  # 0x4
    AmericanSamoa: QLocale.Country = ...  # 0x5
    Andorra: QLocale.Country = ...  # 0x6
    Angola: QLocale.Country = ...  # 0x7
    Anguilla: QLocale.Country = ...  # 0x8
    Antarctica: QLocale.Country = ...  # 0x9
    AntiguaAndBarbuda: QLocale.Country = ...  # 0xa
    Argentina: QLocale.Country = ...  # 0xb
    Armenia: QLocale.Country = ...  # 0xc
    Aruba: QLocale.Country = ...  # 0xd
    AscensionIsland: QLocale.Country = ...  # 0xe
    Australia: QLocale.Country = ...  # 0xf
    Austria: QLocale.Country = ...  # 0x10
    Azerbaijan: QLocale.Country = ...  # 0x11
    Bahamas: QLocale.Country = ...  # 0x12
    Bahrain: QLocale.Country = ...  # 0x13
    Bangladesh: QLocale.Country = ...  # 0x14
    Barbados: QLocale.Country = ...  # 0x15
    Belarus: QLocale.Country = ...  # 0x16
    Belgium: QLocale.Country = ...  # 0x17
    Belize: QLocale.Country = ...  # 0x18
    Benin: QLocale.Country = ...  # 0x19
    Bermuda: QLocale.Country = ...  # 0x1a
    Bhutan: QLocale.Country = ...  # 0x1b
    Bolivia: QLocale.Country = ...  # 0x1c
    BosniaAndHerzegovina: QLocale.Country = ...  # 0x1d
    BosniaAndHerzegowina: QLocale.Country = ...  # 0x1d
    Botswana: QLocale.Country = ...  # 0x1e
    BouvetIsland: QLocale.Country = ...  # 0x1f
    Brazil: QLocale.Country = ...  # 0x20
    BritishIndianOceanTerritory: QLocale.Country = ...  # 0x21
    BritishVirginIslands: QLocale.Country = ...  # 0x22
    Brunei: QLocale.Country = ...  # 0x23
    Bulgaria: QLocale.Country = ...  # 0x24
    BurkinaFaso: QLocale.Country = ...  # 0x25
    Burundi: QLocale.Country = ...  # 0x26
    Cambodia: QLocale.Country = ...  # 0x27
    Cameroon: QLocale.Country = ...  # 0x28
    Canada: QLocale.Country = ...  # 0x29
    CanaryIslands: QLocale.Country = ...  # 0x2a
    CapeVerde: QLocale.Country = ...  # 0x2b
    Bonaire: QLocale.Country = ...  # 0x2c
    CaribbeanNetherlands: QLocale.Country = ...  # 0x2c
    CaymanIslands: QLocale.Country = ...  # 0x2d
    CentralAfricanRepublic: QLocale.Country = ...  # 0x2e
    CeutaAndMelilla: QLocale.Country = ...  # 0x2f
    Chad: QLocale.Country = ...  # 0x30
    Chile: QLocale.Country = ...  # 0x31
    China: QLocale.Country = ...  # 0x32
    ChristmasIsland: QLocale.Country = ...  # 0x33
    ClippertonIsland: QLocale.Country = ...  # 0x34
    CocosIslands: QLocale.Country = ...  # 0x35
    Colombia: QLocale.Country = ...  # 0x36
    Comoros: QLocale.Country = ...  # 0x37
    CongoBrazzaville: QLocale.Country = ...  # 0x38
    PeoplesRepublicOfCongo: QLocale.Country = ...  # 0x38
    CongoKinshasa: QLocale.Country = ...  # 0x39
    DemocraticRepublicOfCongo: QLocale.Country = ...  # 0x39
    CookIslands: QLocale.Country = ...  # 0x3a
    CostaRica: QLocale.Country = ...  # 0x3b
    Croatia: QLocale.Country = ...  # 0x3c
    Cuba: QLocale.Country = ...  # 0x3d
    CuraSao: QLocale.Country = ...  # 0x3e
    Curacao: QLocale.Country = ...  # 0x3e
    Cyprus: QLocale.Country = ...  # 0x3f
    CzechRepublic: QLocale.Country = ...  # 0x40
    Czechia: QLocale.Country = ...  # 0x40
    Denmark: QLocale.Country = ...  # 0x41
    DiegoGarcia: QLocale.Country = ...  # 0x42
    Djibouti: QLocale.Country = ...  # 0x43
    Dominica: QLocale.Country = ...  # 0x44
    DominicanRepublic: QLocale.Country = ...  # 0x45
    Ecuador: QLocale.Country = ...  # 0x46
    Egypt: QLocale.Country = ...  # 0x47
    ElSalvador: QLocale.Country = ...  # 0x48
    EquatorialGuinea: QLocale.Country = ...  # 0x49
    Eritrea: QLocale.Country = ...  # 0x4a
    Estonia: QLocale.Country = ...  # 0x4b
    Eswatini: QLocale.Country = ...  # 0x4c
    Swaziland: QLocale.Country = ...  # 0x4c
    Ethiopia: QLocale.Country = ...  # 0x4d
    Europe: QLocale.Country = ...  # 0x4e
    EuropeanUnion: QLocale.Country = ...  # 0x4f
    FalklandIslands: QLocale.Country = ...  # 0x50
    FaroeIslands: QLocale.Country = ...  # 0x51
    Fiji: QLocale.Country = ...  # 0x52
    Finland: QLocale.Country = ...  # 0x53
    France: QLocale.Country = ...  # 0x54
    FrenchGuiana: QLocale.Country = ...  # 0x55
    FrenchPolynesia: QLocale.Country = ...  # 0x56
    FrenchSouthernTerritories: QLocale.Country = ...  # 0x57
    Gabon: QLocale.Country = ...  # 0x58
    Gambia: QLocale.Country = ...  # 0x59
    Georgia: QLocale.Country = ...  # 0x5a
    Germany: QLocale.Country = ...  # 0x5b
    Ghana: QLocale.Country = ...  # 0x5c
    Gibraltar: QLocale.Country = ...  # 0x5d
    Greece: QLocale.Country = ...  # 0x5e
    Greenland: QLocale.Country = ...  # 0x5f
    Grenada: QLocale.Country = ...  # 0x60
    Guadeloupe: QLocale.Country = ...  # 0x61
    Guam: QLocale.Country = ...  # 0x62
    Guatemala: QLocale.Country = ...  # 0x63
    Guernsey: QLocale.Country = ...  # 0x64
    GuineaBissau: QLocale.Country = ...  # 0x65
    Guinea: QLocale.Country = ...  # 0x66
    Guyana: QLocale.Country = ...  # 0x67
    Haiti: QLocale.Country = ...  # 0x68
    HeardAndMcDonaldIslands: QLocale.Country = ...  # 0x69
    Honduras: QLocale.Country = ...  # 0x6a
    HongKong: QLocale.Country = ...  # 0x6b
    Hungary: QLocale.Country = ...  # 0x6c
    Iceland: QLocale.Country = ...  # 0x6d
    India: QLocale.Country = ...  # 0x6e
    Indonesia: QLocale.Country = ...  # 0x6f
    Iran: QLocale.Country = ...  # 0x70
    Iraq: QLocale.Country = ...  # 0x71
    Ireland: QLocale.Country = ...  # 0x72
    IsleOfMan: QLocale.Country = ...  # 0x73
    Israel: QLocale.Country = ...  # 0x74
    Italy: QLocale.Country = ...  # 0x75
    IvoryCoast: QLocale.Country = ...  # 0x76
    Jamaica: QLocale.Country = ...  # 0x77
    Japan: QLocale.Country = ...  # 0x78
    Jersey: QLocale.Country = ...  # 0x79
    Jordan: QLocale.Country = ...  # 0x7a
    Kazakhstan: QLocale.Country = ...  # 0x7b
    Kenya: QLocale.Country = ...  # 0x7c
    Kiribati: QLocale.Country = ...  # 0x7d
    Kosovo: QLocale.Country = ...  # 0x7e
    Kuwait: QLocale.Country = ...  # 0x7f
    Kyrgyzstan: QLocale.Country = ...  # 0x80
    Laos: QLocale.Country = ...  # 0x81
    LatinAmerica: QLocale.Country = ...  # 0x82
    LatinAmericaAndTheCaribbean: QLocale.Country = ...  # 0x82
    Latvia: QLocale.Country = ...  # 0x83
    Lebanon: QLocale.Country = ...  # 0x84
    Lesotho: QLocale.Country = ...  # 0x85
    Liberia: QLocale.Country = ...  # 0x86
    Libya: QLocale.Country = ...  # 0x87
    Liechtenstein: QLocale.Country = ...  # 0x88
    Lithuania: QLocale.Country = ...  # 0x89
    Luxembourg: QLocale.Country = ...  # 0x8a
    Macao: QLocale.Country = ...  # 0x8b
    Macau: QLocale.Country = ...  # 0x8b
    Macedonia: QLocale.Country = ...  # 0x8c
    Madagascar: QLocale.Country = ...  # 0x8d
    Malawi: QLocale.Country = ...  # 0x8e
    Malaysia: QLocale.Country = ...  # 0x8f
    Maldives: QLocale.Country = ...  # 0x90
    Mali: QLocale.Country = ...  # 0x91
    Malta: QLocale.Country = ...  # 0x92
    MarshallIslands: QLocale.Country = ...  # 0x93
    Martinique: QLocale.Country = ...  # 0x94
    Mauritania: QLocale.Country = ...  # 0x95
    Mauritius: QLocale.Country = ...  # 0x96
    Mayotte: QLocale.Country = ...  # 0x97
    Mexico: QLocale.Country = ...  # 0x98
    Micronesia: QLocale.Country = ...  # 0x99
    Moldova: QLocale.Country = ...  # 0x9a
    Monaco: QLocale.Country = ...  # 0x9b
    Mongolia: QLocale.Country = ...  # 0x9c
    Montenegro: QLocale.Country = ...  # 0x9d
    Montserrat: QLocale.Country = ...  # 0x9e
    Morocco: QLocale.Country = ...  # 0x9f
    Mozambique: QLocale.Country = ...  # 0xa0
    Myanmar: QLocale.Country = ...  # 0xa1
    Namibia: QLocale.Country = ...  # 0xa2
    NauruCountry: QLocale.Country = ...  # 0xa3
    NauruTerritory: QLocale.Country = ...  # 0xa3
    Nepal: QLocale.Country = ...  # 0xa4
    Netherlands: QLocale.Country = ...  # 0xa5
    NewCaledonia: QLocale.Country = ...  # 0xa6
    NewZealand: QLocale.Country = ...  # 0xa7
    Nicaragua: QLocale.Country = ...  # 0xa8
    Nigeria: QLocale.Country = ...  # 0xa9
    Niger: QLocale.Country = ...  # 0xaa
    Niue: QLocale.Country = ...  # 0xab
    NorfolkIsland: QLocale.Country = ...  # 0xac
    NorthernMarianaIslands: QLocale.Country = ...  # 0xad
    DemocraticRepublicOfKorea: QLocale.Country = ...  # 0xae
    NorthKorea: QLocale.Country = ...  # 0xae
    Norway: QLocale.Country = ...  # 0xaf
    Oman: QLocale.Country = ...  # 0xb0
    OutlyingOceania: QLocale.Country = ...  # 0xb1
    Pakistan: QLocale.Country = ...  # 0xb2
    Palau: QLocale.Country = ...  # 0xb3
    PalestinianTerritories: QLocale.Country = ...  # 0xb4
    Panama: QLocale.Country = ...  # 0xb5
    PapuaNewGuinea: QLocale.Country = ...  # 0xb6
    Paraguay: QLocale.Country = ...  # 0xb7
    Peru: QLocale.Country = ...  # 0xb8
    Philippines: QLocale.Country = ...  # 0xb9
    Pitcairn: QLocale.Country = ...  # 0xba
    Poland: QLocale.Country = ...  # 0xbb
    Portugal: QLocale.Country = ...  # 0xbc
    PuertoRico: QLocale.Country = ...  # 0xbd
    Qatar: QLocale.Country = ...  # 0xbe
    Reunion: QLocale.Country = ...  # 0xbf
    Romania: QLocale.Country = ...  # 0xc0
    Russia: QLocale.Country = ...  # 0xc1
    RussianFederation: QLocale.Country = ...  # 0xc1
    Rwanda: QLocale.Country = ...  # 0xc2
    SaintBarthelemy: QLocale.Country = ...  # 0xc3
    SaintHelena: QLocale.Country = ...  # 0xc4
    SaintKittsAndNevis: QLocale.Country = ...  # 0xc5
    SaintLucia: QLocale.Country = ...  # 0xc6
    SaintMartin: QLocale.Country = ...  # 0xc7
    SaintPierreAndMiquelon: QLocale.Country = ...  # 0xc8
    SaintVincentAndGrenadines: QLocale.Country = ...  # 0xc9
    SaintVincentAndTheGrenadines: QLocale.Country = ...  # 0xc9
    Samoa: QLocale.Country = ...  # 0xca
    SanMarino: QLocale.Country = ...  # 0xcb
    SaoTomeAndPrincipe: QLocale.Country = ...  # 0xcc
    SaudiArabia: QLocale.Country = ...  # 0xcd
    Senegal: QLocale.Country = ...  # 0xce
    Serbia: QLocale.Country = ...  # 0xcf
    Seychelles: QLocale.Country = ...  # 0xd0
    SierraLeone: QLocale.Country = ...  # 0xd1
    Singapore: QLocale.Country = ...  # 0xd2
    SintMaarten: QLocale.Country = ...  # 0xd3
    Slovakia: QLocale.Country = ...  # 0xd4
    Slovenia: QLocale.Country = ...  # 0xd5
    SolomonIslands: QLocale.Country = ...  # 0xd6
    Somalia: QLocale.Country = ...  # 0xd7
    SouthAfrica: QLocale.Country = ...  # 0xd8
    SouthGeorgiaAndSouthSandwichIslands: QLocale.Country = ...  # 0xd9
    SouthGeorgiaAndTheSouthSandwichIslands: QLocale.Country = ...  # 0xd9
    RepublicOfKorea: QLocale.Country = ...  # 0xda
    SouthKorea: QLocale.Country = ...  # 0xda
    SouthSudan: QLocale.Country = ...  # 0xdb
    Spain: QLocale.Country = ...  # 0xdc
    SriLanka: QLocale.Country = ...  # 0xdd
    Sudan: QLocale.Country = ...  # 0xde
    Suriname: QLocale.Country = ...  # 0xdf
    SvalbardAndJanMayen: QLocale.Country = ...  # 0xe0
    SvalbardAndJanMayenIslands: QLocale.Country = ...  # 0xe0
    Sweden: QLocale.Country = ...  # 0xe1
    Switzerland: QLocale.Country = ...  # 0xe2
    Syria: QLocale.Country = ...  # 0xe3
    SyrianArabRepublic: QLocale.Country = ...  # 0xe3
    Taiwan: QLocale.Country = ...  # 0xe4
    Tajikistan: QLocale.Country = ...  # 0xe5
    Tanzania: QLocale.Country = ...  # 0xe6
    Thailand: QLocale.Country = ...  # 0xe7
    EastTimor: QLocale.Country = ...  # 0xe8
    TimorLeste: QLocale.Country = ...  # 0xe8
    Togo: QLocale.Country = ...  # 0xe9
    TokelauCountry: QLocale.Country = ...  # 0xea
    TokelauTerritory: QLocale.Country = ...  # 0xea
    Tonga: QLocale.Country = ...  # 0xeb
    TrinidadAndTobago: QLocale.Country = ...  # 0xec
    TristanDaCunha: QLocale.Country = ...  # 0xed
    Tunisia: QLocale.Country = ...  # 0xee
    Turkey: QLocale.Country = ...  # 0xef
    Turkmenistan: QLocale.Country = ...  # 0xf0
    TurksAndCaicosIslands: QLocale.Country = ...  # 0xf1
    TuvaluCountry: QLocale.Country = ...  # 0xf2
    TuvaluTerritory: QLocale.Country = ...  # 0xf2
    Uganda: QLocale.Country = ...  # 0xf3
    Ukraine: QLocale.Country = ...  # 0xf4
    UnitedArabEmirates: QLocale.Country = ...  # 0xf5
    UnitedKingdom: QLocale.Country = ...  # 0xf6
    UnitedStatesMinorOutlyingIslands: QLocale.Country = ...  # 0xf7
    UnitedStatesOutlyingIslands: QLocale.Country = ...  # 0xf7
    UnitedStates: QLocale.Country = ...  # 0xf8
    UnitedStatesVirginIslands: QLocale.Country = ...  # 0xf9
    Uruguay: QLocale.Country = ...  # 0xfa
    Uzbekistan: QLocale.Country = ...  # 0xfb
    Vanuatu: QLocale.Country = ...  # 0xfc
    VaticanCity: QLocale.Country = ...  # 0xfd
    VaticanCityState: QLocale.Country = ...  # 0xfd
    Venezuela: QLocale.Country = ...  # 0xfe
    Vietnam: QLocale.Country = ...  # 0xff
    WallisAndFutuna: QLocale.Country = ...  # 0x100
    WallisAndFutunaIslands: QLocale.Country = ...  # 0x100
    WesternSahara: QLocale.Country = ...  # 0x101
    World: QLocale.Country = ...  # 0x102
    Yemen: QLocale.Country = ...  # 0x103
    Zambia: QLocale.Country = ...  # 0x104
    LastCountry: QLocale.Country = ...  # 0x105
    LastTerritory: QLocale.Country = ...  # 0x105
    Zimbabwe: QLocale.Country = ...  # 0x105
    CurrencyIsoCode: QLocale.CurrencySymbolFormat = ...  # 0x0
    CurrencySymbol: QLocale.CurrencySymbolFormat = ...  # 0x1
    CurrencyDisplayName: QLocale.CurrencySymbolFormat = ...  # 0x2
    DataSizeIecFormat: QLocale.DataSizeFormat = ...  # 0x0
    DataSizeBase1000: QLocale.DataSizeFormat = ...  # 0x1
    DataSizeSIQuantifiers: QLocale.DataSizeFormat = ...  # 0x2
    DataSizeTraditionalFormat: QLocale.DataSizeFormat = ...  # 0x2
    DataSizeSIFormat: QLocale.DataSizeFormat = ...  # 0x3
    FloatingPointShortest: QLocale.FloatingPointPrecisionOption = ...  # -0x80
    LongFormat: QLocale.FormatType = ...  # 0x0
    ShortFormat: QLocale.FormatType = ...  # 0x1
    NarrowFormat: QLocale.FormatType = ...  # 0x2
    AnyLanguage: QLocale.Language = ...  # 0x0
    C: QLocale.Language = ...  # 0x1
    Abkhazian: QLocale.Language = ...  # 0x2
    Afar: QLocale.Language = ...  # 0x3
    Afrikaans: QLocale.Language = ...  # 0x4
    Aghem: QLocale.Language = ...  # 0x5
    Akan: QLocale.Language = ...  # 0x6
    Akkadian: QLocale.Language = ...  # 0x7
    Akoose: QLocale.Language = ...  # 0x8
    Albanian: QLocale.Language = ...  # 0x9
    AmericanSignLanguage: QLocale.Language = ...  # 0xa
    Amharic: QLocale.Language = ...  # 0xb
    AncientEgyptian: QLocale.Language = ...  # 0xc
    AncientGreek: QLocale.Language = ...  # 0xd
    Arabic: QLocale.Language = ...  # 0xe
    Aragonese: QLocale.Language = ...  # 0xf
    Aramaic: QLocale.Language = ...  # 0x10
    Armenian: QLocale.Language = ...  # 0x11
    Assamese: QLocale.Language = ...  # 0x12
    Asturian: QLocale.Language = ...  # 0x13
    Asu: QLocale.Language = ...  # 0x14
    Atsam: QLocale.Language = ...  # 0x15
    Avaric: QLocale.Language = ...  # 0x16
    Avestan: QLocale.Language = ...  # 0x17
    Aymara: QLocale.Language = ...  # 0x18
    Azerbaijani: QLocale.Language = ...  # 0x19
    Bafia: QLocale.Language = ...  # 0x1a
    Balinese: QLocale.Language = ...  # 0x1b
    Bambara: QLocale.Language = ...  # 0x1c
    Bamun: QLocale.Language = ...  # 0x1d
    Bangla: QLocale.Language = ...  # 0x1e
    Bengali: QLocale.Language = ...  # 0x1e
    Basaa: QLocale.Language = ...  # 0x1f
    Bashkir: QLocale.Language = ...  # 0x20
    Basque: QLocale.Language = ...  # 0x21
    BatakToba: QLocale.Language = ...  # 0x22
    Belarusian: QLocale.Language = ...  # 0x23
    Byelorussian: QLocale.Language = ...  # 0x23
    Bemba: QLocale.Language = ...  # 0x24
    Bena: QLocale.Language = ...  # 0x25
    Bhojpuri: QLocale.Language = ...  # 0x26
    Bislama: QLocale.Language = ...  # 0x27
    Blin: QLocale.Language = ...  # 0x28
    Bodo: QLocale.Language = ...  # 0x29
    Bosnian: QLocale.Language = ...  # 0x2a
    Breton: QLocale.Language = ...  # 0x2b
    Buginese: QLocale.Language = ...  # 0x2c
    Bulgarian: QLocale.Language = ...  # 0x2d
    Burmese: QLocale.Language = ...  # 0x2e
    Cantonese: QLocale.Language = ...  # 0x2f
    Catalan: QLocale.Language = ...  # 0x30
    Cebuano: QLocale.Language = ...  # 0x31
    CentralAtlasTamazight: QLocale.Language = ...  # 0x32
    CentralMoroccoTamazight: QLocale.Language = ...  # 0x32
    CentralKurdish: QLocale.Language = ...  # 0x33
    Chakma: QLocale.Language = ...  # 0x34
    Chamorro: QLocale.Language = ...  # 0x35
    Chechen: QLocale.Language = ...  # 0x36
    Cherokee: QLocale.Language = ...  # 0x37
    Chickasaw: QLocale.Language = ...  # 0x38
    Chiga: QLocale.Language = ...  # 0x39
    Chinese: QLocale.Language = ...  # 0x3a
    Church: QLocale.Language = ...  # 0x3b
    Chuvash: QLocale.Language = ...  # 0x3c
    Colognian: QLocale.Language = ...  # 0x3d
    Coptic: QLocale.Language = ...  # 0x3e
    Cornish: QLocale.Language = ...  # 0x3f
    Corsican: QLocale.Language = ...  # 0x40
    Cree: QLocale.Language = ...  # 0x41
    Croatian: QLocale.Language = ...  # 0x42
    Czech: QLocale.Language = ...  # 0x43
    Danish: QLocale.Language = ...  # 0x44
    Divehi: QLocale.Language = ...  # 0x45
    Dogri: QLocale.Language = ...  # 0x46
    Duala: QLocale.Language = ...  # 0x47
    Dutch: QLocale.Language = ...  # 0x48
    Bhutani: QLocale.Language = ...  # 0x49
    Dzongkha: QLocale.Language = ...  # 0x49
    Embu: QLocale.Language = ...  # 0x4a
    English: QLocale.Language = ...  # 0x4b
    Erzya: QLocale.Language = ...  # 0x4c
    Esperanto: QLocale.Language = ...  # 0x4d
    Estonian: QLocale.Language = ...  # 0x4e
    Ewe: QLocale.Language = ...  # 0x4f
    Ewondo: QLocale.Language = ...  # 0x50
    Faroese: QLocale.Language = ...  # 0x51
    Fijian: QLocale.Language = ...  # 0x52
    Filipino: QLocale.Language = ...  # 0x53
    Finnish: QLocale.Language = ...  # 0x54
    French: QLocale.Language = ...  # 0x55
    Friulian: QLocale.Language = ...  # 0x56
    Fulah: QLocale.Language = ...  # 0x57
    Gaelic: QLocale.Language = ...  # 0x58
    Ga: QLocale.Language = ...  # 0x59
    Galician: QLocale.Language = ...  # 0x5a
    Ganda: QLocale.Language = ...  # 0x5b
    Geez: QLocale.Language = ...  # 0x5c
    Georgian: QLocale.Language = ...  # 0x5d
    German: QLocale.Language = ...  # 0x5e
    Gothic: QLocale.Language = ...  # 0x5f
    Greek: QLocale.Language = ...  # 0x60
    Guarani: QLocale.Language = ...  # 0x61
    Gujarati: QLocale.Language = ...  # 0x62
    Gusii: QLocale.Language = ...  # 0x63
    Haitian: QLocale.Language = ...  # 0x64
    Hausa: QLocale.Language = ...  # 0x65
    Hawaiian: QLocale.Language = ...  # 0x66
    Hebrew: QLocale.Language = ...  # 0x67
    Herero: QLocale.Language = ...  # 0x68
    Hindi: QLocale.Language = ...  # 0x69
    HiriMotu: QLocale.Language = ...  # 0x6a
    Hungarian: QLocale.Language = ...  # 0x6b
    Icelandic: QLocale.Language = ...  # 0x6c
    Ido: QLocale.Language = ...  # 0x6d
    Igbo: QLocale.Language = ...  # 0x6e
    InariSami: QLocale.Language = ...  # 0x6f
    Indonesian: QLocale.Language = ...  # 0x70
    Ingush: QLocale.Language = ...  # 0x71
    Interlingua: QLocale.Language = ...  # 0x72
    Interlingue: QLocale.Language = ...  # 0x73
    Inuktitut: QLocale.Language = ...  # 0x74
    Inupiak: QLocale.Language = ...  # 0x75
    Inupiaq: QLocale.Language = ...  # 0x75
    Irish: QLocale.Language = ...  # 0x76
    Italian: QLocale.Language = ...  # 0x77
    Japanese: QLocale.Language = ...  # 0x78
    Javanese: QLocale.Language = ...  # 0x79
    Jju: QLocale.Language = ...  # 0x7a
    JolaFonyi: QLocale.Language = ...  # 0x7b
    Kabuverdianu: QLocale.Language = ...  # 0x7c
    Kabyle: QLocale.Language = ...  # 0x7d
    Kako: QLocale.Language = ...  # 0x7e
    Greenlandic: QLocale.Language = ...  # 0x7f
    Kalaallisut: QLocale.Language = ...  # 0x7f
    Kalenjin: QLocale.Language = ...  # 0x80
    Kamba: QLocale.Language = ...  # 0x81
    Kannada: QLocale.Language = ...  # 0x82
    Kanuri: QLocale.Language = ...  # 0x83
    Kashmiri: QLocale.Language = ...  # 0x84
    Kazakh: QLocale.Language = ...  # 0x85
    Kenyang: QLocale.Language = ...  # 0x86
    Cambodian: QLocale.Language = ...  # 0x87
    Khmer: QLocale.Language = ...  # 0x87
    Kiche: QLocale.Language = ...  # 0x88
    Kikuyu: QLocale.Language = ...  # 0x89
    Kinyarwanda: QLocale.Language = ...  # 0x8a
    Komi: QLocale.Language = ...  # 0x8b
    Kongo: QLocale.Language = ...  # 0x8c
    Konkani: QLocale.Language = ...  # 0x8d
    Korean: QLocale.Language = ...  # 0x8e
    Koro: QLocale.Language = ...  # 0x8f
    KoyraboroSenni: QLocale.Language = ...  # 0x90
    KoyraChiini: QLocale.Language = ...  # 0x91
    Kpelle: QLocale.Language = ...  # 0x92
    Kuanyama: QLocale.Language = ...  # 0x93
    Kwanyama: QLocale.Language = ...  # 0x93
    Kurdish: QLocale.Language = ...  # 0x94
    Kwasio: QLocale.Language = ...  # 0x95
    Kirghiz: QLocale.Language = ...  # 0x96
    Kyrgyz: QLocale.Language = ...  # 0x96
    Lakota: QLocale.Language = ...  # 0x97
    Langi: QLocale.Language = ...  # 0x98
    Lao: QLocale.Language = ...  # 0x99
    Latin: QLocale.Language = ...  # 0x9a
    Latvian: QLocale.Language = ...  # 0x9b
    Lezghian: QLocale.Language = ...  # 0x9c
    Limburgish: QLocale.Language = ...  # 0x9d
    Lingala: QLocale.Language = ...  # 0x9e
    LiteraryChinese: QLocale.Language = ...  # 0x9f
    Lithuanian: QLocale.Language = ...  # 0xa0
    Lojban: QLocale.Language = ...  # 0xa1
    LowerSorbian: QLocale.Language = ...  # 0xa2
    LowGerman: QLocale.Language = ...  # 0xa3
    LubaKatanga: QLocale.Language = ...  # 0xa4
    LuleSami: QLocale.Language = ...  # 0xa5
    Luo: QLocale.Language = ...  # 0xa6
    Luxembourgish: QLocale.Language = ...  # 0xa7
    Luyia: QLocale.Language = ...  # 0xa8
    Macedonian: QLocale.Language = ...  # 0xa9
    Machame: QLocale.Language = ...  # 0xaa
    Maithili: QLocale.Language = ...  # 0xab
    MakhuwaMeetto: QLocale.Language = ...  # 0xac
    Makonde: QLocale.Language = ...  # 0xad
    Malagasy: QLocale.Language = ...  # 0xae
    Malayalam: QLocale.Language = ...  # 0xaf
    Malay: QLocale.Language = ...  # 0xb0
    Maltese: QLocale.Language = ...  # 0xb1
    Mandingo: QLocale.Language = ...  # 0xb2
    Manipuri: QLocale.Language = ...  # 0xb3
    Manx: QLocale.Language = ...  # 0xb4
    Maori: QLocale.Language = ...  # 0xb5
    Mapuche: QLocale.Language = ...  # 0xb6
    Marathi: QLocale.Language = ...  # 0xb7
    Marshallese: QLocale.Language = ...  # 0xb8
    Masai: QLocale.Language = ...  # 0xb9
    Mazanderani: QLocale.Language = ...  # 0xba
    Mende: QLocale.Language = ...  # 0xbb
    Meru: QLocale.Language = ...  # 0xbc
    Meta: QLocale.Language = ...  # 0xbd
    Mohawk: QLocale.Language = ...  # 0xbe
    Mongolian: QLocale.Language = ...  # 0xbf
    Morisyen: QLocale.Language = ...  # 0xc0
    Mundang: QLocale.Language = ...  # 0xc1
    Muscogee: QLocale.Language = ...  # 0xc2
    Nama: QLocale.Language = ...  # 0xc3
    NauruLanguage: QLocale.Language = ...  # 0xc4
    Navaho: QLocale.Language = ...  # 0xc5
    Navajo: QLocale.Language = ...  # 0xc5
    Ndonga: QLocale.Language = ...  # 0xc6
    Nepali: QLocale.Language = ...  # 0xc7
    Newari: QLocale.Language = ...  # 0xc8
    Ngiemboon: QLocale.Language = ...  # 0xc9
    Ngomba: QLocale.Language = ...  # 0xca
    NigerianPidgin: QLocale.Language = ...  # 0xcb
    Nko: QLocale.Language = ...  # 0xcc
    NorthernLuri: QLocale.Language = ...  # 0xcd
    NorthernSami: QLocale.Language = ...  # 0xce
    NorthernSotho: QLocale.Language = ...  # 0xcf
    NorthNdebele: QLocale.Language = ...  # 0xd0
    NorwegianBokmal: QLocale.Language = ...  # 0xd1
    NorwegianNynorsk: QLocale.Language = ...  # 0xd2
    Nuer: QLocale.Language = ...  # 0xd3
    Chewa: QLocale.Language = ...  # 0xd4
    Nyanja: QLocale.Language = ...  # 0xd4
    Nyankole: QLocale.Language = ...  # 0xd5
    Occitan: QLocale.Language = ...  # 0xd6
    Odia: QLocale.Language = ...  # 0xd7
    Oriya: QLocale.Language = ...  # 0xd7
    Ojibwa: QLocale.Language = ...  # 0xd8
    OldIrish: QLocale.Language = ...  # 0xd9
    OldNorse: QLocale.Language = ...  # 0xda
    OldPersian: QLocale.Language = ...  # 0xdb
    Afan: QLocale.Language = ...  # 0xdc
    Oromo: QLocale.Language = ...  # 0xdc
    Osage: QLocale.Language = ...  # 0xdd
    Ossetic: QLocale.Language = ...  # 0xde
    Pahlavi: QLocale.Language = ...  # 0xdf
    Palauan: QLocale.Language = ...  # 0xe0
    Pali: QLocale.Language = ...  # 0xe1
    Papiamento: QLocale.Language = ...  # 0xe2
    Pashto: QLocale.Language = ...  # 0xe3
    Persian: QLocale.Language = ...  # 0xe4
    Phoenician: QLocale.Language = ...  # 0xe5
    Polish: QLocale.Language = ...  # 0xe6
    Portuguese: QLocale.Language = ...  # 0xe7
    Prussian: QLocale.Language = ...  # 0xe8
    Punjabi: QLocale.Language = ...  # 0xe9
    Quechua: QLocale.Language = ...  # 0xea
    Romanian: QLocale.Language = ...  # 0xeb
    RhaetoRomance: QLocale.Language = ...  # 0xec
    Romansh: QLocale.Language = ...  # 0xec
    Rombo: QLocale.Language = ...  # 0xed
    Kurundi: QLocale.Language = ...  # 0xee
    Rundi: QLocale.Language = ...  # 0xee
    Russian: QLocale.Language = ...  # 0xef
    Rwa: QLocale.Language = ...  # 0xf0
    Saho: QLocale.Language = ...  # 0xf1
    Sakha: QLocale.Language = ...  # 0xf2
    Samburu: QLocale.Language = ...  # 0xf3
    Samoan: QLocale.Language = ...  # 0xf4
    Sango: QLocale.Language = ...  # 0xf5
    Sangu: QLocale.Language = ...  # 0xf6
    Sanskrit: QLocale.Language = ...  # 0xf7
    Santali: QLocale.Language = ...  # 0xf8
    Sardinian: QLocale.Language = ...  # 0xf9
    Saurashtra: QLocale.Language = ...  # 0xfa
    Sena: QLocale.Language = ...  # 0xfb
    Serbian: QLocale.Language = ...  # 0xfc
    Shambala: QLocale.Language = ...  # 0xfd
    Shona: QLocale.Language = ...  # 0xfe
    SichuanYi: QLocale.Language = ...  # 0xff
    Sicilian: QLocale.Language = ...  # 0x100
    Sidamo: QLocale.Language = ...  # 0x101
    Silesian: QLocale.Language = ...  # 0x102
    Sindhi: QLocale.Language = ...  # 0x103
    Sinhala: QLocale.Language = ...  # 0x104
    SkoltSami: QLocale.Language = ...  # 0x105
    Slovak: QLocale.Language = ...  # 0x106
    Slovenian: QLocale.Language = ...  # 0x107
    Soga: QLocale.Language = ...  # 0x108
    Somali: QLocale.Language = ...  # 0x109
    SouthernKurdish: QLocale.Language = ...  # 0x10a
    SouthernSami: QLocale.Language = ...  # 0x10b
    SouthernSotho: QLocale.Language = ...  # 0x10c
    SouthNdebele: QLocale.Language = ...  # 0x10d
    Spanish: QLocale.Language = ...  # 0x10e
    StandardMoroccanTamazight: QLocale.Language = ...  # 0x10f
    Sundanese: QLocale.Language = ...  # 0x110
    Swahili: QLocale.Language = ...  # 0x111
    Swati: QLocale.Language = ...  # 0x112
    Swedish: QLocale.Language = ...  # 0x113
    SwissGerman: QLocale.Language = ...  # 0x114
    Syriac: QLocale.Language = ...  # 0x115
    Tachelhit: QLocale.Language = ...  # 0x116
    Tahitian: QLocale.Language = ...  # 0x117
    TaiDam: QLocale.Language = ...  # 0x118
    Taita: QLocale.Language = ...  # 0x119
    Tajik: QLocale.Language = ...  # 0x11a
    Tamil: QLocale.Language = ...  # 0x11b
    Taroko: QLocale.Language = ...  # 0x11c
    Tasawaq: QLocale.Language = ...  # 0x11d
    Tatar: QLocale.Language = ...  # 0x11e
    Telugu: QLocale.Language = ...  # 0x11f
    Teso: QLocale.Language = ...  # 0x120
    Thai: QLocale.Language = ...  # 0x121
    Tibetan: QLocale.Language = ...  # 0x122
    Tigre: QLocale.Language = ...  # 0x123
    Tigrinya: QLocale.Language = ...  # 0x124
    TokelauLanguage: QLocale.Language = ...  # 0x125
    TokPisin: QLocale.Language = ...  # 0x126
    Tongan: QLocale.Language = ...  # 0x127
    Tsonga: QLocale.Language = ...  # 0x128
    Tswana: QLocale.Language = ...  # 0x129
    Turkish: QLocale.Language = ...  # 0x12a
    Turkmen: QLocale.Language = ...  # 0x12b
    TuvaluLanguage: QLocale.Language = ...  # 0x12c
    Tyap: QLocale.Language = ...  # 0x12d
    Ugaritic: QLocale.Language = ...  # 0x12e
    Ukrainian: QLocale.Language = ...  # 0x12f
    UpperSorbian: QLocale.Language = ...  # 0x130
    Urdu: QLocale.Language = ...  # 0x131
    Uighur: QLocale.Language = ...  # 0x132
    Uigur: QLocale.Language = ...  # 0x132
    Uyghur: QLocale.Language = ...  # 0x132
    Uzbek: QLocale.Language = ...  # 0x133
    Vai: QLocale.Language = ...  # 0x134
    Venda: QLocale.Language = ...  # 0x135
    Vietnamese: QLocale.Language = ...  # 0x136
    Volapuk: QLocale.Language = ...  # 0x137
    Vunjo: QLocale.Language = ...  # 0x138
    Walloon: QLocale.Language = ...  # 0x139
    Walser: QLocale.Language = ...  # 0x13a
    Warlpiri: QLocale.Language = ...  # 0x13b
    Welsh: QLocale.Language = ...  # 0x13c
    WesternBalochi: QLocale.Language = ...  # 0x13d
    Frisian: QLocale.Language = ...  # 0x13e
    WesternFrisian: QLocale.Language = ...  # 0x13e
    Walamo: QLocale.Language = ...  # 0x13f
    Wolaytta: QLocale.Language = ...  # 0x13f
    Wolof: QLocale.Language = ...  # 0x140
    Xhosa: QLocale.Language = ...  # 0x141
    Yangben: QLocale.Language = ...  # 0x142
    Yiddish: QLocale.Language = ...  # 0x143
    Yoruba: QLocale.Language = ...  # 0x144
    Zarma: QLocale.Language = ...  # 0x145
    Zhuang: QLocale.Language = ...  # 0x146
    LastLanguage: QLocale.Language = ...  # 0x147
    Zulu: QLocale.Language = ...  # 0x147
    MetricSystem: QLocale.MeasurementSystem = ...  # 0x0
    ImperialSystem: QLocale.MeasurementSystem = ...  # 0x1
    ImperialUSSystem: QLocale.MeasurementSystem = ...  # 0x1
    ImperialUKSystem: QLocale.MeasurementSystem = ...  # 0x2
    DefaultNumberOptions: QLocale.NumberOption = ...  # 0x0
    OmitGroupSeparator: QLocale.NumberOption = ...  # 0x1
    RejectGroupSeparator: QLocale.NumberOption = ...  # 0x2
    OmitLeadingZeroInExponent: QLocale.NumberOption = ...  # 0x4
    RejectLeadingZeroInExponent: QLocale.NumberOption = ...  # 0x8
    IncludeTrailingZeroesAfterDot: QLocale.NumberOption = ...  # 0x10
    RejectTrailingZeroesAfterDot: QLocale.NumberOption = ...  # 0x20
    StandardQuotation: QLocale.QuotationStyle = ...  # 0x0
    AlternateQuotation: QLocale.QuotationStyle = ...  # 0x1
    AnyScript: QLocale.Script = ...  # 0x0
    AdlamScript: QLocale.Script = ...  # 0x1
    AhomScript: QLocale.Script = ...  # 0x2
    AnatolianHieroglyphsScript: QLocale.Script = ...  # 0x3
    ArabicScript: QLocale.Script = ...  # 0x4
    ArmenianScript: QLocale.Script = ...  # 0x5
    AvestanScript: QLocale.Script = ...  # 0x6
    BalineseScript: QLocale.Script = ...  # 0x7
    BamumScript: QLocale.Script = ...  # 0x8
    BanglaScript: QLocale.Script = ...  # 0x9
    BengaliScript: QLocale.Script = ...  # 0x9
    BassaVahScript: QLocale.Script = ...  # 0xa
    BatakScript: QLocale.Script = ...  # 0xb
    BhaiksukiScript: QLocale.Script = ...  # 0xc
    BopomofoScript: QLocale.Script = ...  # 0xd
    BrahmiScript: QLocale.Script = ...  # 0xe
    BrailleScript: QLocale.Script = ...  # 0xf
    BugineseScript: QLocale.Script = ...  # 0x10
    BuhidScript: QLocale.Script = ...  # 0x11
    CanadianAboriginalScript: QLocale.Script = ...  # 0x12
    CarianScript: QLocale.Script = ...  # 0x13
    CaucasianAlbanianScript: QLocale.Script = ...  # 0x14
    ChakmaScript: QLocale.Script = ...  # 0x15
    ChamScript: QLocale.Script = ...  # 0x16
    CherokeeScript: QLocale.Script = ...  # 0x17
    CopticScript: QLocale.Script = ...  # 0x18
    CuneiformScript: QLocale.Script = ...  # 0x19
    CypriotScript: QLocale.Script = ...  # 0x1a
    CyrillicScript: QLocale.Script = ...  # 0x1b
    DeseretScript: QLocale.Script = ...  # 0x1c
    DevanagariScript: QLocale.Script = ...  # 0x1d
    DuployanScript: QLocale.Script = ...  # 0x1e
    EgyptianHieroglyphsScript: QLocale.Script = ...  # 0x1f
    ElbasanScript: QLocale.Script = ...  # 0x20
    EthiopicScript: QLocale.Script = ...  # 0x21
    FraserScript: QLocale.Script = ...  # 0x22
    GeorgianScript: QLocale.Script = ...  # 0x23
    GlagoliticScript: QLocale.Script = ...  # 0x24
    GothicScript: QLocale.Script = ...  # 0x25
    GranthaScript: QLocale.Script = ...  # 0x26
    GreekScript: QLocale.Script = ...  # 0x27
    GujaratiScript: QLocale.Script = ...  # 0x28
    GurmukhiScript: QLocale.Script = ...  # 0x29
    HangulScript: QLocale.Script = ...  # 0x2a
    HanScript: QLocale.Script = ...  # 0x2b
    HanunooScript: QLocale.Script = ...  # 0x2c
    HanWithBopomofoScript: QLocale.Script = ...  # 0x2d
    HatranScript: QLocale.Script = ...  # 0x2e
    HebrewScript: QLocale.Script = ...  # 0x2f
    HiraganaScript: QLocale.Script = ...  # 0x30
    ImperialAramaicScript: QLocale.Script = ...  # 0x31
    InscriptionalPahlaviScript: QLocale.Script = ...  # 0x32
    InscriptionalParthianScript: QLocale.Script = ...  # 0x33
    JamoScript: QLocale.Script = ...  # 0x34
    JapaneseScript: QLocale.Script = ...  # 0x35
    JavaneseScript: QLocale.Script = ...  # 0x36
    KaithiScript: QLocale.Script = ...  # 0x37
    KannadaScript: QLocale.Script = ...  # 0x38
    KatakanaScript: QLocale.Script = ...  # 0x39
    KayahLiScript: QLocale.Script = ...  # 0x3a
    KharoshthiScript: QLocale.Script = ...  # 0x3b
    KhmerScript: QLocale.Script = ...  # 0x3c
    KhojkiScript: QLocale.Script = ...  # 0x3d
    KhudawadiScript: QLocale.Script = ...  # 0x3e
    KoreanScript: QLocale.Script = ...  # 0x3f
    LannaScript: QLocale.Script = ...  # 0x40
    LaoScript: QLocale.Script = ...  # 0x41
    LatinScript: QLocale.Script = ...  # 0x42
    LepchaScript: QLocale.Script = ...  # 0x43
    LimbuScript: QLocale.Script = ...  # 0x44
    LinearAScript: QLocale.Script = ...  # 0x45
    LinearBScript: QLocale.Script = ...  # 0x46
    LycianScript: QLocale.Script = ...  # 0x47
    LydianScript: QLocale.Script = ...  # 0x48
    MahajaniScript: QLocale.Script = ...  # 0x49
    MalayalamScript: QLocale.Script = ...  # 0x4a
    MandaeanScript: QLocale.Script = ...  # 0x4b
    ManichaeanScript: QLocale.Script = ...  # 0x4c
    MarchenScript: QLocale.Script = ...  # 0x4d
    MeiteiMayekScript: QLocale.Script = ...  # 0x4e
    MendeKikakuiScript: QLocale.Script = ...  # 0x4f
    MendeScript: QLocale.Script = ...  # 0x4f
    MeroiticCursiveScript: QLocale.Script = ...  # 0x50
    MeroiticScript: QLocale.Script = ...  # 0x51
    ModiScript: QLocale.Script = ...  # 0x52
    MongolianScript: QLocale.Script = ...  # 0x53
    MroScript: QLocale.Script = ...  # 0x54
    MultaniScript: QLocale.Script = ...  # 0x55
    MyanmarScript: QLocale.Script = ...  # 0x56
    NabataeanScript: QLocale.Script = ...  # 0x57
    NewaScript: QLocale.Script = ...  # 0x58
    NewTaiLueScript: QLocale.Script = ...  # 0x59
    NkoScript: QLocale.Script = ...  # 0x5a
    OdiaScript: QLocale.Script = ...  # 0x5b
    OriyaScript: QLocale.Script = ...  # 0x5b
    OghamScript: QLocale.Script = ...  # 0x5c
    OlChikiScript: QLocale.Script = ...  # 0x5d
    OldHungarianScript: QLocale.Script = ...  # 0x5e
    OldItalicScript: QLocale.Script = ...  # 0x5f
    OldNorthArabianScript: QLocale.Script = ...  # 0x60
    OldPermicScript: QLocale.Script = ...  # 0x61
    OldPersianScript: QLocale.Script = ...  # 0x62
    OldSouthArabianScript: QLocale.Script = ...  # 0x63
    OrkhonScript: QLocale.Script = ...  # 0x64
    OsageScript: QLocale.Script = ...  # 0x65
    OsmanyaScript: QLocale.Script = ...  # 0x66
    PahawhHmongScript: QLocale.Script = ...  # 0x67
    PalmyreneScript: QLocale.Script = ...  # 0x68
    PauCinHauScript: QLocale.Script = ...  # 0x69
    PhagsPaScript: QLocale.Script = ...  # 0x6a
    PhoenicianScript: QLocale.Script = ...  # 0x6b
    PollardPhoneticScript: QLocale.Script = ...  # 0x6c
    PsalterPahlaviScript: QLocale.Script = ...  # 0x6d
    RejangScript: QLocale.Script = ...  # 0x6e
    RunicScript: QLocale.Script = ...  # 0x6f
    SamaritanScript: QLocale.Script = ...  # 0x70
    SaurashtraScript: QLocale.Script = ...  # 0x71
    SharadaScript: QLocale.Script = ...  # 0x72
    ShavianScript: QLocale.Script = ...  # 0x73
    SiddhamScript: QLocale.Script = ...  # 0x74
    SignWritingScript: QLocale.Script = ...  # 0x75
    SimplifiedChineseScript: QLocale.Script = ...  # 0x76
    SimplifiedHanScript: QLocale.Script = ...  # 0x76
    SinhalaScript: QLocale.Script = ...  # 0x77
    SoraSompengScript: QLocale.Script = ...  # 0x78
    SundaneseScript: QLocale.Script = ...  # 0x79
    SylotiNagriScript: QLocale.Script = ...  # 0x7a
    SyriacScript: QLocale.Script = ...  # 0x7b
    TagalogScript: QLocale.Script = ...  # 0x7c
    TagbanwaScript: QLocale.Script = ...  # 0x7d
    TaiLeScript: QLocale.Script = ...  # 0x7e
    TaiVietScript: QLocale.Script = ...  # 0x7f
    TakriScript: QLocale.Script = ...  # 0x80
    TamilScript: QLocale.Script = ...  # 0x81
    TangutScript: QLocale.Script = ...  # 0x82
    TeluguScript: QLocale.Script = ...  # 0x83
    ThaanaScript: QLocale.Script = ...  # 0x84
    ThaiScript: QLocale.Script = ...  # 0x85
    TibetanScript: QLocale.Script = ...  # 0x86
    TifinaghScript: QLocale.Script = ...  # 0x87
    TirhutaScript: QLocale.Script = ...  # 0x88
    TraditionalChineseScript: QLocale.Script = ...  # 0x89
    TraditionalHanScript: QLocale.Script = ...  # 0x89
    UgariticScript: QLocale.Script = ...  # 0x8a
    VaiScript: QLocale.Script = ...  # 0x8b
    VarangKshitiScript: QLocale.Script = ...  # 0x8c
    LastScript: QLocale.Script = ...  # 0x8d
    YiScript: QLocale.Script = ...  # 0x8d
    class Country(Enum):

        AnyCountry: QLocale.Country = ...  # 0x0
        AnyTerritory: QLocale.Country = ...  # 0x0
        Afghanistan: QLocale.Country = ...  # 0x1
        AlandIslands: QLocale.Country = ...  # 0x2
        Albania: QLocale.Country = ...  # 0x3
        Algeria: QLocale.Country = ...  # 0x4
        AmericanSamoa: QLocale.Country = ...  # 0x5
        Andorra: QLocale.Country = ...  # 0x6
        Angola: QLocale.Country = ...  # 0x7
        Anguilla: QLocale.Country = ...  # 0x8
        Antarctica: QLocale.Country = ...  # 0x9
        AntiguaAndBarbuda: QLocale.Country = ...  # 0xa
        Argentina: QLocale.Country = ...  # 0xb
        Armenia: QLocale.Country = ...  # 0xc
        Aruba: QLocale.Country = ...  # 0xd
        AscensionIsland: QLocale.Country = ...  # 0xe
        Australia: QLocale.Country = ...  # 0xf
        Austria: QLocale.Country = ...  # 0x10
        Azerbaijan: QLocale.Country = ...  # 0x11
        Bahamas: QLocale.Country = ...  # 0x12
        Bahrain: QLocale.Country = ...  # 0x13
        Bangladesh: QLocale.Country = ...  # 0x14
        Barbados: QLocale.Country = ...  # 0x15
        Belarus: QLocale.Country = ...  # 0x16
        Belgium: QLocale.Country = ...  # 0x17
        Belize: QLocale.Country = ...  # 0x18
        Benin: QLocale.Country = ...  # 0x19
        Bermuda: QLocale.Country = ...  # 0x1a
        Bhutan: QLocale.Country = ...  # 0x1b
        Bolivia: QLocale.Country = ...  # 0x1c
        BosniaAndHerzegovina: QLocale.Country = ...  # 0x1d
        BosniaAndHerzegowina: QLocale.Country = ...  # 0x1d
        Botswana: QLocale.Country = ...  # 0x1e
        BouvetIsland: QLocale.Country = ...  # 0x1f
        Brazil: QLocale.Country = ...  # 0x20
        BritishIndianOceanTerritory: QLocale.Country = ...  # 0x21
        BritishVirginIslands: QLocale.Country = ...  # 0x22
        Brunei: QLocale.Country = ...  # 0x23
        Bulgaria: QLocale.Country = ...  # 0x24
        BurkinaFaso: QLocale.Country = ...  # 0x25
        Burundi: QLocale.Country = ...  # 0x26
        Cambodia: QLocale.Country = ...  # 0x27
        Cameroon: QLocale.Country = ...  # 0x28
        Canada: QLocale.Country = ...  # 0x29
        CanaryIslands: QLocale.Country = ...  # 0x2a
        CapeVerde: QLocale.Country = ...  # 0x2b
        Bonaire: QLocale.Country = ...  # 0x2c
        CaribbeanNetherlands: QLocale.Country = ...  # 0x2c
        CaymanIslands: QLocale.Country = ...  # 0x2d
        CentralAfricanRepublic: QLocale.Country = ...  # 0x2e
        CeutaAndMelilla: QLocale.Country = ...  # 0x2f
        Chad: QLocale.Country = ...  # 0x30
        Chile: QLocale.Country = ...  # 0x31
        China: QLocale.Country = ...  # 0x32
        ChristmasIsland: QLocale.Country = ...  # 0x33
        ClippertonIsland: QLocale.Country = ...  # 0x34
        CocosIslands: QLocale.Country = ...  # 0x35
        Colombia: QLocale.Country = ...  # 0x36
        Comoros: QLocale.Country = ...  # 0x37
        CongoBrazzaville: QLocale.Country = ...  # 0x38
        PeoplesRepublicOfCongo: QLocale.Country = ...  # 0x38
        CongoKinshasa: QLocale.Country = ...  # 0x39
        DemocraticRepublicOfCongo: QLocale.Country = ...  # 0x39
        CookIslands: QLocale.Country = ...  # 0x3a
        CostaRica: QLocale.Country = ...  # 0x3b
        Croatia: QLocale.Country = ...  # 0x3c
        Cuba: QLocale.Country = ...  # 0x3d
        CuraSao: QLocale.Country = ...  # 0x3e
        Curacao: QLocale.Country = ...  # 0x3e
        Cyprus: QLocale.Country = ...  # 0x3f
        CzechRepublic: QLocale.Country = ...  # 0x40
        Czechia: QLocale.Country = ...  # 0x40
        Denmark: QLocale.Country = ...  # 0x41
        DiegoGarcia: QLocale.Country = ...  # 0x42
        Djibouti: QLocale.Country = ...  # 0x43
        Dominica: QLocale.Country = ...  # 0x44
        DominicanRepublic: QLocale.Country = ...  # 0x45
        Ecuador: QLocale.Country = ...  # 0x46
        Egypt: QLocale.Country = ...  # 0x47
        ElSalvador: QLocale.Country = ...  # 0x48
        EquatorialGuinea: QLocale.Country = ...  # 0x49
        Eritrea: QLocale.Country = ...  # 0x4a
        Estonia: QLocale.Country = ...  # 0x4b
        Eswatini: QLocale.Country = ...  # 0x4c
        Swaziland: QLocale.Country = ...  # 0x4c
        Ethiopia: QLocale.Country = ...  # 0x4d
        Europe: QLocale.Country = ...  # 0x4e
        EuropeanUnion: QLocale.Country = ...  # 0x4f
        FalklandIslands: QLocale.Country = ...  # 0x50
        FaroeIslands: QLocale.Country = ...  # 0x51
        Fiji: QLocale.Country = ...  # 0x52
        Finland: QLocale.Country = ...  # 0x53
        France: QLocale.Country = ...  # 0x54
        FrenchGuiana: QLocale.Country = ...  # 0x55
        FrenchPolynesia: QLocale.Country = ...  # 0x56
        FrenchSouthernTerritories: QLocale.Country = ...  # 0x57
        Gabon: QLocale.Country = ...  # 0x58
        Gambia: QLocale.Country = ...  # 0x59
        Georgia: QLocale.Country = ...  # 0x5a
        Germany: QLocale.Country = ...  # 0x5b
        Ghana: QLocale.Country = ...  # 0x5c
        Gibraltar: QLocale.Country = ...  # 0x5d
        Greece: QLocale.Country = ...  # 0x5e
        Greenland: QLocale.Country = ...  # 0x5f
        Grenada: QLocale.Country = ...  # 0x60
        Guadeloupe: QLocale.Country = ...  # 0x61
        Guam: QLocale.Country = ...  # 0x62
        Guatemala: QLocale.Country = ...  # 0x63
        Guernsey: QLocale.Country = ...  # 0x64
        GuineaBissau: QLocale.Country = ...  # 0x65
        Guinea: QLocale.Country = ...  # 0x66
        Guyana: QLocale.Country = ...  # 0x67
        Haiti: QLocale.Country = ...  # 0x68
        HeardAndMcDonaldIslands: QLocale.Country = ...  # 0x69
        Honduras: QLocale.Country = ...  # 0x6a
        HongKong: QLocale.Country = ...  # 0x6b
        Hungary: QLocale.Country = ...  # 0x6c
        Iceland: QLocale.Country = ...  # 0x6d
        India: QLocale.Country = ...  # 0x6e
        Indonesia: QLocale.Country = ...  # 0x6f
        Iran: QLocale.Country = ...  # 0x70
        Iraq: QLocale.Country = ...  # 0x71
        Ireland: QLocale.Country = ...  # 0x72
        IsleOfMan: QLocale.Country = ...  # 0x73
        Israel: QLocale.Country = ...  # 0x74
        Italy: QLocale.Country = ...  # 0x75
        IvoryCoast: QLocale.Country = ...  # 0x76
        Jamaica: QLocale.Country = ...  # 0x77
        Japan: QLocale.Country = ...  # 0x78
        Jersey: QLocale.Country = ...  # 0x79
        Jordan: QLocale.Country = ...  # 0x7a
        Kazakhstan: QLocale.Country = ...  # 0x7b
        Kenya: QLocale.Country = ...  # 0x7c
        Kiribati: QLocale.Country = ...  # 0x7d
        Kosovo: QLocale.Country = ...  # 0x7e
        Kuwait: QLocale.Country = ...  # 0x7f
        Kyrgyzstan: QLocale.Country = ...  # 0x80
        Laos: QLocale.Country = ...  # 0x81
        LatinAmerica: QLocale.Country = ...  # 0x82
        LatinAmericaAndTheCaribbean: QLocale.Country = ...  # 0x82
        Latvia: QLocale.Country = ...  # 0x83
        Lebanon: QLocale.Country = ...  # 0x84
        Lesotho: QLocale.Country = ...  # 0x85
        Liberia: QLocale.Country = ...  # 0x86
        Libya: QLocale.Country = ...  # 0x87
        Liechtenstein: QLocale.Country = ...  # 0x88
        Lithuania: QLocale.Country = ...  # 0x89
        Luxembourg: QLocale.Country = ...  # 0x8a
        Macao: QLocale.Country = ...  # 0x8b
        Macau: QLocale.Country = ...  # 0x8b
        Macedonia: QLocale.Country = ...  # 0x8c
        Madagascar: QLocale.Country = ...  # 0x8d
        Malawi: QLocale.Country = ...  # 0x8e
        Malaysia: QLocale.Country = ...  # 0x8f
        Maldives: QLocale.Country = ...  # 0x90
        Mali: QLocale.Country = ...  # 0x91
        Malta: QLocale.Country = ...  # 0x92
        MarshallIslands: QLocale.Country = ...  # 0x93
        Martinique: QLocale.Country = ...  # 0x94
        Mauritania: QLocale.Country = ...  # 0x95
        Mauritius: QLocale.Country = ...  # 0x96
        Mayotte: QLocale.Country = ...  # 0x97
        Mexico: QLocale.Country = ...  # 0x98
        Micronesia: QLocale.Country = ...  # 0x99
        Moldova: QLocale.Country = ...  # 0x9a
        Monaco: QLocale.Country = ...  # 0x9b
        Mongolia: QLocale.Country = ...  # 0x9c
        Montenegro: QLocale.Country = ...  # 0x9d
        Montserrat: QLocale.Country = ...  # 0x9e
        Morocco: QLocale.Country = ...  # 0x9f
        Mozambique: QLocale.Country = ...  # 0xa0
        Myanmar: QLocale.Country = ...  # 0xa1
        Namibia: QLocale.Country = ...  # 0xa2
        NauruCountry: QLocale.Country = ...  # 0xa3
        NauruTerritory: QLocale.Country = ...  # 0xa3
        Nepal: QLocale.Country = ...  # 0xa4
        Netherlands: QLocale.Country = ...  # 0xa5
        NewCaledonia: QLocale.Country = ...  # 0xa6
        NewZealand: QLocale.Country = ...  # 0xa7
        Nicaragua: QLocale.Country = ...  # 0xa8
        Nigeria: QLocale.Country = ...  # 0xa9
        Niger: QLocale.Country = ...  # 0xaa
        Niue: QLocale.Country = ...  # 0xab
        NorfolkIsland: QLocale.Country = ...  # 0xac
        NorthernMarianaIslands: QLocale.Country = ...  # 0xad
        DemocraticRepublicOfKorea: QLocale.Country = ...  # 0xae
        NorthKorea: QLocale.Country = ...  # 0xae
        Norway: QLocale.Country = ...  # 0xaf
        Oman: QLocale.Country = ...  # 0xb0
        OutlyingOceania: QLocale.Country = ...  # 0xb1
        Pakistan: QLocale.Country = ...  # 0xb2
        Palau: QLocale.Country = ...  # 0xb3
        PalestinianTerritories: QLocale.Country = ...  # 0xb4
        Panama: QLocale.Country = ...  # 0xb5
        PapuaNewGuinea: QLocale.Country = ...  # 0xb6
        Paraguay: QLocale.Country = ...  # 0xb7
        Peru: QLocale.Country = ...  # 0xb8
        Philippines: QLocale.Country = ...  # 0xb9
        Pitcairn: QLocale.Country = ...  # 0xba
        Poland: QLocale.Country = ...  # 0xbb
        Portugal: QLocale.Country = ...  # 0xbc
        PuertoRico: QLocale.Country = ...  # 0xbd
        Qatar: QLocale.Country = ...  # 0xbe
        Reunion: QLocale.Country = ...  # 0xbf
        Romania: QLocale.Country = ...  # 0xc0
        Russia: QLocale.Country = ...  # 0xc1
        RussianFederation: QLocale.Country = ...  # 0xc1
        Rwanda: QLocale.Country = ...  # 0xc2
        SaintBarthelemy: QLocale.Country = ...  # 0xc3
        SaintHelena: QLocale.Country = ...  # 0xc4
        SaintKittsAndNevis: QLocale.Country = ...  # 0xc5
        SaintLucia: QLocale.Country = ...  # 0xc6
        SaintMartin: QLocale.Country = ...  # 0xc7
        SaintPierreAndMiquelon: QLocale.Country = ...  # 0xc8
        SaintVincentAndGrenadines: QLocale.Country = ...  # 0xc9
        SaintVincentAndTheGrenadines: QLocale.Country = ...  # 0xc9
        Samoa: QLocale.Country = ...  # 0xca
        SanMarino: QLocale.Country = ...  # 0xcb
        SaoTomeAndPrincipe: QLocale.Country = ...  # 0xcc
        SaudiArabia: QLocale.Country = ...  # 0xcd
        Senegal: QLocale.Country = ...  # 0xce
        Serbia: QLocale.Country = ...  # 0xcf
        Seychelles: QLocale.Country = ...  # 0xd0
        SierraLeone: QLocale.Country = ...  # 0xd1
        Singapore: QLocale.Country = ...  # 0xd2
        SintMaarten: QLocale.Country = ...  # 0xd3
        Slovakia: QLocale.Country = ...  # 0xd4
        Slovenia: QLocale.Country = ...  # 0xd5
        SolomonIslands: QLocale.Country = ...  # 0xd6
        Somalia: QLocale.Country = ...  # 0xd7
        SouthAfrica: QLocale.Country = ...  # 0xd8
        SouthGeorgiaAndSouthSandwichIslands: QLocale.Country = ...  # 0xd9
        SouthGeorgiaAndTheSouthSandwichIslands: QLocale.Country = ...  # 0xd9
        RepublicOfKorea: QLocale.Country = ...  # 0xda
        SouthKorea: QLocale.Country = ...  # 0xda
        SouthSudan: QLocale.Country = ...  # 0xdb
        Spain: QLocale.Country = ...  # 0xdc
        SriLanka: QLocale.Country = ...  # 0xdd
        Sudan: QLocale.Country = ...  # 0xde
        Suriname: QLocale.Country = ...  # 0xdf
        SvalbardAndJanMayen: QLocale.Country = ...  # 0xe0
        SvalbardAndJanMayenIslands: QLocale.Country = ...  # 0xe0
        Sweden: QLocale.Country = ...  # 0xe1
        Switzerland: QLocale.Country = ...  # 0xe2
        Syria: QLocale.Country = ...  # 0xe3
        SyrianArabRepublic: QLocale.Country = ...  # 0xe3
        Taiwan: QLocale.Country = ...  # 0xe4
        Tajikistan: QLocale.Country = ...  # 0xe5
        Tanzania: QLocale.Country = ...  # 0xe6
        Thailand: QLocale.Country = ...  # 0xe7
        EastTimor: QLocale.Country = ...  # 0xe8
        TimorLeste: QLocale.Country = ...  # 0xe8
        Togo: QLocale.Country = ...  # 0xe9
        TokelauCountry: QLocale.Country = ...  # 0xea
        TokelauTerritory: QLocale.Country = ...  # 0xea
        Tonga: QLocale.Country = ...  # 0xeb
        TrinidadAndTobago: QLocale.Country = ...  # 0xec
        TristanDaCunha: QLocale.Country = ...  # 0xed
        Tunisia: QLocale.Country = ...  # 0xee
        Turkey: QLocale.Country = ...  # 0xef
        Turkmenistan: QLocale.Country = ...  # 0xf0
        TurksAndCaicosIslands: QLocale.Country = ...  # 0xf1
        TuvaluCountry: QLocale.Country = ...  # 0xf2
        TuvaluTerritory: QLocale.Country = ...  # 0xf2
        Uganda: QLocale.Country = ...  # 0xf3
        Ukraine: QLocale.Country = ...  # 0xf4
        UnitedArabEmirates: QLocale.Country = ...  # 0xf5
        UnitedKingdom: QLocale.Country = ...  # 0xf6
        UnitedStatesMinorOutlyingIslands: QLocale.Country = ...  # 0xf7
        UnitedStatesOutlyingIslands: QLocale.Country = ...  # 0xf7
        UnitedStates: QLocale.Country = ...  # 0xf8
        UnitedStatesVirginIslands: QLocale.Country = ...  # 0xf9
        Uruguay: QLocale.Country = ...  # 0xfa
        Uzbekistan: QLocale.Country = ...  # 0xfb
        Vanuatu: QLocale.Country = ...  # 0xfc
        VaticanCity: QLocale.Country = ...  # 0xfd
        VaticanCityState: QLocale.Country = ...  # 0xfd
        Venezuela: QLocale.Country = ...  # 0xfe
        Vietnam: QLocale.Country = ...  # 0xff
        WallisAndFutuna: QLocale.Country = ...  # 0x100
        WallisAndFutunaIslands: QLocale.Country = ...  # 0x100
        WesternSahara: QLocale.Country = ...  # 0x101
        World: QLocale.Country = ...  # 0x102
        Yemen: QLocale.Country = ...  # 0x103
        Zambia: QLocale.Country = ...  # 0x104
        LastCountry: QLocale.Country = ...  # 0x105
        LastTerritory: QLocale.Country = ...  # 0x105
        Zimbabwe: QLocale.Country = ...  # 0x105
    class CurrencySymbolFormat(Enum):

        CurrencyIsoCode: QLocale.CurrencySymbolFormat = ...  # 0x0
        CurrencySymbol: QLocale.CurrencySymbolFormat = ...  # 0x1
        CurrencyDisplayName: QLocale.CurrencySymbolFormat = ...  # 0x2
    class DataSizeFormat(Enum):

        DataSizeIecFormat: QLocale.DataSizeFormat = ...  # 0x0
        DataSizeBase1000: QLocale.DataSizeFormat = ...  # 0x1
        DataSizeSIQuantifiers: QLocale.DataSizeFormat = ...  # 0x2
        DataSizeTraditionalFormat: QLocale.DataSizeFormat = ...  # 0x2
        DataSizeSIFormat: QLocale.DataSizeFormat = ...  # 0x3
    class DataSizeFormats(object): ...
    class FloatingPointPrecisionOption(Enum):

        FloatingPointShortest: QLocale.FloatingPointPrecisionOption = ...  # -0x80
    class FormatType(Enum):

        LongFormat: QLocale.FormatType = ...  # 0x0
        ShortFormat: QLocale.FormatType = ...  # 0x1
        NarrowFormat: QLocale.FormatType = ...  # 0x2
    class Language(Enum):

        AnyLanguage: QLocale.Language = ...  # 0x0
        C: QLocale.Language = ...  # 0x1
        Abkhazian: QLocale.Language = ...  # 0x2
        Afar: QLocale.Language = ...  # 0x3
        Afrikaans: QLocale.Language = ...  # 0x4
        Aghem: QLocale.Language = ...  # 0x5
        Akan: QLocale.Language = ...  # 0x6
        Akkadian: QLocale.Language = ...  # 0x7
        Akoose: QLocale.Language = ...  # 0x8
        Albanian: QLocale.Language = ...  # 0x9
        AmericanSignLanguage: QLocale.Language = ...  # 0xa
        Amharic: QLocale.Language = ...  # 0xb
        AncientEgyptian: QLocale.Language = ...  # 0xc
        AncientGreek: QLocale.Language = ...  # 0xd
        Arabic: QLocale.Language = ...  # 0xe
        Aragonese: QLocale.Language = ...  # 0xf
        Aramaic: QLocale.Language = ...  # 0x10
        Armenian: QLocale.Language = ...  # 0x11
        Assamese: QLocale.Language = ...  # 0x12
        Asturian: QLocale.Language = ...  # 0x13
        Asu: QLocale.Language = ...  # 0x14
        Atsam: QLocale.Language = ...  # 0x15
        Avaric: QLocale.Language = ...  # 0x16
        Avestan: QLocale.Language = ...  # 0x17
        Aymara: QLocale.Language = ...  # 0x18
        Azerbaijani: QLocale.Language = ...  # 0x19
        Bafia: QLocale.Language = ...  # 0x1a
        Balinese: QLocale.Language = ...  # 0x1b
        Bambara: QLocale.Language = ...  # 0x1c
        Bamun: QLocale.Language = ...  # 0x1d
        Bangla: QLocale.Language = ...  # 0x1e
        Bengali: QLocale.Language = ...  # 0x1e
        Basaa: QLocale.Language = ...  # 0x1f
        Bashkir: QLocale.Language = ...  # 0x20
        Basque: QLocale.Language = ...  # 0x21
        BatakToba: QLocale.Language = ...  # 0x22
        Belarusian: QLocale.Language = ...  # 0x23
        Byelorussian: QLocale.Language = ...  # 0x23
        Bemba: QLocale.Language = ...  # 0x24
        Bena: QLocale.Language = ...  # 0x25
        Bhojpuri: QLocale.Language = ...  # 0x26
        Bislama: QLocale.Language = ...  # 0x27
        Blin: QLocale.Language = ...  # 0x28
        Bodo: QLocale.Language = ...  # 0x29
        Bosnian: QLocale.Language = ...  # 0x2a
        Breton: QLocale.Language = ...  # 0x2b
        Buginese: QLocale.Language = ...  # 0x2c
        Bulgarian: QLocale.Language = ...  # 0x2d
        Burmese: QLocale.Language = ...  # 0x2e
        Cantonese: QLocale.Language = ...  # 0x2f
        Catalan: QLocale.Language = ...  # 0x30
        Cebuano: QLocale.Language = ...  # 0x31
        CentralAtlasTamazight: QLocale.Language = ...  # 0x32
        CentralMoroccoTamazight: QLocale.Language = ...  # 0x32
        CentralKurdish: QLocale.Language = ...  # 0x33
        Chakma: QLocale.Language = ...  # 0x34
        Chamorro: QLocale.Language = ...  # 0x35
        Chechen: QLocale.Language = ...  # 0x36
        Cherokee: QLocale.Language = ...  # 0x37
        Chickasaw: QLocale.Language = ...  # 0x38
        Chiga: QLocale.Language = ...  # 0x39
        Chinese: QLocale.Language = ...  # 0x3a
        Church: QLocale.Language = ...  # 0x3b
        Chuvash: QLocale.Language = ...  # 0x3c
        Colognian: QLocale.Language = ...  # 0x3d
        Coptic: QLocale.Language = ...  # 0x3e
        Cornish: QLocale.Language = ...  # 0x3f
        Corsican: QLocale.Language = ...  # 0x40
        Cree: QLocale.Language = ...  # 0x41
        Croatian: QLocale.Language = ...  # 0x42
        Czech: QLocale.Language = ...  # 0x43
        Danish: QLocale.Language = ...  # 0x44
        Divehi: QLocale.Language = ...  # 0x45
        Dogri: QLocale.Language = ...  # 0x46
        Duala: QLocale.Language = ...  # 0x47
        Dutch: QLocale.Language = ...  # 0x48
        Bhutani: QLocale.Language = ...  # 0x49
        Dzongkha: QLocale.Language = ...  # 0x49
        Embu: QLocale.Language = ...  # 0x4a
        English: QLocale.Language = ...  # 0x4b
        Erzya: QLocale.Language = ...  # 0x4c
        Esperanto: QLocale.Language = ...  # 0x4d
        Estonian: QLocale.Language = ...  # 0x4e
        Ewe: QLocale.Language = ...  # 0x4f
        Ewondo: QLocale.Language = ...  # 0x50
        Faroese: QLocale.Language = ...  # 0x51
        Fijian: QLocale.Language = ...  # 0x52
        Filipino: QLocale.Language = ...  # 0x53
        Finnish: QLocale.Language = ...  # 0x54
        French: QLocale.Language = ...  # 0x55
        Friulian: QLocale.Language = ...  # 0x56
        Fulah: QLocale.Language = ...  # 0x57
        Gaelic: QLocale.Language = ...  # 0x58
        Ga: QLocale.Language = ...  # 0x59
        Galician: QLocale.Language = ...  # 0x5a
        Ganda: QLocale.Language = ...  # 0x5b
        Geez: QLocale.Language = ...  # 0x5c
        Georgian: QLocale.Language = ...  # 0x5d
        German: QLocale.Language = ...  # 0x5e
        Gothic: QLocale.Language = ...  # 0x5f
        Greek: QLocale.Language = ...  # 0x60
        Guarani: QLocale.Language = ...  # 0x61
        Gujarati: QLocale.Language = ...  # 0x62
        Gusii: QLocale.Language = ...  # 0x63
        Haitian: QLocale.Language = ...  # 0x64
        Hausa: QLocale.Language = ...  # 0x65
        Hawaiian: QLocale.Language = ...  # 0x66
        Hebrew: QLocale.Language = ...  # 0x67
        Herero: QLocale.Language = ...  # 0x68
        Hindi: QLocale.Language = ...  # 0x69
        HiriMotu: QLocale.Language = ...  # 0x6a
        Hungarian: QLocale.Language = ...  # 0x6b
        Icelandic: QLocale.Language = ...  # 0x6c
        Ido: QLocale.Language = ...  # 0x6d
        Igbo: QLocale.Language = ...  # 0x6e
        InariSami: QLocale.Language = ...  # 0x6f
        Indonesian: QLocale.Language = ...  # 0x70
        Ingush: QLocale.Language = ...  # 0x71
        Interlingua: QLocale.Language = ...  # 0x72
        Interlingue: QLocale.Language = ...  # 0x73
        Inuktitut: QLocale.Language = ...  # 0x74
        Inupiak: QLocale.Language = ...  # 0x75
        Inupiaq: QLocale.Language = ...  # 0x75
        Irish: QLocale.Language = ...  # 0x76
        Italian: QLocale.Language = ...  # 0x77
        Japanese: QLocale.Language = ...  # 0x78
        Javanese: QLocale.Language = ...  # 0x79
        Jju: QLocale.Language = ...  # 0x7a
        JolaFonyi: QLocale.Language = ...  # 0x7b
        Kabuverdianu: QLocale.Language = ...  # 0x7c
        Kabyle: QLocale.Language = ...  # 0x7d
        Kako: QLocale.Language = ...  # 0x7e
        Greenlandic: QLocale.Language = ...  # 0x7f
        Kalaallisut: QLocale.Language = ...  # 0x7f
        Kalenjin: QLocale.Language = ...  # 0x80
        Kamba: QLocale.Language = ...  # 0x81
        Kannada: QLocale.Language = ...  # 0x82
        Kanuri: QLocale.Language = ...  # 0x83
        Kashmiri: QLocale.Language = ...  # 0x84
        Kazakh: QLocale.Language = ...  # 0x85
        Kenyang: QLocale.Language = ...  # 0x86
        Cambodian: QLocale.Language = ...  # 0x87
        Khmer: QLocale.Language = ...  # 0x87
        Kiche: QLocale.Language = ...  # 0x88
        Kikuyu: QLocale.Language = ...  # 0x89
        Kinyarwanda: QLocale.Language = ...  # 0x8a
        Komi: QLocale.Language = ...  # 0x8b
        Kongo: QLocale.Language = ...  # 0x8c
        Konkani: QLocale.Language = ...  # 0x8d
        Korean: QLocale.Language = ...  # 0x8e
        Koro: QLocale.Language = ...  # 0x8f
        KoyraboroSenni: QLocale.Language = ...  # 0x90
        KoyraChiini: QLocale.Language = ...  # 0x91
        Kpelle: QLocale.Language = ...  # 0x92
        Kuanyama: QLocale.Language = ...  # 0x93
        Kwanyama: QLocale.Language = ...  # 0x93
        Kurdish: QLocale.Language = ...  # 0x94
        Kwasio: QLocale.Language = ...  # 0x95
        Kirghiz: QLocale.Language = ...  # 0x96
        Kyrgyz: QLocale.Language = ...  # 0x96
        Lakota: QLocale.Language = ...  # 0x97
        Langi: QLocale.Language = ...  # 0x98
        Lao: QLocale.Language = ...  # 0x99
        Latin: QLocale.Language = ...  # 0x9a
        Latvian: QLocale.Language = ...  # 0x9b
        Lezghian: QLocale.Language = ...  # 0x9c
        Limburgish: QLocale.Language = ...  # 0x9d
        Lingala: QLocale.Language = ...  # 0x9e
        LiteraryChinese: QLocale.Language = ...  # 0x9f
        Lithuanian: QLocale.Language = ...  # 0xa0
        Lojban: QLocale.Language = ...  # 0xa1
        LowerSorbian: QLocale.Language = ...  # 0xa2
        LowGerman: QLocale.Language = ...  # 0xa3
        LubaKatanga: QLocale.Language = ...  # 0xa4
        LuleSami: QLocale.Language = ...  # 0xa5
        Luo: QLocale.Language = ...  # 0xa6
        Luxembourgish: QLocale.Language = ...  # 0xa7
        Luyia: QLocale.Language = ...  # 0xa8
        Macedonian: QLocale.Language = ...  # 0xa9
        Machame: QLocale.Language = ...  # 0xaa
        Maithili: QLocale.Language = ...  # 0xab
        MakhuwaMeetto: QLocale.Language = ...  # 0xac
        Makonde: QLocale.Language = ...  # 0xad
        Malagasy: QLocale.Language = ...  # 0xae
        Malayalam: QLocale.Language = ...  # 0xaf
        Malay: QLocale.Language = ...  # 0xb0
        Maltese: QLocale.Language = ...  # 0xb1
        Mandingo: QLocale.Language = ...  # 0xb2
        Manipuri: QLocale.Language = ...  # 0xb3
        Manx: QLocale.Language = ...  # 0xb4
        Maori: QLocale.Language = ...  # 0xb5
        Mapuche: QLocale.Language = ...  # 0xb6
        Marathi: QLocale.Language = ...  # 0xb7
        Marshallese: QLocale.Language = ...  # 0xb8
        Masai: QLocale.Language = ...  # 0xb9
        Mazanderani: QLocale.Language = ...  # 0xba
        Mende: QLocale.Language = ...  # 0xbb
        Meru: QLocale.Language = ...  # 0xbc
        Meta: QLocale.Language = ...  # 0xbd
        Mohawk: QLocale.Language = ...  # 0xbe
        Mongolian: QLocale.Language = ...  # 0xbf
        Morisyen: QLocale.Language = ...  # 0xc0
        Mundang: QLocale.Language = ...  # 0xc1
        Muscogee: QLocale.Language = ...  # 0xc2
        Nama: QLocale.Language = ...  # 0xc3
        NauruLanguage: QLocale.Language = ...  # 0xc4
        Navaho: QLocale.Language = ...  # 0xc5
        Navajo: QLocale.Language = ...  # 0xc5
        Ndonga: QLocale.Language = ...  # 0xc6
        Nepali: QLocale.Language = ...  # 0xc7
        Newari: QLocale.Language = ...  # 0xc8
        Ngiemboon: QLocale.Language = ...  # 0xc9
        Ngomba: QLocale.Language = ...  # 0xca
        NigerianPidgin: QLocale.Language = ...  # 0xcb
        Nko: QLocale.Language = ...  # 0xcc
        NorthernLuri: QLocale.Language = ...  # 0xcd
        NorthernSami: QLocale.Language = ...  # 0xce
        NorthernSotho: QLocale.Language = ...  # 0xcf
        NorthNdebele: QLocale.Language = ...  # 0xd0
        NorwegianBokmal: QLocale.Language = ...  # 0xd1
        NorwegianNynorsk: QLocale.Language = ...  # 0xd2
        Nuer: QLocale.Language = ...  # 0xd3
        Chewa: QLocale.Language = ...  # 0xd4
        Nyanja: QLocale.Language = ...  # 0xd4
        Nyankole: QLocale.Language = ...  # 0xd5
        Occitan: QLocale.Language = ...  # 0xd6
        Odia: QLocale.Language = ...  # 0xd7
        Oriya: QLocale.Language = ...  # 0xd7
        Ojibwa: QLocale.Language = ...  # 0xd8
        OldIrish: QLocale.Language = ...  # 0xd9
        OldNorse: QLocale.Language = ...  # 0xda
        OldPersian: QLocale.Language = ...  # 0xdb
        Afan: QLocale.Language = ...  # 0xdc
        Oromo: QLocale.Language = ...  # 0xdc
        Osage: QLocale.Language = ...  # 0xdd
        Ossetic: QLocale.Language = ...  # 0xde
        Pahlavi: QLocale.Language = ...  # 0xdf
        Palauan: QLocale.Language = ...  # 0xe0
        Pali: QLocale.Language = ...  # 0xe1
        Papiamento: QLocale.Language = ...  # 0xe2
        Pashto: QLocale.Language = ...  # 0xe3
        Persian: QLocale.Language = ...  # 0xe4
        Phoenician: QLocale.Language = ...  # 0xe5
        Polish: QLocale.Language = ...  # 0xe6
        Portuguese: QLocale.Language = ...  # 0xe7
        Prussian: QLocale.Language = ...  # 0xe8
        Punjabi: QLocale.Language = ...  # 0xe9
        Quechua: QLocale.Language = ...  # 0xea
        Romanian: QLocale.Language = ...  # 0xeb
        RhaetoRomance: QLocale.Language = ...  # 0xec
        Romansh: QLocale.Language = ...  # 0xec
        Rombo: QLocale.Language = ...  # 0xed
        Kurundi: QLocale.Language = ...  # 0xee
        Rundi: QLocale.Language = ...  # 0xee
        Russian: QLocale.Language = ...  # 0xef
        Rwa: QLocale.Language = ...  # 0xf0
        Saho: QLocale.Language = ...  # 0xf1
        Sakha: QLocale.Language = ...  # 0xf2
        Samburu: QLocale.Language = ...  # 0xf3
        Samoan: QLocale.Language = ...  # 0xf4
        Sango: QLocale.Language = ...  # 0xf5
        Sangu: QLocale.Language = ...  # 0xf6
        Sanskrit: QLocale.Language = ...  # 0xf7
        Santali: QLocale.Language = ...  # 0xf8
        Sardinian: QLocale.Language = ...  # 0xf9
        Saurashtra: QLocale.Language = ...  # 0xfa
        Sena: QLocale.Language = ...  # 0xfb
        Serbian: QLocale.Language = ...  # 0xfc
        Shambala: QLocale.Language = ...  # 0xfd
        Shona: QLocale.Language = ...  # 0xfe
        SichuanYi: QLocale.Language = ...  # 0xff
        Sicilian: QLocale.Language = ...  # 0x100
        Sidamo: QLocale.Language = ...  # 0x101
        Silesian: QLocale.Language = ...  # 0x102
        Sindhi: QLocale.Language = ...  # 0x103
        Sinhala: QLocale.Language = ...  # 0x104
        SkoltSami: QLocale.Language = ...  # 0x105
        Slovak: QLocale.Language = ...  # 0x106
        Slovenian: QLocale.Language = ...  # 0x107
        Soga: QLocale.Language = ...  # 0x108
        Somali: QLocale.Language = ...  # 0x109
        SouthernKurdish: QLocale.Language = ...  # 0x10a
        SouthernSami: QLocale.Language = ...  # 0x10b
        SouthernSotho: QLocale.Language = ...  # 0x10c
        SouthNdebele: QLocale.Language = ...  # 0x10d
        Spanish: QLocale.Language = ...  # 0x10e
        StandardMoroccanTamazight: QLocale.Language = ...  # 0x10f
        Sundanese: QLocale.Language = ...  # 0x110
        Swahili: QLocale.Language = ...  # 0x111
        Swati: QLocale.Language = ...  # 0x112
        Swedish: QLocale.Language = ...  # 0x113
        SwissGerman: QLocale.Language = ...  # 0x114
        Syriac: QLocale.Language = ...  # 0x115
        Tachelhit: QLocale.Language = ...  # 0x116
        Tahitian: QLocale.Language = ...  # 0x117
        TaiDam: QLocale.Language = ...  # 0x118
        Taita: QLocale.Language = ...  # 0x119
        Tajik: QLocale.Language = ...  # 0x11a
        Tamil: QLocale.Language = ...  # 0x11b
        Taroko: QLocale.Language = ...  # 0x11c
        Tasawaq: QLocale.Language = ...  # 0x11d
        Tatar: QLocale.Language = ...  # 0x11e
        Telugu: QLocale.Language = ...  # 0x11f
        Teso: QLocale.Language = ...  # 0x120
        Thai: QLocale.Language = ...  # 0x121
        Tibetan: QLocale.Language = ...  # 0x122
        Tigre: QLocale.Language = ...  # 0x123
        Tigrinya: QLocale.Language = ...  # 0x124
        TokelauLanguage: QLocale.Language = ...  # 0x125
        TokPisin: QLocale.Language = ...  # 0x126
        Tongan: QLocale.Language = ...  # 0x127
        Tsonga: QLocale.Language = ...  # 0x128
        Tswana: QLocale.Language = ...  # 0x129
        Turkish: QLocale.Language = ...  # 0x12a
        Turkmen: QLocale.Language = ...  # 0x12b
        TuvaluLanguage: QLocale.Language = ...  # 0x12c
        Tyap: QLocale.Language = ...  # 0x12d
        Ugaritic: QLocale.Language = ...  # 0x12e
        Ukrainian: QLocale.Language = ...  # 0x12f
        UpperSorbian: QLocale.Language = ...  # 0x130
        Urdu: QLocale.Language = ...  # 0x131
        Uighur: QLocale.Language = ...  # 0x132
        Uigur: QLocale.Language = ...  # 0x132
        Uyghur: QLocale.Language = ...  # 0x132
        Uzbek: QLocale.Language = ...  # 0x133
        Vai: QLocale.Language = ...  # 0x134
        Venda: QLocale.Language = ...  # 0x135
        Vietnamese: QLocale.Language = ...  # 0x136
        Volapuk: QLocale.Language = ...  # 0x137
        Vunjo: QLocale.Language = ...  # 0x138
        Walloon: QLocale.Language = ...  # 0x139
        Walser: QLocale.Language = ...  # 0x13a
        Warlpiri: QLocale.Language = ...  # 0x13b
        Welsh: QLocale.Language = ...  # 0x13c
        WesternBalochi: QLocale.Language = ...  # 0x13d
        Frisian: QLocale.Language = ...  # 0x13e
        WesternFrisian: QLocale.Language = ...  # 0x13e
        Walamo: QLocale.Language = ...  # 0x13f
        Wolaytta: QLocale.Language = ...  # 0x13f
        Wolof: QLocale.Language = ...  # 0x140
        Xhosa: QLocale.Language = ...  # 0x141
        Yangben: QLocale.Language = ...  # 0x142
        Yiddish: QLocale.Language = ...  # 0x143
        Yoruba: QLocale.Language = ...  # 0x144
        Zarma: QLocale.Language = ...  # 0x145
        Zhuang: QLocale.Language = ...  # 0x146
        LastLanguage: QLocale.Language = ...  # 0x147
        Zulu: QLocale.Language = ...  # 0x147
    class MeasurementSystem(Enum):

        MetricSystem: QLocale.MeasurementSystem = ...  # 0x0
        ImperialSystem: QLocale.MeasurementSystem = ...  # 0x1
        ImperialUSSystem: QLocale.MeasurementSystem = ...  # 0x1
        ImperialUKSystem: QLocale.MeasurementSystem = ...  # 0x2
    class NumberOption(Enum):

        DefaultNumberOptions: QLocale.NumberOption = ...  # 0x0
        OmitGroupSeparator: QLocale.NumberOption = ...  # 0x1
        RejectGroupSeparator: QLocale.NumberOption = ...  # 0x2
        OmitLeadingZeroInExponent: QLocale.NumberOption = ...  # 0x4
        RejectLeadingZeroInExponent: QLocale.NumberOption = ...  # 0x8
        IncludeTrailingZeroesAfterDot: QLocale.NumberOption = ...  # 0x10
        RejectTrailingZeroesAfterDot: QLocale.NumberOption = ...  # 0x20
    class NumberOptions(object): ...
    class QuotationStyle(Enum):

        StandardQuotation: QLocale.QuotationStyle = ...  # 0x0
        AlternateQuotation: QLocale.QuotationStyle = ...  # 0x1
    class Script(Enum):

        AnyScript: QLocale.Script = ...  # 0x0
        AdlamScript: QLocale.Script = ...  # 0x1
        AhomScript: QLocale.Script = ...  # 0x2
        AnatolianHieroglyphsScript: QLocale.Script = ...  # 0x3
        ArabicScript: QLocale.Script = ...  # 0x4
        ArmenianScript: QLocale.Script = ...  # 0x5
        AvestanScript: QLocale.Script = ...  # 0x6
        BalineseScript: QLocale.Script = ...  # 0x7
        BamumScript: QLocale.Script = ...  # 0x8
        BanglaScript: QLocale.Script = ...  # 0x9
        BengaliScript: QLocale.Script = ...  # 0x9
        BassaVahScript: QLocale.Script = ...  # 0xa
        BatakScript: QLocale.Script = ...  # 0xb
        BhaiksukiScript: QLocale.Script = ...  # 0xc
        BopomofoScript: QLocale.Script = ...  # 0xd
        BrahmiScript: QLocale.Script = ...  # 0xe
        BrailleScript: QLocale.Script = ...  # 0xf
        BugineseScript: QLocale.Script = ...  # 0x10
        BuhidScript: QLocale.Script = ...  # 0x11
        CanadianAboriginalScript: QLocale.Script = ...  # 0x12
        CarianScript: QLocale.Script = ...  # 0x13
        CaucasianAlbanianScript: QLocale.Script = ...  # 0x14
        ChakmaScript: QLocale.Script = ...  # 0x15
        ChamScript: QLocale.Script = ...  # 0x16
        CherokeeScript: QLocale.Script = ...  # 0x17
        CopticScript: QLocale.Script = ...  # 0x18
        CuneiformScript: QLocale.Script = ...  # 0x19
        CypriotScript: QLocale.Script = ...  # 0x1a
        CyrillicScript: QLocale.Script = ...  # 0x1b
        DeseretScript: QLocale.Script = ...  # 0x1c
        DevanagariScript: QLocale.Script = ...  # 0x1d
        DuployanScript: QLocale.Script = ...  # 0x1e
        EgyptianHieroglyphsScript: QLocale.Script = ...  # 0x1f
        ElbasanScript: QLocale.Script = ...  # 0x20
        EthiopicScript: QLocale.Script = ...  # 0x21
        FraserScript: QLocale.Script = ...  # 0x22
        GeorgianScript: QLocale.Script = ...  # 0x23
        GlagoliticScript: QLocale.Script = ...  # 0x24
        GothicScript: QLocale.Script = ...  # 0x25
        GranthaScript: QLocale.Script = ...  # 0x26
        GreekScript: QLocale.Script = ...  # 0x27
        GujaratiScript: QLocale.Script = ...  # 0x28
        GurmukhiScript: QLocale.Script = ...  # 0x29
        HangulScript: QLocale.Script = ...  # 0x2a
        HanScript: QLocale.Script = ...  # 0x2b
        HanunooScript: QLocale.Script = ...  # 0x2c
        HanWithBopomofoScript: QLocale.Script = ...  # 0x2d
        HatranScript: QLocale.Script = ...  # 0x2e
        HebrewScript: QLocale.Script = ...  # 0x2f
        HiraganaScript: QLocale.Script = ...  # 0x30
        ImperialAramaicScript: QLocale.Script = ...  # 0x31
        InscriptionalPahlaviScript: QLocale.Script = ...  # 0x32
        InscriptionalParthianScript: QLocale.Script = ...  # 0x33
        JamoScript: QLocale.Script = ...  # 0x34
        JapaneseScript: QLocale.Script = ...  # 0x35
        JavaneseScript: QLocale.Script = ...  # 0x36
        KaithiScript: QLocale.Script = ...  # 0x37
        KannadaScript: QLocale.Script = ...  # 0x38
        KatakanaScript: QLocale.Script = ...  # 0x39
        KayahLiScript: QLocale.Script = ...  # 0x3a
        KharoshthiScript: QLocale.Script = ...  # 0x3b
        KhmerScript: QLocale.Script = ...  # 0x3c
        KhojkiScript: QLocale.Script = ...  # 0x3d
        KhudawadiScript: QLocale.Script = ...  # 0x3e
        KoreanScript: QLocale.Script = ...  # 0x3f
        LannaScript: QLocale.Script = ...  # 0x40
        LaoScript: QLocale.Script = ...  # 0x41
        LatinScript: QLocale.Script = ...  # 0x42
        LepchaScript: QLocale.Script = ...  # 0x43
        LimbuScript: QLocale.Script = ...  # 0x44
        LinearAScript: QLocale.Script = ...  # 0x45
        LinearBScript: QLocale.Script = ...  # 0x46
        LycianScript: QLocale.Script = ...  # 0x47
        LydianScript: QLocale.Script = ...  # 0x48
        MahajaniScript: QLocale.Script = ...  # 0x49
        MalayalamScript: QLocale.Script = ...  # 0x4a
        MandaeanScript: QLocale.Script = ...  # 0x4b
        ManichaeanScript: QLocale.Script = ...  # 0x4c
        MarchenScript: QLocale.Script = ...  # 0x4d
        MeiteiMayekScript: QLocale.Script = ...  # 0x4e
        MendeKikakuiScript: QLocale.Script = ...  # 0x4f
        MendeScript: QLocale.Script = ...  # 0x4f
        MeroiticCursiveScript: QLocale.Script = ...  # 0x50
        MeroiticScript: QLocale.Script = ...  # 0x51
        ModiScript: QLocale.Script = ...  # 0x52
        MongolianScript: QLocale.Script = ...  # 0x53
        MroScript: QLocale.Script = ...  # 0x54
        MultaniScript: QLocale.Script = ...  # 0x55
        MyanmarScript: QLocale.Script = ...  # 0x56
        NabataeanScript: QLocale.Script = ...  # 0x57
        NewaScript: QLocale.Script = ...  # 0x58
        NewTaiLueScript: QLocale.Script = ...  # 0x59
        NkoScript: QLocale.Script = ...  # 0x5a
        OdiaScript: QLocale.Script = ...  # 0x5b
        OriyaScript: QLocale.Script = ...  # 0x5b
        OghamScript: QLocale.Script = ...  # 0x5c
        OlChikiScript: QLocale.Script = ...  # 0x5d
        OldHungarianScript: QLocale.Script = ...  # 0x5e
        OldItalicScript: QLocale.Script = ...  # 0x5f
        OldNorthArabianScript: QLocale.Script = ...  # 0x60
        OldPermicScript: QLocale.Script = ...  # 0x61
        OldPersianScript: QLocale.Script = ...  # 0x62
        OldSouthArabianScript: QLocale.Script = ...  # 0x63
        OrkhonScript: QLocale.Script = ...  # 0x64
        OsageScript: QLocale.Script = ...  # 0x65
        OsmanyaScript: QLocale.Script = ...  # 0x66
        PahawhHmongScript: QLocale.Script = ...  # 0x67
        PalmyreneScript: QLocale.Script = ...  # 0x68
        PauCinHauScript: QLocale.Script = ...  # 0x69
        PhagsPaScript: QLocale.Script = ...  # 0x6a
        PhoenicianScript: QLocale.Script = ...  # 0x6b
        PollardPhoneticScript: QLocale.Script = ...  # 0x6c
        PsalterPahlaviScript: QLocale.Script = ...  # 0x6d
        RejangScript: QLocale.Script = ...  # 0x6e
        RunicScript: QLocale.Script = ...  # 0x6f
        SamaritanScript: QLocale.Script = ...  # 0x70
        SaurashtraScript: QLocale.Script = ...  # 0x71
        SharadaScript: QLocale.Script = ...  # 0x72
        ShavianScript: QLocale.Script = ...  # 0x73
        SiddhamScript: QLocale.Script = ...  # 0x74
        SignWritingScript: QLocale.Script = ...  # 0x75
        SimplifiedChineseScript: QLocale.Script = ...  # 0x76
        SimplifiedHanScript: QLocale.Script = ...  # 0x76
        SinhalaScript: QLocale.Script = ...  # 0x77
        SoraSompengScript: QLocale.Script = ...  # 0x78
        SundaneseScript: QLocale.Script = ...  # 0x79
        SylotiNagriScript: QLocale.Script = ...  # 0x7a
        SyriacScript: QLocale.Script = ...  # 0x7b
        TagalogScript: QLocale.Script = ...  # 0x7c
        TagbanwaScript: QLocale.Script = ...  # 0x7d
        TaiLeScript: QLocale.Script = ...  # 0x7e
        TaiVietScript: QLocale.Script = ...  # 0x7f
        TakriScript: QLocale.Script = ...  # 0x80
        TamilScript: QLocale.Script = ...  # 0x81
        TangutScript: QLocale.Script = ...  # 0x82
        TeluguScript: QLocale.Script = ...  # 0x83
        ThaanaScript: QLocale.Script = ...  # 0x84
        ThaiScript: QLocale.Script = ...  # 0x85
        TibetanScript: QLocale.Script = ...  # 0x86
        TifinaghScript: QLocale.Script = ...  # 0x87
        TirhutaScript: QLocale.Script = ...  # 0x88
        TraditionalChineseScript: QLocale.Script = ...  # 0x89
        TraditionalHanScript: QLocale.Script = ...  # 0x89
        UgariticScript: QLocale.Script = ...  # 0x8a
        VaiScript: QLocale.Script = ...  # 0x8b
        VarangKshitiScript: QLocale.Script = ...  # 0x8c
        LastScript: QLocale.Script = ...  # 0x8d
        YiScript: QLocale.Script = ...  # 0x8d
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        language: QLocale.Language,
        script: QLocale.Script = ...,
        territory: QLocale.Country = ...,
    ) -> None: ...
    @overload
    def __init__(self, language: QLocale.Language, territory: QLocale.Country) -> None: ...
    @overload
    def __init__(self, name: str) -> None: ...
    @overload
    def __init__(self, other: Union[QLocale, QLocale.Language]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def amText(self) -> str: ...
    def bcp47Name(self) -> str: ...
    @staticmethod
    def c() -> QLocale: ...
    @staticmethod
    def codeToCountry(countryCode: str) -> QLocale.Country: ...
    @staticmethod
    def codeToLanguage(languageCode: str) -> QLocale.Language: ...
    @staticmethod
    def codeToScript(scriptCode: str) -> QLocale.Script: ...
    @staticmethod
    def codeToTerritory(territoryCode: str) -> QLocale.Country: ...
    def collation(self) -> QLocale: ...
    @staticmethod
    def countriesForLanguage(lang: QLocale.Language) -> List[QLocale.Country]: ...
    def country(self) -> QLocale.Country: ...
    @staticmethod
    def countryToCode(country: QLocale.Country) -> str: ...
    @staticmethod
    def countryToString(country: QLocale.Country) -> str: ...
    def createSeparatedList(self, strl: Sequence[str]) -> str: ...
    def currencySymbol(self, arg__1: QLocale.CurrencySymbolFormat = ...) -> str: ...
    def dateFormat(self, format: QLocale.FormatType = ...) -> str: ...
    def dateTimeFormat(self, format: QLocale.FormatType = ...) -> str: ...
    def dayName(self, arg__1: int, format: QLocale.FormatType = ...) -> str: ...
    def decimalPoint(self) -> str: ...
    def exponential(self) -> str: ...
    def firstDayOfWeek(self) -> Qt.DayOfWeek: ...
    def formattedDataSize(
        self, bytes: int, precision: int = ..., format: QLocale.DataSizeFormats = ...
    ) -> str: ...
    def groupSeparator(self) -> str: ...
    def language(self) -> QLocale.Language: ...
    @staticmethod
    def languageToCode(language: QLocale.Language) -> str: ...
    @staticmethod
    def languageToString(language: QLocale.Language) -> str: ...
    @staticmethod
    def matchingLocales(
        language: QLocale.Language, script: QLocale.Script, territory: QLocale.Country
    ) -> List[QLocale]: ...
    def measurementSystem(self) -> QLocale.MeasurementSystem: ...
    def monthName(self, arg__1: int, format: QLocale.FormatType = ...) -> str: ...
    def name(self) -> str: ...
    def nativeCountryName(self) -> str: ...
    def nativeLanguageName(self) -> str: ...
    def nativeTerritoryName(self) -> str: ...
    def negativeSign(self) -> str: ...
    def numberOptions(self) -> QLocale.NumberOptions: ...
    def percent(self) -> str: ...
    def pmText(self) -> str: ...
    def positiveSign(self) -> str: ...
    def quoteString(self, str: str, style: QLocale.QuotationStyle = ...) -> str: ...
    def script(self) -> QLocale.Script: ...
    @staticmethod
    def scriptToCode(script: QLocale.Script) -> str: ...
    @staticmethod
    def scriptToString(script: QLocale.Script) -> str: ...
    @staticmethod
    def setDefault(locale: Union[QLocale, QLocale.Language]) -> None: ...
    def setNumberOptions(self, options: QLocale.NumberOptions) -> None: ...
    def standaloneDayName(self, arg__1: int, format: QLocale.FormatType = ...) -> str: ...
    def standaloneMonthName(self, arg__1: int, format: QLocale.FormatType = ...) -> str: ...
    def swap(self, other: Union[QLocale, QLocale.Language]) -> None: ...
    @staticmethod
    def system() -> QLocale: ...
    def territory(self) -> QLocale.Country: ...
    @staticmethod
    def territoryToCode(territory: QLocale.Country) -> str: ...
    @staticmethod
    def territoryToString(territory: QLocale.Country) -> str: ...
    def textDirection(self) -> Qt.LayoutDirection: ...
    def timeFormat(self, format: QLocale.FormatType = ...) -> str: ...
    @overload
    def toCurrencyString(self, arg__1: float, symbol: str = ..., precision: int = ...) -> str: ...
    @overload
    def toCurrencyString(self, arg__1: int, symbol: str = ...) -> str: ...
    @overload
    def toCurrencyString(self, arg__1: int, symbol: str = ...) -> str: ...
    @overload
    def toCurrencyString(self, i: float, symbol: str = ..., precision: int = ...) -> str: ...
    @overload
    def toCurrencyString(self, i: int, symbol: str = ...) -> str: ...
    @overload
    def toCurrencyString(self, i: int, symbol: str = ...) -> str: ...
    @overload
    def toCurrencyString(self, i: int, symbol: str = ...) -> str: ...
    @overload
    def toCurrencyString(self, i: int, symbol: str = ...) -> str: ...
    @overload
    def toDate(self, string: str, format: QLocale.FormatType, cal: QCalendar) -> QDate: ...
    @overload
    def toDate(self, string: str, format: QLocale.FormatType = ...) -> QDate: ...
    @overload
    def toDate(self, string: str, format: str) -> QDate: ...
    @overload
    def toDate(self, string: str, format: str, cal: QCalendar) -> QDate: ...
    @overload
    def toDateTime(self, string: str, format: QLocale.FormatType, cal: QCalendar) -> QDateTime: ...
    @overload
    def toDateTime(self, string: str, format: QLocale.FormatType = ...) -> QDateTime: ...
    @overload
    def toDateTime(self, string: str, format: str) -> QDateTime: ...
    @overload
    def toDateTime(self, string: str, format: str, cal: QCalendar) -> QDateTime: ...
    @overload
    def toDouble(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toDouble(self, s: str) -> Tuple[float, bool]: ...
    @overload
    def toFloat(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toFloat(self, s: str) -> Tuple[float, bool]: ...
    @overload
    def toInt(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toInt(self, s: str) -> Tuple[int, bool]: ...
    def toLong(self, s: str) -> Tuple[int, bool]: ...
    @overload
    def toLongLong(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toLongLong(self, s: str) -> Tuple[int, bool]: ...
    def toLower(self, str: str) -> str: ...
    @overload
    def toShort(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toShort(self, s: str) -> Tuple[int, bool]: ...
    @overload
    def toString(self, date: QDate, format: QLocale.FormatType, cal: QCalendar) -> str: ...
    @overload
    def toString(self, date: QDate, format: QLocale.FormatType = ...) -> str: ...
    @overload
    def toString(self, date: QDate, format: str) -> str: ...
    @overload
    def toString(self, date: QDate, format: str, cal: QCalendar) -> str: ...
    @overload
    def toString(self, dateTime: QDateTime, format: QLocale.FormatType, cal: QCalendar) -> str: ...
    @overload
    def toString(self, dateTime: QDateTime, format: QLocale.FormatType = ...) -> str: ...
    @overload
    def toString(self, dateTime: QDateTime, format: str) -> str: ...
    @overload
    def toString(self, dateTime: QDateTime, format: str, cal: QCalendar) -> str: ...
    @overload
    def toString(self, f: float, format: int = ..., precision: int = ...) -> str: ...
    @overload
    def toString(self, f: float, format: int = ..., precision: int = ...) -> str: ...
    @overload
    def toString(self, i: int) -> str: ...
    @overload
    def toString(self, i: int) -> str: ...
    @overload
    def toString(self, i: int) -> str: ...
    @overload
    def toString(self, i: int) -> str: ...
    @overload
    def toString(self, i: int) -> str: ...
    @overload
    def toString(self, time: QTime, format: QLocale.FormatType = ...) -> str: ...
    @overload
    def toString(self, time: QTime, format: str) -> str: ...
    @overload
    def toTime(self, string: str, format: QLocale.FormatType = ...) -> QTime: ...
    @overload
    def toTime(self, string: str, format: str) -> QTime: ...
    @overload
    def toUInt(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toUInt(self, s: str) -> Tuple[int, bool]: ...
    def toULong(self, s: str) -> Tuple[int, bool]: ...
    @overload
    def toULongLong(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toULongLong(self, s: str) -> Tuple[int, bool]: ...
    @overload
    def toUShort(self, s: str) -> Tuple[Tuple, bool]: ...
    @overload
    def toUShort(self, s: str) -> Tuple[int, bool]: ...
    def toUpper(self, str: str) -> str: ...
    def uiLanguages(self) -> List[str]: ...
    def weekdays(self) -> List[Qt.DayOfWeek]: ...
    def zeroDigit(self) -> str: ...

class QLockFile(Shiboken.Object):

    NoError: QLockFile.LockError = ...  # 0x0
    LockFailedError: QLockFile.LockError = ...  # 0x1
    PermissionError: QLockFile.LockError = ...  # 0x2
    UnknownError: QLockFile.LockError = ...  # 0x3
    class LockError(Enum):

        NoError: QLockFile.LockError = ...  # 0x0
        LockFailedError: QLockFile.LockError = ...  # 0x1
        PermissionError: QLockFile.LockError = ...  # 0x2
        UnknownError: QLockFile.LockError = ...  # 0x3
    def __init__(self, fileName: str) -> None: ...
    def error(self) -> QLockFile.LockError: ...
    def fileName(self) -> str: ...
    def getLockInfo(self) -> Tuple[bool, int, str, str]: ...
    def isLocked(self) -> bool: ...
    def lock(self) -> bool: ...
    def removeStaleLockFile(self) -> bool: ...
    def setStaleLockTime(self, arg__1: int) -> None: ...
    def staleLockTime(self) -> int: ...
    def tryLock(self, timeout: int = ...) -> bool: ...
    def unlock(self) -> None: ...

class QMargins(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QMargins: QMargins) -> None: ...
    @overload
    def __init__(self, left: int, top: int, right: int, bottom: int) -> None: ...
    @overload
    def __add__(self, lhs: int) -> QMargins: ...
    @overload
    def __add__(self, m2: QMargins) -> QMargins: ...
    @overload
    def __add__(self, rhs: int) -> QMargins: ...
    @staticmethod
    def __copy__() -> None: ...
    @overload
    def __iadd__(self, arg__1: int) -> QMargins: ...
    @overload
    def __iadd__(self, margins: QMargins) -> QMargins: ...
    @overload
    def __imul__(self, arg__1: int) -> QMargins: ...
    @overload
    def __imul__(self, arg__1: float) -> QMargins: ...
    @overload
    def __isub__(self, arg__1: int) -> QMargins: ...
    @overload
    def __isub__(self, margins: QMargins) -> QMargins: ...
    @overload
    def __mul__(self, factor: int) -> QMargins: ...
    @overload
    def __mul__(self, factor: float) -> QMargins: ...
    def __neg__(self) -> QMargins: ...
    def __or__(self, m2: QMargins) -> QMargins: ...
    def __pos__(self) -> QMargins: ...
    @overload
    def __sub__(self, m2: QMargins) -> QMargins: ...
    @overload
    def __sub__(self, rhs: int) -> QMargins: ...
    def bottom(self) -> int: ...
    def isNull(self) -> bool: ...
    def left(self) -> int: ...
    def right(self) -> int: ...
    def setBottom(self, bottom: int) -> None: ...
    def setLeft(self, left: int) -> None: ...
    def setRight(self, right: int) -> None: ...
    def setTop(self, top: int) -> None: ...
    def top(self) -> int: ...

class QMarginsF(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QMarginsF: Union[QMarginsF, QMargins]) -> None: ...
    @overload
    def __init__(self, left: float, top: float, right: float, bottom: float) -> None: ...
    @overload
    def __init__(self, margins: QMargins) -> None: ...
    @overload
    def __add__(self, lhs: float) -> QMarginsF: ...
    @overload
    def __add__(self, rhs: float) -> QMarginsF: ...
    @overload
    def __add__(self, rhs: Union[QMarginsF, QMargins]) -> QMarginsF: ...
    @staticmethod
    def __copy__() -> None: ...
    @overload
    def __iadd__(self, addend: float) -> QMarginsF: ...
    @overload
    def __iadd__(self, margins: Union[QMarginsF, QMargins]) -> QMarginsF: ...
    def __imul__(self, factor: float) -> QMarginsF: ...
    @overload
    def __isub__(self, margins: Union[QMarginsF, QMargins]) -> QMarginsF: ...
    @overload
    def __isub__(self, subtrahend: float) -> QMarginsF: ...
    @overload
    def __mul__(self, lhs: float) -> QMarginsF: ...
    @overload
    def __mul__(self, rhs: float) -> QMarginsF: ...
    def __neg__(self) -> QMarginsF: ...
    def __or__(self, m2: Union[QMarginsF, QMargins]) -> QMarginsF: ...
    def __pos__(self) -> QMarginsF: ...
    @overload
    def __sub__(self, rhs: float) -> QMarginsF: ...
    @overload
    def __sub__(self, rhs: Union[QMarginsF, QMargins]) -> QMarginsF: ...
    def bottom(self) -> float: ...
    def isNull(self) -> bool: ...
    def left(self) -> float: ...
    def right(self) -> float: ...
    def setBottom(self, abottom: float) -> None: ...
    def setLeft(self, aleft: float) -> None: ...
    def setRight(self, aright: float) -> None: ...
    def setTop(self, atop: float) -> None: ...
    def toMargins(self) -> QMargins: ...
    def top(self) -> float: ...

class QMessageAuthenticationCode(Shiboken.Object):
    def __init__(
        self, method: QCryptographicHash.Algorithm, key: Union[QByteArray, bytes] = ...
    ) -> None: ...
    @overload
    def addData(self, data: bytes, length: int) -> None: ...
    @overload
    def addData(self, data: Union[QByteArray, bytes]) -> None: ...
    @overload
    def addData(self, device: QIODevice) -> bool: ...
    @staticmethod
    def hash(
        message: Union[QByteArray, bytes],
        key: Union[QByteArray, bytes],
        method: QCryptographicHash.Algorithm,
    ) -> QByteArray: ...
    def reset(self) -> None: ...
    def result(self) -> QByteArray: ...
    def setKey(self, key: Union[QByteArray, bytes]) -> None: ...

class QMessageLogContext(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, fileName: bytes, lineNumber: int, functionName: bytes, categoryName: bytes
    ) -> None: ...

class QMetaClassInfo(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QMetaClassInfo: QMetaClassInfo) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def name(self) -> bytes: ...
    def value(self) -> bytes: ...

class QMetaEnum(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QMetaEnum: QMetaEnum) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def enumName(self) -> bytes: ...
    def isFlag(self) -> bool: ...
    def isScoped(self) -> bool: ...
    def isValid(self) -> bool: ...
    def key(self, index: int) -> bytes: ...
    def keyCount(self) -> int: ...
    def keyToValue(self, key: bytes) -> Tuple[Tuple, bool]: ...
    def keysToValue(self, keys: bytes) -> Tuple[Tuple, bool]: ...
    def name(self) -> bytes: ...
    def scope(self) -> bytes: ...
    def value(self, index: int) -> int: ...
    def valueToKey(self, value: int) -> bytes: ...
    def valueToKeys(self, value: int) -> QByteArray: ...

class QMetaMethod(Shiboken.Object):

    Private: QMetaMethod.Access = ...  # 0x0
    Protected: QMetaMethod.Access = ...  # 0x1
    Public: QMetaMethod.Access = ...  # 0x2
    Method: QMetaMethod.MethodType = ...  # 0x0
    Signal: QMetaMethod.MethodType = ...  # 0x1
    Slot: QMetaMethod.MethodType = ...  # 0x2
    Constructor: QMetaMethod.MethodType = ...  # 0x3
    class Access(Enum):

        Private: QMetaMethod.Access = ...  # 0x0
        Protected: QMetaMethod.Access = ...  # 0x1
        Public: QMetaMethod.Access = ...  # 0x2
    class MethodType(Enum):

        Method: QMetaMethod.MethodType = ...  # 0x0
        Signal: QMetaMethod.MethodType = ...  # 0x1
        Slot: QMetaMethod.MethodType = ...  # 0x2
        Constructor: QMetaMethod.MethodType = ...  # 0x3
    def __init__(self) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def access(self) -> QMetaMethod.Access: ...
    def enclosingMetaObject(self) -> QMetaObject: ...
    @overload
    def invoke(
        self,
        object: QObject,
        connectionType: Qt.ConnectionType,
        returnValue: QGenericReturnArgument,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    def invoke(
        self,
        object: QObject,
        connectionType: Qt.ConnectionType,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    def invoke(
        self,
        object: QObject,
        returnValue: QGenericReturnArgument,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    def invoke(
        self,
        object: QObject,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    def invokeOnGadget(
        self,
        gadget: int,
        returnValue: QGenericReturnArgument,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    def invokeOnGadget(
        self,
        gadget: int,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    def isConst(self) -> bool: ...
    def isValid(self) -> bool: ...
    def methodIndex(self) -> int: ...
    def methodSignature(self) -> QByteArray: ...
    def methodType(self) -> QMetaMethod.MethodType: ...
    def name(self) -> QByteArray: ...
    def parameterCount(self) -> int: ...
    def parameterMetaType(self, index: int) -> QMetaType: ...
    def parameterNames(self) -> List[QByteArray]: ...
    def parameterType(self, index: int) -> int: ...
    def parameterTypeName(self, index: int) -> QByteArray: ...
    def parameterTypes(self) -> List[QByteArray]: ...
    def relativeMethodIndex(self) -> int: ...
    def returnMetaType(self) -> QMetaType: ...
    def returnType(self) -> int: ...
    def revision(self) -> int: ...
    def tag(self) -> bytes: ...
    def typeName(self) -> bytes: ...

class QMetaObject(Shiboken.Object):

    InvokeMetaMethod: QMetaObject.Call = ...  # 0x0
    ReadProperty: QMetaObject.Call = ...  # 0x1
    WriteProperty: QMetaObject.Call = ...  # 0x2
    ResetProperty: QMetaObject.Call = ...  # 0x3
    CreateInstance: QMetaObject.Call = ...  # 0x4
    IndexOfMethod: QMetaObject.Call = ...  # 0x5
    RegisterPropertyMetaType: QMetaObject.Call = ...  # 0x6
    RegisterMethodArgumentMetaType: QMetaObject.Call = ...  # 0x7
    BindableProperty: QMetaObject.Call = ...  # 0x8
    class Call(Enum):

        InvokeMetaMethod: QMetaObject.Call = ...  # 0x0
        ReadProperty: QMetaObject.Call = ...  # 0x1
        WriteProperty: QMetaObject.Call = ...  # 0x2
        ResetProperty: QMetaObject.Call = ...  # 0x3
        CreateInstance: QMetaObject.Call = ...  # 0x4
        IndexOfMethod: QMetaObject.Call = ...  # 0x5
        RegisterPropertyMetaType: QMetaObject.Call = ...  # 0x6
        RegisterMethodArgumentMetaType: QMetaObject.Call = ...  # 0x7
        BindableProperty: QMetaObject.Call = ...  # 0x8
    class Connection(Shiboken.Object):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, other: QMetaObject.Connection) -> None: ...
        @staticmethod
        def __copy__() -> None: ...
        def swap(self, other: QMetaObject.Connection) -> None: ...
    def __init__(self) -> None: ...
    def cast(self, obj: QObject) -> QObject: ...
    @overload
    @staticmethod
    def checkConnectArgs(signal: QMetaMethod, method: QMetaMethod) -> bool: ...
    @overload
    @staticmethod
    def checkConnectArgs(signal: bytes, method: bytes) -> bool: ...
    def classInfo(self, index: int) -> QMetaClassInfo: ...
    def classInfoCount(self) -> int: ...
    def classInfoOffset(self) -> int: ...
    def className(self) -> bytes: ...
    @staticmethod
    def connectSlotsByName(o: QObject) -> None: ...
    def constructor(self, index: int) -> QMetaMethod: ...
    def constructorCount(self) -> int: ...
    @staticmethod
    def disconnect(
        sender: QObject, signal_index: int, receiver: QObject, method_index: int
    ) -> bool: ...
    @staticmethod
    def disconnectOne(
        sender: QObject, signal_index: int, receiver: QObject, method_index: int
    ) -> bool: ...
    def enumerator(self, index: int) -> QMetaEnum: ...
    def enumeratorCount(self) -> int: ...
    def enumeratorOffset(self) -> int: ...
    def indexOfClassInfo(self, name: bytes) -> int: ...
    def indexOfConstructor(self, constructor: bytes) -> int: ...
    def indexOfEnumerator(self, name: bytes) -> int: ...
    def indexOfMethod(self, method: bytes) -> int: ...
    def indexOfProperty(self, name: bytes) -> int: ...
    def indexOfSignal(self, signal: bytes) -> int: ...
    def indexOfSlot(self, slot: bytes) -> int: ...
    def inherits(self, metaObject: QMetaObject) -> bool: ...
    @overload
    @staticmethod
    def invokeMethod(
        obj: QObject,
        member: bytes,
        arg__3: Qt.ConnectionType,
        ret: QGenericReturnArgument,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    @staticmethod
    def invokeMethod(
        obj: QObject,
        member: bytes,
        ret: QGenericReturnArgument,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    @staticmethod
    def invokeMethod(
        obj: QObject,
        member: bytes,
        type: Qt.ConnectionType,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    @overload
    @staticmethod
    def invokeMethod(
        obj: QObject,
        member: bytes,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> bool: ...
    def metaType(self) -> QMetaType: ...
    def method(self, index: int) -> QMetaMethod: ...
    def methodCount(self) -> int: ...
    def methodOffset(self) -> int: ...
    def newInstance(
        self,
        val0: QGenericArgument = ...,
        val1: QGenericArgument = ...,
        val2: QGenericArgument = ...,
        val3: QGenericArgument = ...,
        val4: QGenericArgument = ...,
        val5: QGenericArgument = ...,
        val6: QGenericArgument = ...,
        val7: QGenericArgument = ...,
        val8: QGenericArgument = ...,
        val9: QGenericArgument = ...,
    ) -> QObject: ...
    @staticmethod
    def normalizedSignature(method: bytes) -> QByteArray: ...
    @staticmethod
    def normalizedType(type: bytes) -> QByteArray: ...
    def property(self, index: int) -> QMetaProperty: ...
    def propertyCount(self) -> int: ...
    def propertyOffset(self) -> int: ...
    def superClass(self) -> QMetaObject: ...
    def userProperty(self) -> QMetaProperty: ...

class QMetaProperty(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QMetaProperty: QMetaProperty) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def enumerator(self) -> QMetaEnum: ...
    def hasNotifySignal(self) -> bool: ...
    def hasStdCppSet(self) -> bool: ...
    def isAlias(self) -> bool: ...
    def isBindable(self) -> bool: ...
    def isConstant(self) -> bool: ...
    def isDesignable(self) -> bool: ...
    def isEnumType(self) -> bool: ...
    def isFinal(self) -> bool: ...
    def isFlagType(self) -> bool: ...
    def isReadable(self) -> bool: ...
    def isRequired(self) -> bool: ...
    def isResettable(self) -> bool: ...
    def isScriptable(self) -> bool: ...
    def isStored(self) -> bool: ...
    def isUser(self) -> bool: ...
    def isValid(self) -> bool: ...
    def isWritable(self) -> bool: ...
    def metaType(self) -> QMetaType: ...
    def name(self) -> bytes: ...
    def notifySignal(self) -> QMetaMethod: ...
    def notifySignalIndex(self) -> int: ...
    def propertyIndex(self) -> int: ...
    def read(self, obj: QObject) -> Any: ...
    def readOnGadget(self, gadget: int) -> Any: ...
    def relativePropertyIndex(self) -> int: ...
    def reset(self, obj: QObject) -> bool: ...
    def resetOnGadget(self, gadget: int) -> bool: ...
    def revision(self) -> int: ...
    def typeId(self) -> int: ...
    def typeName(self) -> bytes: ...
    def userType(self) -> int: ...
    def write(self, obj: QObject, value: Any) -> bool: ...
    def writeOnGadget(self, gadget: int, value: Any) -> bool: ...

class QMetaType(Shiboken.Object):

    UnknownType: QMetaType.Type = ...  # 0x0
    Bool: QMetaType.Type = ...  # 0x1
    FirstCoreType: QMetaType.Type = ...  # 0x1
    Int: QMetaType.Type = ...  # 0x2
    UInt: QMetaType.Type = ...  # 0x3
    LongLong: QMetaType.Type = ...  # 0x4
    ULongLong: QMetaType.Type = ...  # 0x5
    Double: QMetaType.Type = ...  # 0x6
    QReal: QMetaType.Type = ...  # 0x6
    QChar: QMetaType.Type = ...  # 0x7
    QVariantMap: QMetaType.Type = ...  # 0x8
    QVariantList: QMetaType.Type = ...  # 0x9
    QString: QMetaType.Type = ...  # 0xa
    QStringList: QMetaType.Type = ...  # 0xb
    QByteArray: QMetaType.Type = ...  # 0xc
    QBitArray: QMetaType.Type = ...  # 0xd
    QDate: QMetaType.Type = ...  # 0xe
    QTime: QMetaType.Type = ...  # 0xf
    QDateTime: QMetaType.Type = ...  # 0x10
    QUrl: QMetaType.Type = ...  # 0x11
    QLocale: QMetaType.Type = ...  # 0x12
    QRect: QMetaType.Type = ...  # 0x13
    QRectF: QMetaType.Type = ...  # 0x14
    QSize: QMetaType.Type = ...  # 0x15
    QSizeF: QMetaType.Type = ...  # 0x16
    QLine: QMetaType.Type = ...  # 0x17
    QLineF: QMetaType.Type = ...  # 0x18
    QPoint: QMetaType.Type = ...  # 0x19
    QPointF: QMetaType.Type = ...  # 0x1a
    QVariantHash: QMetaType.Type = ...  # 0x1c
    QEasingCurve: QMetaType.Type = ...  # 0x1d
    QUuid: QMetaType.Type = ...  # 0x1e
    VoidStar: QMetaType.Type = ...  # 0x1f
    Long: QMetaType.Type = ...  # 0x20
    Short: QMetaType.Type = ...  # 0x21
    Char: QMetaType.Type = ...  # 0x22
    ULong: QMetaType.Type = ...  # 0x23
    UShort: QMetaType.Type = ...  # 0x24
    UChar: QMetaType.Type = ...  # 0x25
    Float: QMetaType.Type = ...  # 0x26
    QObjectStar: QMetaType.Type = ...  # 0x27
    SChar: QMetaType.Type = ...  # 0x28
    QVariant: QMetaType.Type = ...  # 0x29
    QModelIndex: QMetaType.Type = ...  # 0x2a
    Void: QMetaType.Type = ...  # 0x2b
    QRegularExpression: QMetaType.Type = ...  # 0x2c
    QJsonValue: QMetaType.Type = ...  # 0x2d
    QJsonObject: QMetaType.Type = ...  # 0x2e
    QJsonArray: QMetaType.Type = ...  # 0x2f
    QJsonDocument: QMetaType.Type = ...  # 0x30
    QByteArrayList: QMetaType.Type = ...  # 0x31
    QPersistentModelIndex: QMetaType.Type = ...  # 0x32
    Nullptr: QMetaType.Type = ...  # 0x33
    QCborSimpleType: QMetaType.Type = ...  # 0x34
    QCborValue: QMetaType.Type = ...  # 0x35
    QCborArray: QMetaType.Type = ...  # 0x36
    QCborMap: QMetaType.Type = ...  # 0x37
    Char16: QMetaType.Type = ...  # 0x38
    Char32: QMetaType.Type = ...  # 0x39
    LastCoreType: QMetaType.Type = ...  # 0x3a
    QVariantPair: QMetaType.Type = ...  # 0x3a
    FirstGuiType: QMetaType.Type = ...  # 0x1000
    QFont: QMetaType.Type = ...  # 0x1000
    QPixmap: QMetaType.Type = ...  # 0x1001
    QBrush: QMetaType.Type = ...  # 0x1002
    QColor: QMetaType.Type = ...  # 0x1003
    QPalette: QMetaType.Type = ...  # 0x1004
    QIcon: QMetaType.Type = ...  # 0x1005
    QImage: QMetaType.Type = ...  # 0x1006
    QPolygon: QMetaType.Type = ...  # 0x1007
    QRegion: QMetaType.Type = ...  # 0x1008
    QBitmap: QMetaType.Type = ...  # 0x1009
    QCursor: QMetaType.Type = ...  # 0x100a
    QKeySequence: QMetaType.Type = ...  # 0x100b
    QPen: QMetaType.Type = ...  # 0x100c
    QTextLength: QMetaType.Type = ...  # 0x100d
    QTextFormat: QMetaType.Type = ...  # 0x100e
    QTransform: QMetaType.Type = ...  # 0x1010
    QMatrix4x4: QMetaType.Type = ...  # 0x1011
    QVector2D: QMetaType.Type = ...  # 0x1012
    QVector3D: QMetaType.Type = ...  # 0x1013
    QVector4D: QMetaType.Type = ...  # 0x1014
    QQuaternion: QMetaType.Type = ...  # 0x1015
    QPolygonF: QMetaType.Type = ...  # 0x1016
    LastGuiType: QMetaType.Type = ...  # 0x1017
    QColorSpace: QMetaType.Type = ...  # 0x1017
    FirstWidgetsType: QMetaType.Type = ...  # 0x2000
    HighestInternalId: QMetaType.Type = ...  # 0x2000
    LastWidgetsType: QMetaType.Type = ...  # 0x2000
    QSizePolicy: QMetaType.Type = ...  # 0x2000
    User: QMetaType.Type = ...  # 0x10000
    NeedsConstruction: QMetaType.TypeFlag = ...  # 0x1
    NeedsDestruction: QMetaType.TypeFlag = ...  # 0x2
    MovableType: QMetaType.TypeFlag = ...  # 0x4
    RelocatableType: QMetaType.TypeFlag = ...  # 0x4
    PointerToQObject: QMetaType.TypeFlag = ...  # 0x8
    IsEnumeration: QMetaType.TypeFlag = ...  # 0x10
    SharedPointerToQObject: QMetaType.TypeFlag = ...  # 0x20
    WeakPointerToQObject: QMetaType.TypeFlag = ...  # 0x40
    TrackingPointerToQObject: QMetaType.TypeFlag = ...  # 0x80
    IsUnsignedEnumeration: QMetaType.TypeFlag = ...  # 0x100
    IsGadget: QMetaType.TypeFlag = ...  # 0x200
    PointerToGadget: QMetaType.TypeFlag = ...  # 0x400
    IsPointer: QMetaType.TypeFlag = ...  # 0x800
    IsQmlList: QMetaType.TypeFlag = ...  # 0x1000
    IsConst: QMetaType.TypeFlag = ...  # 0x2000
    class Type(Enum):

        UnknownType: QMetaType.Type = ...  # 0x0
        Bool: QMetaType.Type = ...  # 0x1
        FirstCoreType: QMetaType.Type = ...  # 0x1
        Int: QMetaType.Type = ...  # 0x2
        UInt: QMetaType.Type = ...  # 0x3
        LongLong: QMetaType.Type = ...  # 0x4
        ULongLong: QMetaType.Type = ...  # 0x5
        Double: QMetaType.Type = ...  # 0x6
        QReal: QMetaType.Type = ...  # 0x6
        QChar: QMetaType.Type = ...  # 0x7
        QVariantMap: QMetaType.Type = ...  # 0x8
        QVariantList: QMetaType.Type = ...  # 0x9
        QString: QMetaType.Type = ...  # 0xa
        QStringList: QMetaType.Type = ...  # 0xb
        QByteArray: QMetaType.Type = ...  # 0xc
        QBitArray: QMetaType.Type = ...  # 0xd
        QDate: QMetaType.Type = ...  # 0xe
        QTime: QMetaType.Type = ...  # 0xf
        QDateTime: QMetaType.Type = ...  # 0x10
        QUrl: QMetaType.Type = ...  # 0x11
        QLocale: QMetaType.Type = ...  # 0x12
        QRect: QMetaType.Type = ...  # 0x13
        QRectF: QMetaType.Type = ...  # 0x14
        QSize: QMetaType.Type = ...  # 0x15
        QSizeF: QMetaType.Type = ...  # 0x16
        QLine: QMetaType.Type = ...  # 0x17
        QLineF: QMetaType.Type = ...  # 0x18
        QPoint: QMetaType.Type = ...  # 0x19
        QPointF: QMetaType.Type = ...  # 0x1a
        QVariantHash: QMetaType.Type = ...  # 0x1c
        QEasingCurve: QMetaType.Type = ...  # 0x1d
        QUuid: QMetaType.Type = ...  # 0x1e
        VoidStar: QMetaType.Type = ...  # 0x1f
        Long: QMetaType.Type = ...  # 0x20
        Short: QMetaType.Type = ...  # 0x21
        Char: QMetaType.Type = ...  # 0x22
        ULong: QMetaType.Type = ...  # 0x23
        UShort: QMetaType.Type = ...  # 0x24
        UChar: QMetaType.Type = ...  # 0x25
        Float: QMetaType.Type = ...  # 0x26
        QObjectStar: QMetaType.Type = ...  # 0x27
        SChar: QMetaType.Type = ...  # 0x28
        QVariant: QMetaType.Type = ...  # 0x29
        QModelIndex: QMetaType.Type = ...  # 0x2a
        Void: QMetaType.Type = ...  # 0x2b
        QRegularExpression: QMetaType.Type = ...  # 0x2c
        QJsonValue: QMetaType.Type = ...  # 0x2d
        QJsonObject: QMetaType.Type = ...  # 0x2e
        QJsonArray: QMetaType.Type = ...  # 0x2f
        QJsonDocument: QMetaType.Type = ...  # 0x30
        QByteArrayList: QMetaType.Type = ...  # 0x31
        QPersistentModelIndex: QMetaType.Type = ...  # 0x32
        Nullptr: QMetaType.Type = ...  # 0x33
        QCborSimpleType: QMetaType.Type = ...  # 0x34
        QCborValue: QMetaType.Type = ...  # 0x35
        QCborArray: QMetaType.Type = ...  # 0x36
        QCborMap: QMetaType.Type = ...  # 0x37
        Char16: QMetaType.Type = ...  # 0x38
        Char32: QMetaType.Type = ...  # 0x39
        LastCoreType: QMetaType.Type = ...  # 0x3a
        QVariantPair: QMetaType.Type = ...  # 0x3a
        FirstGuiType: QMetaType.Type = ...  # 0x1000
        QFont: QMetaType.Type = ...  # 0x1000
        QPixmap: QMetaType.Type = ...  # 0x1001
        QBrush: QMetaType.Type = ...  # 0x1002
        QColor: QMetaType.Type = ...  # 0x1003
        QPalette: QMetaType.Type = ...  # 0x1004
        QIcon: QMetaType.Type = ...  # 0x1005
        QImage: QMetaType.Type = ...  # 0x1006
        QPolygon: QMetaType.Type = ...  # 0x1007
        QRegion: QMetaType.Type = ...  # 0x1008
        QBitmap: QMetaType.Type = ...  # 0x1009
        QCursor: QMetaType.Type = ...  # 0x100a
        QKeySequence: QMetaType.Type = ...  # 0x100b
        QPen: QMetaType.Type = ...  # 0x100c
        QTextLength: QMetaType.Type = ...  # 0x100d
        QTextFormat: QMetaType.Type = ...  # 0x100e
        QTransform: QMetaType.Type = ...  # 0x1010
        QMatrix4x4: QMetaType.Type = ...  # 0x1011
        QVector2D: QMetaType.Type = ...  # 0x1012
        QVector3D: QMetaType.Type = ...  # 0x1013
        QVector4D: QMetaType.Type = ...  # 0x1014
        QQuaternion: QMetaType.Type = ...  # 0x1015
        QPolygonF: QMetaType.Type = ...  # 0x1016
        LastGuiType: QMetaType.Type = ...  # 0x1017
        QColorSpace: QMetaType.Type = ...  # 0x1017
        FirstWidgetsType: QMetaType.Type = ...  # 0x2000
        HighestInternalId: QMetaType.Type = ...  # 0x2000
        LastWidgetsType: QMetaType.Type = ...  # 0x2000
        QSizePolicy: QMetaType.Type = ...  # 0x2000
        User: QMetaType.Type = ...  # 0x10000
    class TypeFlag(Enum):

        NeedsConstruction: QMetaType.TypeFlag = ...  # 0x1
        NeedsDestruction: QMetaType.TypeFlag = ...  # 0x2
        MovableType: QMetaType.TypeFlag = ...  # 0x4
        RelocatableType: QMetaType.TypeFlag = ...  # 0x4
        PointerToQObject: QMetaType.TypeFlag = ...  # 0x8
        IsEnumeration: QMetaType.TypeFlag = ...  # 0x10
        SharedPointerToQObject: QMetaType.TypeFlag = ...  # 0x20
        WeakPointerToQObject: QMetaType.TypeFlag = ...  # 0x40
        TrackingPointerToQObject: QMetaType.TypeFlag = ...  # 0x80
        IsUnsignedEnumeration: QMetaType.TypeFlag = ...  # 0x100
        IsGadget: QMetaType.TypeFlag = ...  # 0x200
        PointerToGadget: QMetaType.TypeFlag = ...  # 0x400
        IsPointer: QMetaType.TypeFlag = ...  # 0x800
        IsQmlList: QMetaType.TypeFlag = ...  # 0x1000
        IsConst: QMetaType.TypeFlag = ...  # 0x2000
    class TypeFlags(object): ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, type: int) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def alignOf(self) -> int: ...
    @staticmethod
    def canConvert(fromType: QMetaType, toType: QMetaType) -> bool: ...
    @staticmethod
    def canView(fromType: QMetaType, toType: QMetaType) -> bool: ...
    @staticmethod
    def compare(lhs: int, rhs: int, typeId: int) -> Tuple[bool, int]: ...
    @overload
    def construct(self, where: int, copy: Optional[int] = ...) -> int: ...
    @overload
    @staticmethod
    def construct(type: int, where: int, copy: int) -> int: ...
    @overload
    @staticmethod
    def convert(from_: int, fromTypeId: int, to: int, toTypeId: int) -> bool: ...
    @overload
    @staticmethod
    def convert(fromType: QMetaType, from_: int, toType: QMetaType, to: int) -> bool: ...
    @overload
    def create(self, copy: Optional[int] = ...) -> int: ...
    @overload
    @staticmethod
    def create(type: int, copy: Optional[int] = ...) -> int: ...
    @overload
    def destroy(self, data: int) -> None: ...
    @overload
    @staticmethod
    def destroy(type: int, data: int) -> None: ...
    @overload
    def destruct(self, data: int) -> None: ...
    @overload
    @staticmethod
    def destruct(type: int, where: int) -> None: ...
    @overload
    @staticmethod
    def equals(lhs: int, rhs: int, typeId: int) -> Tuple[bool, int]: ...
    @overload
    def equals(self, lhs: int, rhs: int) -> bool: ...
    def flags(self) -> QMetaType.TypeFlags: ...
    @staticmethod
    def fromName(name: Union[QByteArray, bytes]) -> QMetaType: ...
    @staticmethod
    def hasRegisteredConverterFunction(fromType: QMetaType, toType: QMetaType) -> bool: ...
    def hasRegisteredDataStreamOperators(self) -> bool: ...
    @overload
    def hasRegisteredDebugStreamOperator(self) -> bool: ...
    @overload
    @staticmethod
    def hasRegisteredDebugStreamOperator(typeId: int) -> bool: ...
    @staticmethod
    def hasRegisteredMutableViewFunction(fromType: QMetaType, toType: QMetaType) -> bool: ...
    def id(self, arg__1: int = ...) -> int: ...
    def isEqualityComparable(self) -> bool: ...
    def isOrdered(self) -> bool: ...
    @overload
    def isRegistered(self) -> bool: ...
    @overload
    @staticmethod
    def isRegistered(type: int) -> bool: ...
    def isValid(self) -> bool: ...
    @overload
    def load(self, stream: QDataStream, data: int) -> bool: ...
    @overload
    @staticmethod
    def load(stream: QDataStream, type: int, data: int) -> bool: ...
    @staticmethod
    def metaObjectForType(type: int) -> QMetaObject: ...
    def name(self) -> bytes: ...
    @overload
    def save(self, stream: QDataStream, data: int) -> bool: ...
    @overload
    @staticmethod
    def save(stream: QDataStream, type: int, data: int) -> bool: ...
    @overload
    def sizeOf(self) -> int: ...
    @overload
    @staticmethod
    def sizeOf(type: int) -> int: ...
    @staticmethod
    def type(typeName: bytes) -> int: ...
    @staticmethod
    def typeFlags(type: int) -> QMetaType.TypeFlags: ...
    @staticmethod
    def typeName(type: int) -> bytes: ...
    @staticmethod
    def unregisterConverterFunction(from_: QMetaType, to: QMetaType) -> None: ...
    @staticmethod
    def unregisterMetaType(type: QMetaType) -> None: ...
    @staticmethod
    def unregisterMutableViewFunction(from_: QMetaType, to: QMetaType) -> None: ...
    @staticmethod
    def view(fromType: QMetaType, from_: int, toType: QMetaType, to: int) -> bool: ...

class QMimeData(QObject):
    def __init__(self) -> None: ...
    def clear(self) -> None: ...
    def colorData(self) -> Any: ...
    def data(self, mimetype: str) -> QByteArray: ...
    def formats(self) -> List[str]: ...
    def hasColor(self) -> bool: ...
    def hasFormat(self, mimetype: str) -> bool: ...
    def hasHtml(self) -> bool: ...
    def hasImage(self) -> bool: ...
    def hasText(self) -> bool: ...
    def hasUrls(self) -> bool: ...
    def html(self) -> str: ...
    def imageData(self) -> Any: ...
    def removeFormat(self, mimetype: str) -> None: ...
    def retrieveData(self, mimetype: str, preferredType: QMetaType) -> Any: ...
    def setColorData(self, color: Any) -> None: ...
    def setData(self, mimetype: str, data: Union[QByteArray, bytes]) -> None: ...
    def setHtml(self, html: str) -> None: ...
    def setImageData(self, image: Any) -> None: ...
    def setText(self, text: str) -> None: ...
    def setUrls(self, urls: Sequence[QUrl]) -> None: ...
    def text(self) -> str: ...
    def urls(self) -> List[QUrl]: ...

class QMimeDatabase(Shiboken.Object):

    MatchDefault: QMimeDatabase.MatchMode = ...  # 0x0
    MatchExtension: QMimeDatabase.MatchMode = ...  # 0x1
    MatchContent: QMimeDatabase.MatchMode = ...  # 0x2
    class MatchMode(Enum):

        MatchDefault: QMimeDatabase.MatchMode = ...  # 0x0
        MatchExtension: QMimeDatabase.MatchMode = ...  # 0x1
        MatchContent: QMimeDatabase.MatchMode = ...  # 0x2
    def __init__(self) -> None: ...
    def allMimeTypes(self) -> List[QMimeType]: ...
    @overload
    def mimeTypeForData(self, data: Union[QByteArray, bytes]) -> QMimeType: ...
    @overload
    def mimeTypeForData(self, device: QIODevice) -> QMimeType: ...
    @overload
    def mimeTypeForFile(
        self, fileInfo: QFileInfo, mode: QMimeDatabase.MatchMode = ...
    ) -> QMimeType: ...
    @overload
    def mimeTypeForFile(self, fileName: str, mode: QMimeDatabase.MatchMode = ...) -> QMimeType: ...
    @overload
    def mimeTypeForFileNameAndData(
        self, fileName: str, data: Union[QByteArray, bytes]
    ) -> QMimeType: ...
    @overload
    def mimeTypeForFileNameAndData(self, fileName: str, device: QIODevice) -> QMimeType: ...
    def mimeTypeForName(self, nameOrAlias: str) -> QMimeType: ...
    def mimeTypeForUrl(self, url: Union[QUrl, str]) -> QMimeType: ...
    def mimeTypesForFileName(self, fileName: str) -> List[QMimeType]: ...
    def suffixForFileName(self, fileName: str) -> str: ...

class QMimeType(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QMimeType) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def aliases(self) -> List[str]: ...
    def allAncestors(self) -> List[str]: ...
    def comment(self) -> str: ...
    def filterString(self) -> str: ...
    def genericIconName(self) -> str: ...
    def globPatterns(self) -> List[str]: ...
    def iconName(self) -> str: ...
    def inherits(self, mimeTypeName: str) -> bool: ...
    def isDefault(self) -> bool: ...
    def isValid(self) -> bool: ...
    def name(self) -> str: ...
    def parentMimeTypes(self) -> List[str]: ...
    def preferredSuffix(self) -> str: ...
    def suffixes(self) -> List[str]: ...
    def swap(self, other: QMimeType) -> None: ...

class QModelIndex(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QModelIndex: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def column(self) -> int: ...
    def constInternalPointer(self) -> int: ...
    def data(self, role: int = ...) -> Any: ...
    def flags(self) -> Qt.ItemFlags: ...
    def internalId(self) -> int: ...
    def internalPointer(self) -> int: ...
    def isValid(self) -> bool: ...
    def model(self) -> QAbstractItemModel: ...
    def parent(self) -> QModelIndex: ...
    def row(self) -> int: ...
    def sibling(self, row: int, column: int) -> QModelIndex: ...
    def siblingAtColumn(self, column: int) -> QModelIndex: ...
    def siblingAtRow(self, row: int) -> QModelIndex: ...

class QModelRoleData(Shiboken.Object):
    @overload
    def __init__(self, QModelRoleData: QModelRoleData) -> None: ...
    @overload
    def __init__(self, role: int) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def clearData(self) -> None: ...
    def data(self) -> Any: ...
    def role(self) -> int: ...

class QMutex(QBasicMutex):
    def __init__(self) -> None: ...
    @overload
    def tryLock(self) -> bool: ...
    @overload
    def tryLock(self, timeout: int) -> bool: ...
    def try_lock(self) -> bool: ...

class QMutexLocker(Shiboken.Object):
    @overload
    def __init__(self, m: QMutex) -> None: ...
    @overload
    def __init__(self, m: QRecursiveMutex) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, arg__1: object, arg__2: object, arg__3: object) -> None: ...
    def mutex(self) -> QMutex: ...
    def recursiveMutex(self) -> QRecursiveMutex: ...
    def relock(self) -> None: ...
    def unlock(self) -> None: ...

class QObject(Shiboken.Object):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def blockSignals(self, b: bool) -> bool: ...
    def childEvent(self, event: QChildEvent) -> None: ...
    def children(self) -> List[QObject]: ...
    @overload
    @staticmethod
    def connect(
        arg__1: QObject, arg__2: bytes, arg__3: Callable, type: Qt.ConnectionType = ...
    ) -> QMetaObject.Connection: ...
    @overload
    def connect(
        self, arg__1: bytes, arg__2: Callable, type: Qt.ConnectionType = ...
    ) -> QMetaObject.Connection: ...
    @overload
    def connect(
        self, arg__1: bytes, arg__2: QObject, arg__3: bytes, type: Qt.ConnectionType = ...
    ) -> QMetaObject.Connection: ...
    @overload
    def connect(
        self, sender: QObject, signal: bytes, member: bytes, type: Qt.ConnectionType = ...
    ) -> QMetaObject.Connection: ...
    @overload
    @staticmethod
    def connect(
        sender: QObject,
        signal: QMetaMethod,
        receiver: QObject,
        method: QMetaMethod,
        type: Qt.ConnectionType = ...,
    ) -> QMetaObject.Connection: ...
    @overload
    @staticmethod
    def connect(
        sender: QObject,
        signal: bytes,
        receiver: QObject,
        member: bytes,
        type: Qt.ConnectionType = ...,
    ) -> QMetaObject.Connection: ...
    def connectNotify(self, signal: QMetaMethod) -> None: ...
    def customEvent(self, event: QEvent) -> None: ...
    def deleteLater(self) -> None: ...
    @overload
    @staticmethod
    def disconnect(arg__1: QMetaObject.Connection) -> bool: ...
    @overload
    @staticmethod
    def disconnect(arg__1: QObject, arg__2: bytes, arg__3: Callable) -> bool: ...
    @overload
    def disconnect(self, arg__1: bytes, arg__2: Callable) -> bool: ...
    @overload
    def disconnect(self, receiver: QObject, member: Optional[bytes] = ...) -> bool: ...
    @overload
    def disconnect(self, signal: bytes, receiver: QObject, member: bytes) -> bool: ...
    @overload
    @staticmethod
    def disconnect(
        sender: QObject, signal: QMetaMethod, receiver: QObject, member: QMetaMethod
    ) -> bool: ...
    @overload
    @staticmethod
    def disconnect(sender: QObject, signal: bytes, receiver: QObject, member: bytes) -> bool: ...
    def disconnectNotify(self, signal: QMetaMethod) -> None: ...
    def dumpObjectInfo(self) -> None: ...
    def dumpObjectTree(self) -> None: ...
    def dynamicPropertyNames(self) -> List[QByteArray]: ...
    def emit(self, arg__1: bytes, *args: None) -> bool: ...
    def event(self, event: QEvent) -> bool: ...
    def eventFilter(self, watched: QObject, event: QEvent) -> bool: ...
    def findChild(
        self, type: type, name: str = ..., options: Qt.FindChildOptions = ...
    ) -> object: ...
    @overload
    def findChildren(
        self, type: type, name: str = ..., options: Qt.FindChildOptions = ...
    ) -> Iterable: ...
    @overload
    def findChildren(
        self,
        type: type,
        pattern: Union[QRegularExpression, str],
        options: Qt.FindChildOptions = ...,
    ) -> Iterable: ...
    def inherits(self, classname: bytes) -> bool: ...
    def installEventFilter(self, filterObj: QObject) -> None: ...
    def isSignalConnected(self, signal: QMetaMethod) -> bool: ...
    def isWidgetType(self) -> bool: ...
    def isWindowType(self) -> bool: ...
    def killTimer(self, id: int) -> None: ...
    def metaObject(self) -> QMetaObject: ...
    def moveToThread(self, thread: QThread) -> None: ...
    def objectName(self) -> str: ...
    def parent(self) -> QObject: ...
    def property(self, name: bytes) -> Any: ...
    def receivers(self, signal: bytes) -> int: ...
    def removeEventFilter(self, obj: QObject) -> None: ...
    def sender(self) -> QObject: ...
    def senderSignalIndex(self) -> int: ...
    def setObjectName(self, name: str) -> None: ...
    def setParent(self, parent: QObject) -> None: ...
    def setProperty(self, name: bytes, value: Any) -> bool: ...
    def signalsBlocked(self) -> bool: ...
    def startTimer(self, interval: int, timerType: Qt.TimerType = ...) -> int: ...
    def thread(self) -> QThread: ...
    def timerEvent(self, event: QTimerEvent) -> None: ...

class QOperatingSystemVersion(Shiboken.Object):

    Unknown: QOperatingSystemVersion.OSType = ...  # 0x0
    Windows: QOperatingSystemVersion.OSType = ...  # 0x1
    MacOS: QOperatingSystemVersion.OSType = ...  # 0x2
    IOS: QOperatingSystemVersion.OSType = ...  # 0x3
    TvOS: QOperatingSystemVersion.OSType = ...  # 0x4
    WatchOS: QOperatingSystemVersion.OSType = ...  # 0x5
    Android: QOperatingSystemVersion.OSType = ...  # 0x6
    class OSType(Enum):

        Unknown: QOperatingSystemVersion.OSType = ...  # 0x0
        Windows: QOperatingSystemVersion.OSType = ...  # 0x1
        MacOS: QOperatingSystemVersion.OSType = ...  # 0x2
        IOS: QOperatingSystemVersion.OSType = ...  # 0x3
        TvOS: QOperatingSystemVersion.OSType = ...  # 0x4
        WatchOS: QOperatingSystemVersion.OSType = ...  # 0x5
        Android: QOperatingSystemVersion.OSType = ...  # 0x6
    @overload
    def __init__(self, QOperatingSystemVersion: QOperatingSystemVersion) -> None: ...
    @overload
    def __init__(
        self,
        osType: QOperatingSystemVersion.OSType,
        vmajor: int,
        vminor: int = ...,
        vmicro: int = ...,
    ) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def current() -> QOperatingSystemVersion: ...
    @staticmethod
    def currentType() -> QOperatingSystemVersion.OSType: ...
    def majorVersion(self) -> int: ...
    def microVersion(self) -> int: ...
    def minorVersion(self) -> int: ...
    def name(self) -> str: ...
    def segmentCount(self) -> int: ...
    def type(self) -> QOperatingSystemVersion.OSType: ...
    def version(self) -> QVersionNumber: ...

class QParallelAnimationGroup(QAnimationGroup):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def duration(self) -> int: ...
    def event(self, event: QEvent) -> bool: ...
    def updateCurrentTime(self, currentTime: int) -> None: ...
    def updateDirection(self, direction: QAbstractAnimation.Direction) -> None: ...
    def updateState(
        self, newState: QAbstractAnimation.State, oldState: QAbstractAnimation.State
    ) -> None: ...

class QPauseAnimation(QAbstractAnimation):
    @overload
    def __init__(self, msecs: int, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def duration(self) -> int: ...
    def event(self, e: QEvent) -> bool: ...
    def setDuration(self, msecs: int) -> None: ...
    def updateCurrentTime(self, arg__1: int) -> None: ...

class QPersistentModelIndex(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, index: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    @overload
    def __init__(self, other: Union[QPersistentModelIndex, QModelIndex]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def column(self) -> int: ...
    def constInternalPointer(self) -> int: ...
    def data(self, role: int = ...) -> Any: ...
    def flags(self) -> Qt.ItemFlags: ...
    def internalId(self) -> int: ...
    def internalPointer(self) -> int: ...
    def isValid(self) -> bool: ...
    def model(self) -> QAbstractItemModel: ...
    def parent(self) -> QModelIndex: ...
    def row(self) -> int: ...
    def sibling(self, row: int, column: int) -> QModelIndex: ...
    def swap(self, other: Union[QPersistentModelIndex, QModelIndex]) -> None: ...

class QPluginLoader(QObject):
    @overload
    def __init__(self, fileName: str, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def errorString(self) -> str: ...
    def fileName(self) -> str: ...
    def instance(self) -> QObject: ...
    def isLoaded(self) -> bool: ...
    def load(self) -> bool: ...
    def loadHints(self) -> QLibrary.LoadHints: ...
    def metaData(self) -> Dict[str, QJsonValue]: ...
    def setFileName(self, fileName: str) -> None: ...
    def setLoadHints(self, loadHints: QLibrary.LoadHints) -> None: ...
    @staticmethod
    def staticInstances() -> List[QObject]: ...
    def unload(self) -> bool: ...

class QPoint(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QPoint: QPoint) -> None: ...
    @overload
    def __init__(self, xpos: int, ypos: int) -> None: ...
    def __add__(self, p2: QPoint) -> QPoint: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, p: QPoint) -> QPoint: ...
    @overload
    def __imul__(self, factor: float) -> QPoint: ...
    @overload
    def __imul__(self, factor: float) -> QPoint: ...
    @overload
    def __imul__(self, factor: int) -> QPoint: ...
    def __isub__(self, p: QPoint) -> QPoint: ...
    @overload
    def __mul__(self, factor: float) -> QPoint: ...
    @overload
    def __mul__(self, factor: float) -> QPoint: ...
    @overload
    def __mul__(self, factor: int) -> QPoint: ...
    def __neg__(self) -> QPoint: ...
    def __pos__(self) -> QPoint: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, p2: QPoint | QPointF) -> QPoint: ...
    @staticmethod
    def dotProduct(p1: QPoint, p2: QPoint) -> int: ...
    def isNull(self) -> bool: ...
    def manhattanLength(self) -> int: ...
    def setX(self, x: int) -> None: ...
    def setY(self, y: int) -> None: ...
    def toTuple(self) -> object: ...
    def transposed(self) -> QPoint: ...
    def x(self) -> int: ...
    def y(self) -> int: ...

class QPointF(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QPointF: Union[QPointF, QPoint]) -> None: ...
    @overload
    def __init__(self, p: QPoint) -> None: ...
    @overload
    def __init__(self, xpos: float, ypos: float) -> None: ...
    def __add__(self, p2: Union[QPointF, QPoint]) -> QPointF: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, p: Union[QPointF, QPoint]) -> QPointF: ...
    def __imul__(self, c: float) -> QPointF: ...
    def __isub__(self, p: Union[QPointF, QPoint]) -> QPointF: ...
    def __mul__(self, c: float) -> QPointF: ...
    def __neg__(self) -> QPointF: ...
    def __pos__(self) -> QPointF: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, p2: Union[QPointF, QPoint]) -> QPointF: ...
    @staticmethod
    def dotProduct(p1: Union[QPointF, QPoint], p2: Union[QPointF, QPoint]) -> float: ...
    def isNull(self) -> bool: ...
    def manhattanLength(self) -> float: ...
    def setX(self, x: float) -> None: ...
    def setY(self, y: float) -> None: ...
    def toPoint(self) -> QPoint: ...
    def toTuple(self) -> object: ...
    def transposed(self) -> QPointF: ...
    def x(self) -> float: ...
    def y(self) -> float: ...

class QPointFList(object): ...

class QProcess(QIODevice):

    NormalExit: QProcess.ExitStatus = ...  # 0x0
    CrashExit: QProcess.ExitStatus = ...  # 0x1
    ManagedInputChannel: QProcess.InputChannelMode = ...  # 0x0
    ForwardedInputChannel: QProcess.InputChannelMode = ...  # 0x1
    StandardOutput: QProcess.ProcessChannel = ...  # 0x0
    StandardError: QProcess.ProcessChannel = ...  # 0x1
    SeparateChannels: QProcess.ProcessChannelMode = ...  # 0x0
    MergedChannels: QProcess.ProcessChannelMode = ...  # 0x1
    ForwardedChannels: QProcess.ProcessChannelMode = ...  # 0x2
    ForwardedOutputChannel: QProcess.ProcessChannelMode = ...  # 0x3
    ForwardedErrorChannel: QProcess.ProcessChannelMode = ...  # 0x4
    FailedToStart: QProcess.ProcessError = ...  # 0x0
    Crashed: QProcess.ProcessError = ...  # 0x1
    Timedout: QProcess.ProcessError = ...  # 0x2
    ReadError: QProcess.ProcessError = ...  # 0x3
    WriteError: QProcess.ProcessError = ...  # 0x4
    UnknownError: QProcess.ProcessError = ...  # 0x5
    NotRunning: QProcess.ProcessState = ...  # 0x0
    Starting: QProcess.ProcessState = ...  # 0x1
    Running: QProcess.ProcessState = ...  # 0x2
    class ExitStatus(Enum):

        NormalExit: QProcess.ExitStatus = ...  # 0x0
        CrashExit: QProcess.ExitStatus = ...  # 0x1
    class InputChannelMode(Enum):

        ManagedInputChannel: QProcess.InputChannelMode = ...  # 0x0
        ForwardedInputChannel: QProcess.InputChannelMode = ...  # 0x1
    class ProcessChannel(Enum):

        StandardOutput: QProcess.ProcessChannel = ...  # 0x0
        StandardError: QProcess.ProcessChannel = ...  # 0x1
    class ProcessChannelMode(Enum):

        SeparateChannels: QProcess.ProcessChannelMode = ...  # 0x0
        MergedChannels: QProcess.ProcessChannelMode = ...  # 0x1
        ForwardedChannels: QProcess.ProcessChannelMode = ...  # 0x2
        ForwardedOutputChannel: QProcess.ProcessChannelMode = ...  # 0x3
        ForwardedErrorChannel: QProcess.ProcessChannelMode = ...  # 0x4
    class ProcessError(Enum):

        FailedToStart: QProcess.ProcessError = ...  # 0x0
        Crashed: QProcess.ProcessError = ...  # 0x1
        Timedout: QProcess.ProcessError = ...  # 0x2
        ReadError: QProcess.ProcessError = ...  # 0x3
        WriteError: QProcess.ProcessError = ...  # 0x4
        UnknownError: QProcess.ProcessError = ...  # 0x5
    class ProcessState(Enum):

        NotRunning: QProcess.ProcessState = ...  # 0x0
        Starting: QProcess.ProcessState = ...  # 0x1
        Running: QProcess.ProcessState = ...  # 0x2
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def arguments(self) -> List[str]: ...
    def bytesToWrite(self) -> int: ...
    def close(self) -> None: ...
    def closeReadChannel(self, channel: QProcess.ProcessChannel) -> None: ...
    def closeWriteChannel(self) -> None: ...
    def environment(self) -> List[str]: ...
    def error(self) -> QProcess.ProcessError: ...
    @staticmethod
    def execute(program: str, arguments: Sequence[str] = ...) -> int: ...
    def exitCode(self) -> int: ...
    def exitStatus(self) -> QProcess.ExitStatus: ...
    def inputChannelMode(self) -> QProcess.InputChannelMode: ...
    def isSequential(self) -> bool: ...
    def kill(self) -> None: ...
    def nativeArguments(self) -> str: ...
    @staticmethod
    def nullDevice() -> str: ...
    def open(self, mode: QIODeviceBase.OpenMode = ...) -> bool: ...
    def processChannelMode(self) -> QProcess.ProcessChannelMode: ...
    def processEnvironment(self) -> QProcessEnvironment: ...
    def processId(self) -> int: ...
    def program(self) -> str: ...
    def readAllStandardError(self) -> QByteArray: ...
    def readAllStandardOutput(self) -> QByteArray: ...
    def readChannel(self) -> QProcess.ProcessChannel: ...
    def readData(self, data: bytes, maxlen: int) -> object: ...
    def setArguments(self, arguments: Sequence[str]) -> None: ...
    def setEnvironment(self, environment: Sequence[str]) -> None: ...
    def setInputChannelMode(self, mode: QProcess.InputChannelMode) -> None: ...
    def setNativeArguments(self, arguments: str) -> None: ...
    def setProcessChannelMode(self, mode: QProcess.ProcessChannelMode) -> None: ...
    def setProcessEnvironment(self, environment: QProcessEnvironment) -> None: ...
    def setProcessState(self, state: QProcess.ProcessState) -> None: ...
    def setProgram(self, program: str) -> None: ...
    def setReadChannel(self, channel: QProcess.ProcessChannel) -> None: ...
    def setStandardErrorFile(self, fileName: str, mode: QIODeviceBase.OpenMode = ...) -> None: ...
    def setStandardInputFile(self, fileName: str) -> None: ...
    def setStandardOutputFile(self, fileName: str, mode: QIODeviceBase.OpenMode = ...) -> None: ...
    def setStandardOutputProcess(self, destination: QProcess) -> None: ...
    def setWorkingDirectory(self, dir: str) -> None: ...
    @staticmethod
    def splitCommand(command: str) -> List[str]: ...
    @overload
    def start(self, mode: QIODeviceBase.OpenMode = ...) -> None: ...
    @overload
    def start(
        self, program: str, arguments: Sequence[str] = ..., mode: QIODeviceBase.OpenMode = ...
    ) -> None: ...
    def startCommand(self, command: str, mode: QIODeviceBase.OpenMode = ...) -> None: ...
    @overload
    @staticmethod
    def startDetached(
        program: str, arguments: Sequence[str] = ..., workingDirectory: str = ...
    ) -> Tuple[Tuple, int]: ...
    @overload
    def startDetached(self) -> Tuple[bool, int]: ...
    def state(self) -> QProcess.ProcessState: ...
    @staticmethod
    def systemEnvironment() -> List[str]: ...
    def terminate(self) -> None: ...
    def waitForBytesWritten(self, msecs: int = ...) -> bool: ...
    def waitForFinished(self, msecs: int = ...) -> bool: ...
    def waitForReadyRead(self, msecs: int = ...) -> bool: ...
    def waitForStarted(self, msecs: int = ...) -> bool: ...
    def workingDirectory(self) -> str: ...
    def writeData(self, data: bytes, len: int) -> int: ...

class QProcessEnvironment(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QProcessEnvironment) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def clear(self) -> None: ...
    def contains(self, name: str) -> bool: ...
    @overload
    def insert(self, e: QProcessEnvironment) -> None: ...
    @overload
    def insert(self, name: str, value: str) -> None: ...
    def isEmpty(self) -> bool: ...
    def keys(self) -> List[str]: ...
    def remove(self, name: str) -> None: ...
    def swap(self, other: QProcessEnvironment) -> None: ...
    @staticmethod
    def systemEnvironment() -> QProcessEnvironment: ...
    def toStringList(self) -> List[str]: ...
    def value(self, name: str, defaultValue: str = ...) -> str: ...

class QPropertyAnimation(QVariantAnimation):
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(
        self,
        target: QObject,
        propertyName: Union[QByteArray, bytes],
        parent: Optional[QObject] = ...,
    ) -> None: ...
    def event(self, event: QEvent) -> bool: ...
    def propertyName(self) -> QByteArray: ...
    def setPropertyName(self, propertyName: Union[QByteArray, bytes]) -> None: ...
    def setTargetObject(self, target: QObject) -> None: ...
    def targetObject(self) -> QObject: ...
    def updateCurrentValue(self, value: Any) -> None: ...
    def updateState(
        self, newState: QAbstractAnimation.State, oldState: QAbstractAnimation.State
    ) -> None: ...

class QRandomGenerator(Shiboken.Object):
    @overload
    def __init__(self, begin: int, end: int) -> None: ...
    @overload
    def __init__(self, other: QRandomGenerator) -> None: ...
    @overload
    def __init__(self, seedBuffer: int, len: int) -> None: ...
    @overload
    def __init__(self, seedValue: int = ...) -> None: ...
    @overload
    def bounded(self, highest: float) -> float: ...
    @overload
    def bounded(self, highest: int) -> int: ...
    @overload
    def bounded(self, highest: int) -> int: ...
    @overload
    def bounded(self, highest: int) -> int: ...
    @overload
    def bounded(self, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    @overload
    def bounded(self, lowest: int, highest: int) -> int: ...
    def discard(self, z: int) -> None: ...
    def generate(self) -> int: ...
    def generate64(self) -> int: ...
    def generateDouble(self) -> float: ...
    @staticmethod
    def global_() -> QRandomGenerator: ...
    @staticmethod
    def max() -> int: ...
    @staticmethod
    def min() -> int: ...
    @staticmethod
    def securelySeeded() -> QRandomGenerator: ...
    def seed(self, s: int = ...) -> None: ...
    @staticmethod
    def system() -> QRandomGenerator: ...

class QRandomGenerator64(QRandomGenerator):
    @overload
    def __init__(self, begin: int, end: int) -> None: ...
    @overload
    def __init__(self, other: QRandomGenerator) -> None: ...
    @overload
    def __init__(self, seedBuffer: int, len: int) -> None: ...
    @overload
    def __init__(self, seedValue: int = ...) -> None: ...
    def discard(self, z: int) -> None: ...
    def generate(self) -> int: ...
    @staticmethod
    def global_() -> QRandomGenerator64: ...
    @staticmethod
    def max() -> int: ...
    @staticmethod
    def min() -> int: ...
    @staticmethod
    def securelySeeded() -> QRandomGenerator64: ...
    @staticmethod
    def system() -> QRandomGenerator64: ...

class QReadLocker(Shiboken.Object):
    def __init__(self, readWriteLock: QReadWriteLock) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, arg__1: object, arg__2: object, arg__3: object) -> None: ...
    def readWriteLock(self) -> QReadWriteLock: ...
    def relock(self) -> None: ...
    def unlock(self) -> None: ...

class QReadWriteLock(Shiboken.Object):

    NonRecursive: QReadWriteLock.RecursionMode = ...  # 0x0
    Recursive: QReadWriteLock.RecursionMode = ...  # 0x1
    class RecursionMode(Enum):

        NonRecursive: QReadWriteLock.RecursionMode = ...  # 0x0
        Recursive: QReadWriteLock.RecursionMode = ...  # 0x1
    def __init__(self, recursionMode: QReadWriteLock.RecursionMode = ...) -> None: ...
    def lockForRead(self) -> None: ...
    def lockForWrite(self) -> None: ...
    @overload
    def tryLockForRead(self) -> bool: ...
    @overload
    def tryLockForRead(self, timeout: int) -> bool: ...
    @overload
    def tryLockForWrite(self) -> bool: ...
    @overload
    def tryLockForWrite(self, timeout: int) -> bool: ...
    def unlock(self) -> None: ...

class QRect(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QRect: QRect) -> None: ...
    @overload
    def __init__(self, left: int, top: int, width: int, height: int) -> None: ...
    @overload
    def __init__(self, topleft: QPoint, bottomright: QPoint) -> None: ...
    @overload
    def __init__(self, topleft: QPoint, size: QSize) -> None: ...
    def __add__(self, margins: QMargins) -> QRect: ...
    def __and__(self, r: QRect) -> QRect: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, margins: QMargins) -> QRect: ...
    def __iand__(self, r: QRect) -> QRect: ...
    def __ior__(self, r: QRect) -> QRect: ...
    def __isub__(self, margins: QMargins) -> QRect: ...
    def __or__(self, r: QRect) -> QRect: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, rhs: QMargins) -> QRect: ...
    def adjust(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def adjusted(self, x1: int, y1: int, x2: int, y2: int) -> QRect: ...
    def bottom(self) -> int: ...
    def bottomLeft(self) -> QPoint: ...
    def bottomRight(self) -> QPoint: ...
    def center(self) -> QPoint: ...
    @overload
    def contains(self, p: QPoint | QPointF, proper: bool = ...) -> bool: ...
    @overload
    def contains(self, r: QRect, proper: bool = ...) -> bool: ...
    @overload
    def contains(self, x: int, y: int) -> bool: ...
    @overload
    def contains(self, x: int, y: int, proper: bool) -> bool: ...
    def getCoords(self) -> Tuple[int, int, int, int]: ...
    def getRect(self) -> Tuple[int, int, int, int]: ...
    def height(self) -> int: ...
    def intersected(self, other: QRect) -> QRect: ...
    def intersects(self, r: QRect) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isValid(self) -> bool: ...
    def left(self) -> int: ...
    def marginsAdded(self, margins: QMargins) -> QRect: ...
    def marginsRemoved(self, margins: QMargins) -> QRect: ...
    def moveBottom(self, pos: int) -> None: ...
    def moveBottomLeft(self, p: QPoint) -> None: ...
    def moveBottomRight(self, p: QPoint) -> None: ...
    def moveCenter(self, p: QPoint) -> None: ...
    def moveLeft(self, pos: int) -> None: ...
    def moveRight(self, pos: int) -> None: ...
    @overload
    def moveTo(self, p: QPoint) -> None: ...
    @overload
    def moveTo(self, x: int, t: int) -> None: ...
    def moveTop(self, pos: int) -> None: ...
    def moveTopLeft(self, p: QPoint) -> None: ...
    def moveTopRight(self, p: QPoint) -> None: ...
    def normalized(self) -> QRect: ...
    def right(self) -> int: ...
    def setBottom(self, pos: int) -> None: ...
    def setBottomLeft(self, p: QPoint) -> None: ...
    def setBottomRight(self, p: QPoint) -> None: ...
    def setCoords(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def setHeight(self, h: int) -> None: ...
    def setLeft(self, pos: int) -> None: ...
    def setRect(self, x: int, y: int, w: int, h: int) -> None: ...
    def setRight(self, pos: int) -> None: ...
    def setSize(self, s: QSize) -> None: ...
    def setTop(self, pos: int) -> None: ...
    def setTopLeft(self, p: QPoint) -> None: ...
    def setTopRight(self, p: QPoint) -> None: ...
    def setWidth(self, w: int) -> None: ...
    def setX(self, x: int) -> None: ...
    def setY(self, y: int) -> None: ...
    def size(self) -> QSize: ...
    @staticmethod
    def span(p1: QPoint, p2: QPoint) -> QRect: ...
    def top(self) -> int: ...
    def topLeft(self) -> QPoint: ...
    def topRight(self) -> QPoint: ...
    @overload
    def translate(self, dx: int | float, dy: int | float) -> None: ...
    @overload
    def translate(self, p: QPoint) -> None: ...
    @overload
    def translated(self, dx: int, dy: int) -> QRect: ...
    @overload
    def translated(self, p: QPoint) -> QRect: ...
    def transposed(self) -> QRect: ...
    def united(self, other: QRect) -> QRect: ...
    def width(self) -> int: ...
    def x(self) -> int: ...
    def y(self) -> int: ...

class QRectF(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QRectF: Union[QRectF, QRect]) -> None: ...
    @overload
    def __init__(self, left: float, top: float, width: float, height: float) -> None: ...
    @overload
    def __init__(self, rect: QRect) -> None: ...
    @overload
    def __init__(
        self, topleft: Union[QPointF, QPoint], bottomRight: Union[QPointF, QPoint]
    ) -> None: ...
    @overload
    def __init__(self, topleft: Union[QPointF, QPoint], size: Union[QSizeF, QSize]) -> None: ...
    @overload
    def __add__(self, lhs: Union[QMarginsF, QMargins]) -> QRectF: ...
    @overload
    def __add__(self, rhs: Union[QMarginsF, QMargins]) -> QRectF: ...
    def __and__(self, r: Union[QRectF, QRect]) -> QRectF: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, margins: Union[QMarginsF, QMargins]) -> QRectF: ...
    def __iand__(self, r: Union[QRectF, QRect]) -> QRectF: ...
    def __ior__(self, r: Union[QRectF, QRect]) -> QRectF: ...
    def __isub__(self, margins: Union[QMarginsF, QMargins]) -> QRectF: ...
    def __or__(self, r: Union[QRectF, QRect]) -> QRectF: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, rhs: Union[QMarginsF, QMargins]) -> QRectF: ...
    def adjust(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    def adjusted(self, x1: float, y1: float, x2: float, y2: float) -> QRectF: ...
    def bottom(self) -> float: ...
    def bottomLeft(self) -> QPointF: ...
    def bottomRight(self) -> QPointF: ...
    def center(self) -> QPointF: ...
    @overload
    def contains(self, p: Union[QPointF, QPoint]) -> bool: ...
    @overload
    def contains(self, r: Union[QRectF, QRect]) -> bool: ...
    @overload
    def contains(self, x: float, y: float) -> bool: ...
    def getCoords(self) -> Tuple[float, float, float, float]: ...
    def getRect(self) -> Tuple[float, float, float, float]: ...
    def height(self) -> float: ...
    def intersected(self, other: Union[QRectF, QRect]) -> QRectF: ...
    def intersects(self, r: Union[QRectF, QRect]) -> bool: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isValid(self) -> bool: ...
    def left(self) -> float: ...
    def marginsAdded(self, margins: Union[QMarginsF, QMargins]) -> QRectF: ...
    def marginsRemoved(self, margins: Union[QMarginsF, QMargins]) -> QRectF: ...
    def moveBottom(self, pos: float) -> None: ...
    def moveBottomLeft(self, p: Union[QPointF, QPoint]) -> None: ...
    def moveBottomRight(self, p: Union[QPointF, QPoint]) -> None: ...
    def moveCenter(self, p: Union[QPointF, QPoint]) -> None: ...
    def moveLeft(self, pos: float) -> None: ...
    def moveRight(self, pos: float) -> None: ...
    @overload
    def moveTo(self, p: Union[QPointF, QPoint]) -> None: ...
    @overload
    def moveTo(self, x: float, y: float) -> None: ...
    def moveTop(self, pos: float) -> None: ...
    def moveTopLeft(self, p: Union[QPointF, QPoint]) -> None: ...
    def moveTopRight(self, p: Union[QPointF, QPoint]) -> None: ...
    def normalized(self) -> QRectF: ...
    def right(self) -> float: ...
    def setBottom(self, pos: float) -> None: ...
    def setBottomLeft(self, p: Union[QPointF, QPoint]) -> None: ...
    def setBottomRight(self, p: Union[QPointF, QPoint]) -> None: ...
    def setCoords(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    def setHeight(self, h: float) -> None: ...
    def setLeft(self, pos: float) -> None: ...
    def setRect(self, x: float, y: float, w: float, h: float) -> None: ...
    def setRight(self, pos: float) -> None: ...
    def setSize(self, s: Union[QSizeF, QSize]) -> None: ...
    def setTop(self, pos: float) -> None: ...
    def setTopLeft(self, p: Union[QPointF, QPoint]) -> None: ...
    def setTopRight(self, p: Union[QPointF, QPoint]) -> None: ...
    def setWidth(self, w: float) -> None: ...
    def setX(self, pos: float) -> None: ...
    def setY(self, pos: float) -> None: ...
    def size(self) -> QSizeF: ...
    def toAlignedRect(self) -> QRect: ...
    def toRect(self) -> QRect: ...
    def top(self) -> float: ...
    def topLeft(self) -> QPointF: ...
    def topRight(self) -> QPointF: ...
    @overload
    def translate(self, dx: float, dy: float) -> None: ...
    @overload
    def translate(self, p: Union[QPointF, QPoint]) -> None: ...
    @overload
    def translated(self, dx: float, dy: float) -> QRectF: ...
    @overload
    def translated(self, p: Union[QPointF, QPoint]) -> QRectF: ...
    def transposed(self) -> QRectF: ...
    def united(self, other: Union[QRectF, QRect]) -> QRectF: ...
    def width(self) -> float: ...
    def x(self) -> float: ...
    def y(self) -> float: ...

class QRecursiveMutex(Shiboken.Object):
    def __init__(self) -> None: ...
    def lock(self) -> None: ...
    def tryLock(self, timeout: int = ...) -> bool: ...
    def try_lock(self) -> bool: ...
    def unlock(self) -> None: ...

class QRegularExpression(Shiboken.Object):

    NoMatchOption: QRegularExpression.MatchOption = ...  # 0x0
    AnchorAtOffsetMatchOption: QRegularExpression.MatchOption = ...  # 0x1
    AnchoredMatchOption: QRegularExpression.MatchOption = ...  # 0x1
    DontCheckSubjectStringMatchOption: QRegularExpression.MatchOption = ...  # 0x2
    NormalMatch: QRegularExpression.MatchType = ...  # 0x0
    PartialPreferCompleteMatch: QRegularExpression.MatchType = ...  # 0x1
    PartialPreferFirstMatch: QRegularExpression.MatchType = ...  # 0x2
    NoMatch: QRegularExpression.MatchType = ...  # 0x3
    NoPatternOption: QRegularExpression.PatternOption = ...  # 0x0
    CaseInsensitiveOption: QRegularExpression.PatternOption = ...  # 0x1
    DotMatchesEverythingOption: QRegularExpression.PatternOption = ...  # 0x2
    MultilineOption: QRegularExpression.PatternOption = ...  # 0x4
    ExtendedPatternSyntaxOption: QRegularExpression.PatternOption = ...  # 0x8
    InvertedGreedinessOption: QRegularExpression.PatternOption = ...  # 0x10
    DontCaptureOption: QRegularExpression.PatternOption = ...  # 0x20
    UseUnicodePropertiesOption: QRegularExpression.PatternOption = ...  # 0x40
    DefaultWildcardConversion: QRegularExpression.WildcardConversionOption = ...  # 0x0
    UnanchoredWildcardConversion: QRegularExpression.WildcardConversionOption = ...  # 0x1
    class MatchOption(Enum):

        NoMatchOption: QRegularExpression.MatchOption = ...  # 0x0
        AnchorAtOffsetMatchOption: QRegularExpression.MatchOption = ...  # 0x1
        AnchoredMatchOption: QRegularExpression.MatchOption = ...  # 0x1
        DontCheckSubjectStringMatchOption: QRegularExpression.MatchOption = ...  # 0x2
    class MatchOptions(object): ...
    class MatchType(Enum):

        NormalMatch: QRegularExpression.MatchType = ...  # 0x0
        PartialPreferCompleteMatch: QRegularExpression.MatchType = ...  # 0x1
        PartialPreferFirstMatch: QRegularExpression.MatchType = ...  # 0x2
        NoMatch: QRegularExpression.MatchType = ...  # 0x3
    class PatternOption(Enum):

        NoPatternOption: QRegularExpression.PatternOption = ...  # 0x0
        CaseInsensitiveOption: QRegularExpression.PatternOption = ...  # 0x1
        DotMatchesEverythingOption: QRegularExpression.PatternOption = ...  # 0x2
        MultilineOption: QRegularExpression.PatternOption = ...  # 0x4
        ExtendedPatternSyntaxOption: QRegularExpression.PatternOption = ...  # 0x8
        InvertedGreedinessOption: QRegularExpression.PatternOption = ...  # 0x10
        DontCaptureOption: QRegularExpression.PatternOption = ...  # 0x20
        UseUnicodePropertiesOption: QRegularExpression.PatternOption = ...  # 0x40
    class PatternOptions(object): ...
    class WildcardConversionOption(Enum):

        DefaultWildcardConversion: QRegularExpression.WildcardConversionOption = ...  # 0x0
        UnanchoredWildcardConversion: QRegularExpression.WildcardConversionOption = ...  # 0x1
    class WildcardConversionOptions(object): ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, pattern: str, options: QRegularExpression.PatternOptions = ...) -> None: ...
    @overload
    def __init__(self, re: Union[QRegularExpression, str]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def anchoredPattern(expression: str) -> str: ...
    def captureCount(self) -> int: ...
    def errorString(self) -> str: ...
    @staticmethod
    def escape(str: str) -> str: ...
    @staticmethod
    def fromWildcard(
        pattern: str,
        cs: Qt.CaseSensitivity = ...,
        options: QRegularExpression.WildcardConversionOptions = ...,
    ) -> QRegularExpression: ...
    @overload
    def globalMatch(
        self,
        subject: str,
        offset: int = ...,
        matchType: QRegularExpression.MatchType = ...,
        matchOptions: QRegularExpression.MatchOptions = ...,
    ) -> QRegularExpressionMatchIterator: ...
    @overload
    def globalMatch(
        self,
        subjectView: str,
        offset: int = ...,
        matchType: QRegularExpression.MatchType = ...,
        matchOptions: QRegularExpression.MatchOptions = ...,
    ) -> QRegularExpressionMatchIterator: ...
    def isValid(self) -> bool: ...
    @overload
    def match(
        self,
        subject: str,
        offset: int = ...,
        matchType: QRegularExpression.MatchType = ...,
        matchOptions: QRegularExpression.MatchOptions = ...,
    ) -> QRegularExpressionMatch: ...
    @overload
    def match(
        self,
        subjectView: str,
        offset: int = ...,
        matchType: QRegularExpression.MatchType = ...,
        matchOptions: QRegularExpression.MatchOptions = ...,
    ) -> QRegularExpressionMatch: ...
    def namedCaptureGroups(self) -> List[str]: ...
    def optimize(self) -> None: ...
    def pattern(self) -> str: ...
    def patternErrorOffset(self) -> int: ...
    def patternOptions(self) -> QRegularExpression.PatternOptions: ...
    def setPattern(self, pattern: str) -> None: ...
    def setPatternOptions(self, options: QRegularExpression.PatternOptions) -> None: ...
    def swap(self, other: Union[QRegularExpression, str]) -> None: ...
    @staticmethod
    def wildcardToRegularExpression(
        str: str, options: QRegularExpression.WildcardConversionOptions = ...
    ) -> str: ...

class QRegularExpressionMatch(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, match: QRegularExpressionMatch) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @overload
    def captured(self, name: str) -> str: ...
    @overload
    def captured(self, nth: int = ...) -> str: ...
    @overload
    def capturedEnd(self, name: str) -> int: ...
    @overload
    def capturedEnd(self, nth: int = ...) -> int: ...
    @overload
    def capturedLength(self, name: str) -> int: ...
    @overload
    def capturedLength(self, nth: int = ...) -> int: ...
    @overload
    def capturedStart(self, name: str) -> int: ...
    @overload
    def capturedStart(self, nth: int = ...) -> int: ...
    def capturedTexts(self) -> List[str]: ...
    @overload
    def capturedView(self, name: str) -> str: ...
    @overload
    def capturedView(self, nth: int = ...) -> str: ...
    def hasMatch(self) -> bool: ...
    def hasPartialMatch(self) -> bool: ...
    def isValid(self) -> bool: ...
    def lastCapturedIndex(self) -> int: ...
    def matchOptions(self) -> QRegularExpression.MatchOptions: ...
    def matchType(self) -> QRegularExpression.MatchType: ...
    def regularExpression(self) -> QRegularExpression: ...
    def swap(self, other: QRegularExpressionMatch) -> None: ...

class QRegularExpressionMatchIterator(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, iterator: QRegularExpressionMatchIterator) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def hasNext(self) -> bool: ...
    def isValid(self) -> bool: ...
    def matchOptions(self) -> QRegularExpression.MatchOptions: ...
    def matchType(self) -> QRegularExpression.MatchType: ...
    def next(self) -> QRegularExpressionMatch: ...
    def peekNext(self) -> QRegularExpressionMatch: ...
    def regularExpression(self) -> QRegularExpression: ...
    def swap(self, other: QRegularExpressionMatchIterator) -> None: ...

class QResource(Shiboken.Object):

    NoCompression: QResource.Compression = ...  # 0x0
    ZlibCompression: QResource.Compression = ...  # 0x1
    ZstdCompression: QResource.Compression = ...  # 0x2
    class Compression(Enum):

        NoCompression: QResource.Compression = ...  # 0x0
        ZlibCompression: QResource.Compression = ...  # 0x1
        ZstdCompression: QResource.Compression = ...  # 0x2
    def __init__(self, file: str = ..., locale: Union[QLocale, QLocale.Language] = ...) -> None: ...
    def absoluteFilePath(self) -> str: ...
    def children(self) -> List[str]: ...
    def compressionAlgorithm(self) -> QResource.Compression: ...
    def data(self) -> object: ...
    def fileName(self) -> str: ...
    def isDir(self) -> bool: ...
    def isFile(self) -> bool: ...
    def isValid(self) -> bool: ...
    def lastModified(self) -> QDateTime: ...
    def locale(self) -> QLocale: ...
    @staticmethod
    def registerResource(rccFilename: str, resourceRoot: str = ...) -> bool: ...
    @staticmethod
    def registerResourceData(rccData: bytes, resourceRoot: str = ...) -> bool: ...
    def setFileName(self, file: str) -> None: ...
    def setLocale(self, locale: Union[QLocale, QLocale.Language]) -> None: ...
    def size(self) -> int: ...
    def uncompressedData(self) -> QByteArray: ...
    def uncompressedSize(self) -> int: ...
    @staticmethod
    def unregisterResource(rccFilename: str, resourceRoot: str = ...) -> bool: ...
    @staticmethod
    def unregisterResourceData(rccData: bytes, resourceRoot: str = ...) -> bool: ...

class QRunnable(Shiboken.Object):
    def __init__(self) -> None: ...
    def autoDelete(self) -> bool: ...
    def run(self) -> None: ...
    def setAutoDelete(self, autoDelete: bool) -> None: ...

class QSaveFile(QFileDevice):
    @overload
    def __init__(self, name: str) -> None: ...
    @overload
    def __init__(self, name: str, parent: QObject) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def cancelWriting(self) -> None: ...
    def close(self) -> None: ...
    def commit(self) -> bool: ...
    def directWriteFallback(self) -> bool: ...
    def fileName(self) -> str: ...
    def open(self, flags: QIODeviceBase.OpenMode) -> bool: ...
    def setDirectWriteFallback(self, enabled: bool) -> None: ...
    def setFileName(self, name: str) -> None: ...
    def writeData(self, data: bytes, len: int) -> int: ...

class QSemaphore(Shiboken.Object):
    def __init__(self, n: int = ...) -> None: ...
    def acquire(self, n: int = ...) -> None: ...
    def available(self) -> int: ...
    def release(self, n: int = ...) -> None: ...
    @overload
    def tryAcquire(self, n: int, timeout: int) -> bool: ...
    @overload
    def tryAcquire(self, n: int = ...) -> bool: ...

class QSemaphoreReleaser(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, sem: QSemaphore, n: int = ...) -> None: ...
    def cancel(self) -> QSemaphore: ...
    def semaphore(self) -> QSemaphore: ...
    def swap(self, other: QSemaphoreReleaser) -> None: ...

class QSequentialAnimationGroup(QAnimationGroup):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def addPause(self, msecs: int) -> QPauseAnimation: ...
    def currentAnimation(self) -> QAbstractAnimation: ...
    def duration(self) -> int: ...
    def event(self, event: QEvent) -> bool: ...
    def insertPause(self, index: int, msecs: int) -> QPauseAnimation: ...
    def updateCurrentTime(self, arg__1: int) -> None: ...
    def updateDirection(self, direction: QAbstractAnimation.Direction) -> None: ...
    def updateState(
        self, newState: QAbstractAnimation.State, oldState: QAbstractAnimation.State
    ) -> None: ...

class QSettings(QObject):

    NativeFormat: QSettings.Format = ...  # 0x0
    IniFormat: QSettings.Format = ...  # 0x1
    Registry32Format: QSettings.Format = ...  # 0x2
    Registry64Format: QSettings.Format = ...  # 0x3
    InvalidFormat: QSettings.Format = ...  # 0x10
    CustomFormat1: QSettings.Format = ...  # 0x11
    CustomFormat2: QSettings.Format = ...  # 0x12
    CustomFormat3: QSettings.Format = ...  # 0x13
    CustomFormat4: QSettings.Format = ...  # 0x14
    CustomFormat5: QSettings.Format = ...  # 0x15
    CustomFormat6: QSettings.Format = ...  # 0x16
    CustomFormat7: QSettings.Format = ...  # 0x17
    CustomFormat8: QSettings.Format = ...  # 0x18
    CustomFormat9: QSettings.Format = ...  # 0x19
    CustomFormat10: QSettings.Format = ...  # 0x1a
    CustomFormat11: QSettings.Format = ...  # 0x1b
    CustomFormat12: QSettings.Format = ...  # 0x1c
    CustomFormat13: QSettings.Format = ...  # 0x1d
    CustomFormat14: QSettings.Format = ...  # 0x1e
    CustomFormat15: QSettings.Format = ...  # 0x1f
    CustomFormat16: QSettings.Format = ...  # 0x20
    UserScope: QSettings.Scope = ...  # 0x0
    SystemScope: QSettings.Scope = ...  # 0x1
    NoError: QSettings.Status = ...  # 0x0
    AccessError: QSettings.Status = ...  # 0x1
    FormatError: QSettings.Status = ...  # 0x2
    class Format(Enum):

        NativeFormat: QSettings.Format = ...  # 0x0
        IniFormat: QSettings.Format = ...  # 0x1
        Registry32Format: QSettings.Format = ...  # 0x2
        Registry64Format: QSettings.Format = ...  # 0x3
        InvalidFormat: QSettings.Format = ...  # 0x10
        CustomFormat1: QSettings.Format = ...  # 0x11
        CustomFormat2: QSettings.Format = ...  # 0x12
        CustomFormat3: QSettings.Format = ...  # 0x13
        CustomFormat4: QSettings.Format = ...  # 0x14
        CustomFormat5: QSettings.Format = ...  # 0x15
        CustomFormat6: QSettings.Format = ...  # 0x16
        CustomFormat7: QSettings.Format = ...  # 0x17
        CustomFormat8: QSettings.Format = ...  # 0x18
        CustomFormat9: QSettings.Format = ...  # 0x19
        CustomFormat10: QSettings.Format = ...  # 0x1a
        CustomFormat11: QSettings.Format = ...  # 0x1b
        CustomFormat12: QSettings.Format = ...  # 0x1c
        CustomFormat13: QSettings.Format = ...  # 0x1d
        CustomFormat14: QSettings.Format = ...  # 0x1e
        CustomFormat15: QSettings.Format = ...  # 0x1f
        CustomFormat16: QSettings.Format = ...  # 0x20
    class Scope(Enum):

        UserScope: QSettings.Scope = ...  # 0x0
        SystemScope: QSettings.Scope = ...  # 0x1
    class Status(Enum):

        NoError: QSettings.Status = ...  # 0x0
        AccessError: QSettings.Status = ...  # 0x1
        FormatError: QSettings.Status = ...  # 0x2
    @overload
    def __init__(
        self, fileName: str, format: QSettings.Format, parent: Optional[QObject] = ...
    ) -> None: ...
    @overload
    def __init__(
        self,
        format: QSettings.Format,
        scope: QSettings.Scope,
        organization: str,
        application: str = ...,
        parent: Optional[QObject] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self, organization: str, application: str = ..., parent: Optional[QObject] = ...
    ) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(
        self,
        scope: QSettings.Scope,
        organization: str,
        application: str = ...,
        parent: Optional[QObject] = ...,
    ) -> None: ...
    @overload
    def __init__(self, scope: QSettings.Scope, parent: Optional[QObject] = ...) -> None: ...
    def allKeys(self) -> List[str]: ...
    def applicationName(self) -> str: ...
    def beginGroup(self, prefix: str) -> None: ...
    def beginReadArray(self, prefix: str) -> int: ...
    def beginWriteArray(self, prefix: str, size: int = ...) -> None: ...
    def childGroups(self) -> List[str]: ...
    def childKeys(self) -> List[str]: ...
    def clear(self) -> None: ...
    def contains(self, key: str) -> bool: ...
    @staticmethod
    def defaultFormat() -> QSettings.Format: ...
    def endArray(self) -> None: ...
    def endGroup(self) -> None: ...
    def event(self, event: QEvent) -> bool: ...
    def fallbacksEnabled(self) -> bool: ...
    def fileName(self) -> str: ...
    def format(self) -> QSettings.Format: ...
    def group(self) -> str: ...
    def isAtomicSyncRequired(self) -> bool: ...
    def isWritable(self) -> bool: ...
    def organizationName(self) -> str: ...
    def remove(self, key: str) -> None: ...
    def scope(self) -> QSettings.Scope: ...
    def setArrayIndex(self, i: int) -> None: ...
    def setAtomicSyncRequired(self, enable: bool) -> None: ...
    @staticmethod
    def setDefaultFormat(format: QSettings.Format) -> None: ...
    def setFallbacksEnabled(self, b: bool) -> None: ...
    @staticmethod
    def setPath(format: QSettings.Format, scope: QSettings.Scope, path: str) -> None: ...
    def setValue(self, key: str, value: Any) -> None: ...
    def status(self) -> QSettings.Status: ...
    def sync(self) -> None: ...
    def value(
        self, arg__1: str, defaultValue: Optional[Any] = ..., type: object = ...
    ) -> object: ...

class QSharedMemory(QObject):

    ReadOnly: QSharedMemory.AccessMode = ...  # 0x0
    ReadWrite: QSharedMemory.AccessMode = ...  # 0x1
    NoError: QSharedMemory.SharedMemoryError = ...  # 0x0
    PermissionDenied: QSharedMemory.SharedMemoryError = ...  # 0x1
    InvalidSize: QSharedMemory.SharedMemoryError = ...  # 0x2
    KeyError: QSharedMemory.SharedMemoryError = ...  # 0x3
    AlreadyExists: QSharedMemory.SharedMemoryError = ...  # 0x4
    NotFound: QSharedMemory.SharedMemoryError = ...  # 0x5
    LockError: QSharedMemory.SharedMemoryError = ...  # 0x6
    OutOfResources: QSharedMemory.SharedMemoryError = ...  # 0x7
    UnknownError: QSharedMemory.SharedMemoryError = ...  # 0x8
    class AccessMode(Enum):

        ReadOnly: QSharedMemory.AccessMode = ...  # 0x0
        ReadWrite: QSharedMemory.AccessMode = ...  # 0x1
    class SharedMemoryError(Enum):

        NoError: QSharedMemory.SharedMemoryError = ...  # 0x0
        PermissionDenied: QSharedMemory.SharedMemoryError = ...  # 0x1
        InvalidSize: QSharedMemory.SharedMemoryError = ...  # 0x2
        KeyError: QSharedMemory.SharedMemoryError = ...  # 0x3
        AlreadyExists: QSharedMemory.SharedMemoryError = ...  # 0x4
        NotFound: QSharedMemory.SharedMemoryError = ...  # 0x5
        LockError: QSharedMemory.SharedMemoryError = ...  # 0x6
        OutOfResources: QSharedMemory.SharedMemoryError = ...  # 0x7
        UnknownError: QSharedMemory.SharedMemoryError = ...  # 0x8
    @overload
    def __init__(self, key: str, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def attach(self, mode: QSharedMemory.AccessMode = ...) -> bool: ...
    def constData(self) -> int: ...
    def create(self, size: int, mode: QSharedMemory.AccessMode = ...) -> bool: ...
    def data(self) -> int: ...
    def detach(self) -> bool: ...
    def error(self) -> QSharedMemory.SharedMemoryError: ...
    def errorString(self) -> str: ...
    def isAttached(self) -> bool: ...
    def key(self) -> str: ...
    def lock(self) -> bool: ...
    def nativeKey(self) -> str: ...
    def setKey(self, key: str) -> None: ...
    def setNativeKey(self, key: str) -> None: ...
    def size(self) -> int: ...
    def unlock(self) -> bool: ...

class QSignalBlocker(Shiboken.Object):
    def __init__(self, o: QObject) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, arg__1: object, arg__2: object, arg__3: object) -> None: ...
    def reblock(self) -> None: ...
    def unblock(self) -> None: ...

class QSignalMapper(QObject):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def map(self) -> None: ...
    @overload
    def map(self, sender: QObject) -> None: ...
    @overload
    def mapping(self, id: int) -> QObject: ...
    @overload
    def mapping(self, object: QObject) -> QObject: ...
    @overload
    def mapping(self, text: str) -> QObject: ...
    def removeMappings(self, sender: QObject) -> None: ...
    @overload
    def setMapping(self, sender: QObject, id: int) -> None: ...
    @overload
    def setMapping(self, sender: QObject, object: QObject) -> None: ...
    @overload
    def setMapping(self, sender: QObject, text: str) -> None: ...

class QSize(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QSize: QSize) -> None: ...
    @overload
    def __init__(self, w: int, h: int) -> None: ...
    def __add__(self, s2: QSize) -> QSize: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, arg__1: QSize) -> QSize: ...
    def __imul__(self, c: float) -> QSize: ...
    def __isub__(self, arg__1: QSize) -> QSize: ...
    def __mul__(self, c: float) -> QSize: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, s2: QSize) -> QSize: ...
    def boundedTo(self, arg__1: QSize) -> QSize: ...
    def expandedTo(self, arg__1: QSize) -> QSize: ...
    def grownBy(self, m: QMargins) -> QSize: ...
    def height(self) -> int: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isValid(self) -> bool: ...
    @overload
    def scale(self, s: QSize, mode: Qt.AspectRatioMode) -> None: ...
    @overload
    def scale(self, w: int, h: int, mode: Qt.AspectRatioMode) -> None: ...
    @overload
    def scaled(self, s: QSize, mode: Qt.AspectRatioMode) -> QSize: ...
    @overload
    def scaled(self, w: int, h: int, mode: Qt.AspectRatioMode) -> QSize: ...
    def setHeight(self, h: int) -> None: ...
    def setWidth(self, w: int) -> None: ...
    def shrunkBy(self, m: QMargins) -> QSize: ...
    def toTuple(self) -> object: ...
    def transpose(self) -> None: ...
    def transposed(self) -> QSize: ...
    def width(self) -> int: ...

class QSizeF(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QSizeF: Union[QSizeF, QSize]) -> None: ...
    @overload
    def __init__(self, sz: QSize) -> None: ...
    @overload
    def __init__(self, w: float, h: float) -> None: ...
    def __add__(self, s2: Union[QSizeF, QSize]) -> QSizeF: ...
    @staticmethod
    def __copy__() -> None: ...
    def __iadd__(self, arg__1: Union[QSizeF, QSize]) -> QSizeF: ...
    def __imul__(self, c: float) -> QSizeF: ...
    def __isub__(self, arg__1: Union[QSizeF, QSize]) -> QSizeF: ...
    def __mul__(self, c: float) -> QSizeF: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def __sub__(self, s2: Union[QSizeF, QSize]) -> QSizeF: ...
    def boundedTo(self, arg__1: Union[QSizeF, QSize]) -> QSizeF: ...
    def expandedTo(self, arg__1: Union[QSizeF, QSize]) -> QSizeF: ...
    def grownBy(self, m: Union[QMarginsF, QMargins]) -> QSizeF: ...
    def height(self) -> float: ...
    def isEmpty(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isValid(self) -> bool: ...
    @overload
    def scale(self, s: Union[QSizeF, QSize], mode: Qt.AspectRatioMode) -> None: ...
    @overload
    def scale(self, w: float, h: float, mode: Qt.AspectRatioMode) -> None: ...
    @overload
    def scaled(self, s: Union[QSizeF, QSize], mode: Qt.AspectRatioMode) -> QSizeF: ...
    @overload
    def scaled(self, w: float, h: float, mode: Qt.AspectRatioMode) -> QSizeF: ...
    def setHeight(self, h: float) -> None: ...
    def setWidth(self, w: float) -> None: ...
    def shrunkBy(self, m: Union[QMarginsF, QMargins]) -> QSizeF: ...
    def toSize(self) -> QSize: ...
    def toTuple(self) -> object: ...
    def transpose(self) -> None: ...
    def transposed(self) -> QSizeF: ...
    def width(self) -> float: ...

class QSocketDescriptor(Shiboken.Object):
    @overload
    def __init__(self, QSocketDescriptor: Union[QSocketDescriptor, int]) -> None: ...
    @overload
    def __init__(self, desc: int) -> None: ...
    @overload
    def __init__(self, descriptor: int = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def isValid(self) -> bool: ...
    def winHandle(self) -> int: ...

class QSocketNotifier(QObject):

    Read: QSocketNotifier.Type = ...  # 0x0
    Write: QSocketNotifier.Type = ...  # 0x1
    Exception: QSocketNotifier.Type = ...  # 0x2
    class Type(Enum):

        Read: QSocketNotifier.Type = ...  # 0x0
        Write: QSocketNotifier.Type = ...  # 0x1
        Exception: QSocketNotifier.Type = ...  # 0x2
    @overload
    def __init__(
        self, arg__1: object, arg__2: QSocketNotifier.Type, parent: Optional[QObject] = ...
    ) -> None: ...
    @overload
    def __init__(self, arg__1: QSocketNotifier.Type, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(
        self, socket: int, arg__2: QSocketNotifier.Type, parent: Optional[QObject] = ...
    ) -> None: ...
    def event(self, arg__1: QEvent) -> bool: ...
    def isEnabled(self) -> bool: ...
    def isValid(self) -> bool: ...
    def setEnabled(self, arg__1: bool) -> None: ...
    def setSocket(self, socket: int) -> None: ...
    def socket(self) -> int: ...
    def type(self) -> QSocketNotifier.Type: ...

class QSortFilterProxyModel(QAbstractProxyModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def autoAcceptChildRows(self) -> bool: ...
    def buddy(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def canFetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any: ...
    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def dynamicSortFilter(self) -> bool: ...
    def fetchMore(self, parent: Union[QModelIndex, QPersistentModelIndex]) -> None: ...
    def filterAcceptsColumn(
        self, source_column: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool: ...
    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool: ...
    def filterCaseSensitivity(self) -> Qt.CaseSensitivity: ...
    def filterKeyColumn(self) -> int: ...
    def filterRegularExpression(self) -> QRegularExpression: ...
    def filterRole(self) -> int: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def hasChildren(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> bool: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    def insertColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def invalidate(self) -> None: ...
    def invalidateColumnsFilter(self) -> None: ...
    def invalidateFilter(self) -> None: ...
    def invalidateRowsFilter(self) -> None: ...
    def isRecursiveFilteringEnabled(self) -> bool: ...
    def isSortLocaleAware(self) -> bool: ...
    def lessThan(
        self,
        source_left: Union[QModelIndex, QPersistentModelIndex],
        source_right: Union[QModelIndex, QPersistentModelIndex],
    ) -> bool: ...
    def mapFromSource(
        self, sourceIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def mapSelectionFromSource(self, sourceSelection: QItemSelection) -> QItemSelection: ...
    def mapSelectionToSource(self, proxySelection: QItemSelection) -> QItemSelection: ...
    def mapToSource(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def match(
        self,
        start: Union[QModelIndex, QPersistentModelIndex],
        role: int,
        value: Any,
        hits: int = ...,
        flags: Qt.MatchFlags = ...,
    ) -> List[int]: ...
    def mimeData(self, indexes: List[int]) -> QMimeData: ...
    def mimeTypes(self) -> List[str]: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, child: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def removeColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setAutoAcceptChildRows(self, accept: bool) -> None: ...
    def setData(
        self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = ...
    ) -> bool: ...
    def setDynamicSortFilter(self, enable: bool) -> None: ...
    def setFilterCaseSensitivity(self, cs: Qt.CaseSensitivity) -> None: ...
    def setFilterFixedString(self, pattern: str) -> None: ...
    def setFilterKeyColumn(self, column: int) -> None: ...
    @overload
    def setFilterRegularExpression(self, pattern: str) -> None: ...
    @overload
    def setFilterRegularExpression(
        self, regularExpression: Union[QRegularExpression, str]
    ) -> None: ...
    def setFilterRole(self, role: int) -> None: ...
    def setFilterWildcard(self, pattern: str) -> None: ...
    def setHeaderData(
        self, section: int, orientation: Qt.Orientation, value: Any, role: int = ...
    ) -> bool: ...
    def setRecursiveFilteringEnabled(self, recursive: bool) -> None: ...
    def setSortCaseSensitivity(self, cs: Qt.CaseSensitivity) -> None: ...
    def setSortLocaleAware(self, on: bool) -> None: ...
    def setSortRole(self, role: int) -> None: ...
    def setSourceModel(self, sourceModel: QAbstractItemModel) -> None: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def sort(self, column: int, order: Qt.SortOrder = ...) -> None: ...
    def sortCaseSensitivity(self) -> Qt.CaseSensitivity: ...
    def sortColumn(self) -> int: ...
    def sortOrder(self) -> Qt.SortOrder: ...
    def sortRole(self) -> int: ...
    def span(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize: ...
    def supportedDropActions(self) -> Qt.DropActions: ...

class QStandardPaths(Shiboken.Object):

    LocateFile: QStandardPaths.LocateOption = ...  # 0x0
    LocateDirectory: QStandardPaths.LocateOption = ...  # 0x1
    DesktopLocation: QStandardPaths.StandardLocation = ...  # 0x0
    DocumentsLocation: QStandardPaths.StandardLocation = ...  # 0x1
    FontsLocation: QStandardPaths.StandardLocation = ...  # 0x2
    ApplicationsLocation: QStandardPaths.StandardLocation = ...  # 0x3
    MusicLocation: QStandardPaths.StandardLocation = ...  # 0x4
    MoviesLocation: QStandardPaths.StandardLocation = ...  # 0x5
    PicturesLocation: QStandardPaths.StandardLocation = ...  # 0x6
    TempLocation: QStandardPaths.StandardLocation = ...  # 0x7
    HomeLocation: QStandardPaths.StandardLocation = ...  # 0x8
    AppLocalDataLocation: QStandardPaths.StandardLocation = ...  # 0x9
    CacheLocation: QStandardPaths.StandardLocation = ...  # 0xa
    GenericDataLocation: QStandardPaths.StandardLocation = ...  # 0xb
    RuntimeLocation: QStandardPaths.StandardLocation = ...  # 0xc
    ConfigLocation: QStandardPaths.StandardLocation = ...  # 0xd
    DownloadLocation: QStandardPaths.StandardLocation = ...  # 0xe
    GenericCacheLocation: QStandardPaths.StandardLocation = ...  # 0xf
    GenericConfigLocation: QStandardPaths.StandardLocation = ...  # 0x10
    AppDataLocation: QStandardPaths.StandardLocation = ...  # 0x11
    AppConfigLocation: QStandardPaths.StandardLocation = ...  # 0x12
    class LocateOption(Enum):

        LocateFile: QStandardPaths.LocateOption = ...  # 0x0
        LocateDirectory: QStandardPaths.LocateOption = ...  # 0x1
    class LocateOptions(object): ...
    class StandardLocation(Enum):

        DesktopLocation: QStandardPaths.StandardLocation = ...  # 0x0
        DocumentsLocation: QStandardPaths.StandardLocation = ...  # 0x1
        FontsLocation: QStandardPaths.StandardLocation = ...  # 0x2
        ApplicationsLocation: QStandardPaths.StandardLocation = ...  # 0x3
        MusicLocation: QStandardPaths.StandardLocation = ...  # 0x4
        MoviesLocation: QStandardPaths.StandardLocation = ...  # 0x5
        PicturesLocation: QStandardPaths.StandardLocation = ...  # 0x6
        TempLocation: QStandardPaths.StandardLocation = ...  # 0x7
        HomeLocation: QStandardPaths.StandardLocation = ...  # 0x8
        AppLocalDataLocation: QStandardPaths.StandardLocation = ...  # 0x9
        CacheLocation: QStandardPaths.StandardLocation = ...  # 0xa
        GenericDataLocation: QStandardPaths.StandardLocation = ...  # 0xb
        RuntimeLocation: QStandardPaths.StandardLocation = ...  # 0xc
        ConfigLocation: QStandardPaths.StandardLocation = ...  # 0xd
        DownloadLocation: QStandardPaths.StandardLocation = ...  # 0xe
        GenericCacheLocation: QStandardPaths.StandardLocation = ...  # 0xf
        GenericConfigLocation: QStandardPaths.StandardLocation = ...  # 0x10
        AppDataLocation: QStandardPaths.StandardLocation = ...  # 0x11
        AppConfigLocation: QStandardPaths.StandardLocation = ...  # 0x12
    @staticmethod
    def displayName(type: QStandardPaths.StandardLocation) -> str: ...
    @staticmethod
    def findExecutable(executableName: str, paths: Sequence[str] = ...) -> str: ...
    @staticmethod
    def isTestModeEnabled() -> bool: ...
    @staticmethod
    def locate(
        type: QStandardPaths.StandardLocation,
        fileName: str,
        options: QStandardPaths.LocateOptions = ...,
    ) -> str: ...
    @staticmethod
    def locateAll(
        type: QStandardPaths.StandardLocation,
        fileName: str,
        options: QStandardPaths.LocateOptions = ...,
    ) -> List[str]: ...
    @staticmethod
    def setTestModeEnabled(testMode: bool) -> None: ...
    @staticmethod
    def standardLocations(type: QStandardPaths.StandardLocation) -> List[str]: ...
    @staticmethod
    def writableLocation(type: QStandardPaths.StandardLocation) -> str: ...

class QStorageInfo(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, dir: Union[QDir, str]) -> None: ...
    @overload
    def __init__(self, other: QStorageInfo) -> None: ...
    @overload
    def __init__(self, path: str) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def blockSize(self) -> int: ...
    def bytesAvailable(self) -> int: ...
    def bytesFree(self) -> int: ...
    def bytesTotal(self) -> int: ...
    def device(self) -> QByteArray: ...
    def displayName(self) -> str: ...
    def fileSystemType(self) -> QByteArray: ...
    def isReadOnly(self) -> bool: ...
    def isReady(self) -> bool: ...
    def isRoot(self) -> bool: ...
    def isValid(self) -> bool: ...
    @staticmethod
    def mountedVolumes() -> List[QStorageInfo]: ...
    def name(self) -> str: ...
    def refresh(self) -> None: ...
    @staticmethod
    def root() -> QStorageInfo: ...
    def rootPath(self) -> str: ...
    def setPath(self, path: str) -> None: ...
    def subvolume(self) -> QByteArray: ...
    def swap(self, other: QStorageInfo) -> None: ...

class QStringConverter(QStringConverterBase):

    Utf8: QStringConverter.Encoding = ...  # 0x0
    Utf16: QStringConverter.Encoding = ...  # 0x1
    Utf16LE: QStringConverter.Encoding = ...  # 0x2
    Utf16BE: QStringConverter.Encoding = ...  # 0x3
    Utf32: QStringConverter.Encoding = ...  # 0x4
    Utf32LE: QStringConverter.Encoding = ...  # 0x5
    Utf32BE: QStringConverter.Encoding = ...  # 0x6
    Latin1: QStringConverter.Encoding = ...  # 0x7
    LastEncoding: QStringConverter.Encoding = ...  # 0x8
    System: QStringConverter.Encoding = ...  # 0x8
    class Encoding(Enum):

        Utf8: QStringConverter.Encoding = ...  # 0x0
        Utf16: QStringConverter.Encoding = ...  # 0x1
        Utf16LE: QStringConverter.Encoding = ...  # 0x2
        Utf16BE: QStringConverter.Encoding = ...  # 0x3
        Utf32: QStringConverter.Encoding = ...  # 0x4
        Utf32LE: QStringConverter.Encoding = ...  # 0x5
        Utf32BE: QStringConverter.Encoding = ...  # 0x6
        Latin1: QStringConverter.Encoding = ...  # 0x7
        LastEncoding: QStringConverter.Encoding = ...  # 0x8
        System: QStringConverter.Encoding = ...  # 0x8
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, encoding: QStringConverter.Encoding, f: QStringConverterBase.Flags
    ) -> None: ...
    @overload
    def __init__(self, name: bytes, f: QStringConverterBase.Flags) -> None: ...
    def hasError(self) -> bool: ...
    def isValid(self) -> bool: ...
    def name(self) -> bytes: ...
    @staticmethod
    def nameForEncoding(e: QStringConverter.Encoding) -> bytes: ...
    def resetState(self) -> None: ...

class QStringConverterBase(Shiboken.Object):
    class Flag(Enum):

        Default: QStringConverterBase.Flag = ...  # 0x0
        Stateless: QStringConverterBase.Flag = ...  # 0x1
        ConvertInvalidToNull: QStringConverterBase.Flag = ...  # 0x2
        WriteBom: QStringConverterBase.Flag = ...  # 0x4
        ConvertInitialBom: QStringConverterBase.Flag = ...  # 0x8
    class Flags(object): ...
    class State(Shiboken.Object):
        def __init__(self, f: QStringConverterBase.Flags = ...) -> None: ...
        def clear(self) -> None: ...
    def __init__(self) -> None: ...

class QStringDecoder(QStringConverter):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, encoding: QStringConverter.Encoding, flags: QStringConverterBase.Flags = ...
    ) -> None: ...
    @overload
    def __init__(self, name: bytes, f: QStringConverterBase.Flags = ...) -> None: ...
    def appendToBuffer(self, out: bytes, ba: Union[QByteArray, bytes]) -> bytes: ...
    def requiredSpace(self, inputLength: int) -> int: ...

class QStringEncoder(QStringConverter):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, encoding: QStringConverter.Encoding, flags: QStringConverterBase.Flags = ...
    ) -> None: ...
    @overload
    def __init__(self, name: bytes, flags: QStringConverterBase.Flags = ...) -> None: ...
    def requiredSpace(self, inputLength: int) -> int: ...

class QStringListModel(QAbstractListModel):
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, strings: Sequence[str], parent: Optional[QObject] = ...) -> None: ...
    def clearItemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> bool: ...
    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any: ...
    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags: ...
    def insertRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def itemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Dict[int, Any]: ...
    def moveRows(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceRow: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def removeRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setData(
        self, index: Union[QModelIndex, QPersistentModelIndex], value: Any, role: int = ...
    ) -> bool: ...
    def setItemData(
        self, index: Union[QModelIndex, QPersistentModelIndex], roles: Dict[int, Any]
    ) -> bool: ...
    def setStringList(self, strings: Sequence[str]) -> None: ...
    def sibling(
        self, row: int, column: int, idx: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def sort(self, column: int, order: Qt.SortOrder = ...) -> None: ...
    def stringList(self) -> List[str]: ...
    def supportedDropActions(self) -> Qt.DropActions: ...

class QSysInfo(Shiboken.Object):

    BigEndian: QSysInfo.Endian = ...  # 0x0
    ByteOrder: QSysInfo.Endian = ...  # 0x1
    LittleEndian: QSysInfo.Endian = ...  # 0x1
    WordSize: QSysInfo.Sizes = ...  # 0x40
    class Endian(Enum):

        BigEndian: QSysInfo.Endian = ...  # 0x0
        ByteOrder: QSysInfo.Endian = ...  # 0x1
        LittleEndian: QSysInfo.Endian = ...  # 0x1
    class Sizes(Enum):

        WordSize: QSysInfo.Sizes = ...  # 0x40
    def __init__(self) -> None: ...
    @staticmethod
    def bootUniqueId() -> QByteArray: ...
    @staticmethod
    def buildAbi() -> str: ...
    @staticmethod
    def buildCpuArchitecture() -> str: ...
    @staticmethod
    def currentCpuArchitecture() -> str: ...
    @staticmethod
    def kernelType() -> str: ...
    @staticmethod
    def kernelVersion() -> str: ...
    @staticmethod
    def machineHostName() -> str: ...
    @staticmethod
    def machineUniqueId() -> QByteArray: ...
    @staticmethod
    def prettyProductName() -> str: ...
    @staticmethod
    def productType() -> str: ...
    @staticmethod
    def productVersion() -> str: ...

class QSystemSemaphore(Shiboken.Object):

    Open: QSystemSemaphore.AccessMode = ...  # 0x0
    Create: QSystemSemaphore.AccessMode = ...  # 0x1
    NoError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x0
    PermissionDenied: QSystemSemaphore.SystemSemaphoreError = ...  # 0x1
    KeyError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x2
    AlreadyExists: QSystemSemaphore.SystemSemaphoreError = ...  # 0x3
    NotFound: QSystemSemaphore.SystemSemaphoreError = ...  # 0x4
    OutOfResources: QSystemSemaphore.SystemSemaphoreError = ...  # 0x5
    UnknownError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x6
    class AccessMode(Enum):

        Open: QSystemSemaphore.AccessMode = ...  # 0x0
        Create: QSystemSemaphore.AccessMode = ...  # 0x1
    class SystemSemaphoreError(Enum):

        NoError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x0
        PermissionDenied: QSystemSemaphore.SystemSemaphoreError = ...  # 0x1
        KeyError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x2
        AlreadyExists: QSystemSemaphore.SystemSemaphoreError = ...  # 0x3
        NotFound: QSystemSemaphore.SystemSemaphoreError = ...  # 0x4
        OutOfResources: QSystemSemaphore.SystemSemaphoreError = ...  # 0x5
        UnknownError: QSystemSemaphore.SystemSemaphoreError = ...  # 0x6
    def __init__(
        self, key: str, initialValue: int = ..., mode: QSystemSemaphore.AccessMode = ...
    ) -> None: ...
    def acquire(self) -> bool: ...
    def error(self) -> QSystemSemaphore.SystemSemaphoreError: ...
    def errorString(self) -> str: ...
    def key(self) -> str: ...
    def release(self, n: int = ...) -> bool: ...
    def setKey(
        self, key: str, initialValue: int = ..., mode: QSystemSemaphore.AccessMode = ...
    ) -> None: ...

class QTemporaryDir(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, templateName: str) -> None: ...
    def autoRemove(self) -> bool: ...
    def errorString(self) -> str: ...
    def filePath(self, fileName: str) -> str: ...
    def isValid(self) -> bool: ...
    def path(self) -> str: ...
    def remove(self) -> bool: ...
    def setAutoRemove(self, b: bool) -> None: ...

class QTemporaryFile(QFile):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, parent: QObject) -> None: ...
    @overload
    def __init__(self, templateName: str) -> None: ...
    @overload
    def __init__(self, templateName: str, parent: QObject) -> None: ...
    def autoRemove(self) -> bool: ...
    @overload
    @staticmethod
    def createNativeFile(file: QFile) -> QTemporaryFile: ...
    @overload
    @staticmethod
    def createNativeFile(fileName: str) -> QTemporaryFile: ...
    def fileName(self) -> str: ...
    def fileTemplate(self) -> str: ...
    @overload
    def open(self) -> bool: ...
    @overload
    def open(self, flags: QIODeviceBase.OpenMode) -> bool: ...
    def rename(self, newName: Union[str, bytes, os.PathLike]) -> bool: ...
    def setAutoRemove(self, b: bool) -> None: ...
    def setFileTemplate(self, name: str) -> None: ...

class QTextBoundaryFinder(Shiboken.Object):

    NotAtBoundary: QTextBoundaryFinder.BoundaryReason = ...  # 0x0
    BreakOpportunity: QTextBoundaryFinder.BoundaryReason = ...  # 0x1f
    StartOfItem: QTextBoundaryFinder.BoundaryReason = ...  # 0x20
    EndOfItem: QTextBoundaryFinder.BoundaryReason = ...  # 0x40
    MandatoryBreak: QTextBoundaryFinder.BoundaryReason = ...  # 0x80
    SoftHyphen: QTextBoundaryFinder.BoundaryReason = ...  # 0x100
    Grapheme: QTextBoundaryFinder.BoundaryType = ...  # 0x0
    Word: QTextBoundaryFinder.BoundaryType = ...  # 0x1
    Sentence: QTextBoundaryFinder.BoundaryType = ...  # 0x2
    Line: QTextBoundaryFinder.BoundaryType = ...  # 0x3
    class BoundaryReason(Enum):

        NotAtBoundary: QTextBoundaryFinder.BoundaryReason = ...  # 0x0
        BreakOpportunity: QTextBoundaryFinder.BoundaryReason = ...  # 0x1f
        StartOfItem: QTextBoundaryFinder.BoundaryReason = ...  # 0x20
        EndOfItem: QTextBoundaryFinder.BoundaryReason = ...  # 0x40
        MandatoryBreak: QTextBoundaryFinder.BoundaryReason = ...  # 0x80
        SoftHyphen: QTextBoundaryFinder.BoundaryReason = ...  # 0x100
    class BoundaryReasons(object): ...
    class BoundaryType(Enum):

        Grapheme: QTextBoundaryFinder.BoundaryType = ...  # 0x0
        Word: QTextBoundaryFinder.BoundaryType = ...  # 0x1
        Sentence: QTextBoundaryFinder.BoundaryType = ...  # 0x2
        Line: QTextBoundaryFinder.BoundaryType = ...  # 0x3
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QTextBoundaryFinder) -> None: ...
    @overload
    def __init__(
        self,
        type: QTextBoundaryFinder.BoundaryType,
        str: str,
        buffer: Optional[bytes] = ...,
        bufferSize: int = ...,
    ) -> None: ...
    @overload
    def __init__(self, type: QTextBoundaryFinder.BoundaryType, string: str) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def boundaryReasons(self) -> QTextBoundaryFinder.BoundaryReasons: ...
    def isAtBoundary(self) -> bool: ...
    def isValid(self) -> bool: ...
    def position(self) -> int: ...
    def setPosition(self, position: int) -> None: ...
    def string(self) -> str: ...
    def toEnd(self) -> None: ...
    def toNextBoundary(self) -> int: ...
    def toPreviousBoundary(self) -> int: ...
    def toStart(self) -> None: ...
    def type(self) -> QTextBoundaryFinder.BoundaryType: ...

class QTextStream(QIODeviceBase):

    AlignLeft: QTextStream.FieldAlignment = ...  # 0x0
    AlignRight: QTextStream.FieldAlignment = ...  # 0x1
    AlignCenter: QTextStream.FieldAlignment = ...  # 0x2
    AlignAccountingStyle: QTextStream.FieldAlignment = ...  # 0x3
    ShowBase: QTextStream.NumberFlag = ...  # 0x1
    ForcePoint: QTextStream.NumberFlag = ...  # 0x2
    ForceSign: QTextStream.NumberFlag = ...  # 0x4
    UppercaseBase: QTextStream.NumberFlag = ...  # 0x8
    UppercaseDigits: QTextStream.NumberFlag = ...  # 0x10
    SmartNotation: QTextStream.RealNumberNotation = ...  # 0x0
    FixedNotation: QTextStream.RealNumberNotation = ...  # 0x1
    ScientificNotation: QTextStream.RealNumberNotation = ...  # 0x2
    Ok: QTextStream.Status = ...  # 0x0
    ReadPastEnd: QTextStream.Status = ...  # 0x1
    ReadCorruptData: QTextStream.Status = ...  # 0x2
    WriteFailed: QTextStream.Status = ...  # 0x3
    class FieldAlignment(Enum):

        AlignLeft: QTextStream.FieldAlignment = ...  # 0x0
        AlignRight: QTextStream.FieldAlignment = ...  # 0x1
        AlignCenter: QTextStream.FieldAlignment = ...  # 0x2
        AlignAccountingStyle: QTextStream.FieldAlignment = ...  # 0x3
    class NumberFlag(Enum):

        ShowBase: QTextStream.NumberFlag = ...  # 0x1
        ForcePoint: QTextStream.NumberFlag = ...  # 0x2
        ForceSign: QTextStream.NumberFlag = ...  # 0x4
        UppercaseBase: QTextStream.NumberFlag = ...  # 0x8
        UppercaseDigits: QTextStream.NumberFlag = ...  # 0x10
    class NumberFlags(object): ...
    class RealNumberNotation(Enum):

        SmartNotation: QTextStream.RealNumberNotation = ...  # 0x0
        FixedNotation: QTextStream.RealNumberNotation = ...  # 0x1
        ScientificNotation: QTextStream.RealNumberNotation = ...  # 0x2
    class Status(Enum):

        Ok: QTextStream.Status = ...  # 0x0
        ReadPastEnd: QTextStream.Status = ...  # 0x1
        ReadCorruptData: QTextStream.Status = ...  # 0x2
        WriteFailed: QTextStream.Status = ...  # 0x3
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, array: Union[QByteArray, bytes], openMode: QIODeviceBase.OpenMode = ...
    ) -> None: ...
    @overload
    def __init__(self, device: QIODevice) -> None: ...
    @overload
    def __lshift__(self, array: Union[QByteArray, bytes]) -> QTextStream: ...
    @overload
    def __lshift__(self, ch: str) -> QTextStream: ...
    @overload
    def __lshift__(self, ch: int) -> QTextStream: ...
    @overload
    def __lshift__(self, f: float) -> QTextStream: ...
    @overload
    def __lshift__(self, i: int) -> QTextStream: ...
    @overload
    def __lshift__(self, i: int) -> QTextStream: ...
    @overload
    def __lshift__(self, m: QTextStreamManipulator) -> QTextStream: ...
    @overload
    def __lshift__(self, s: str) -> QTextStream: ...
    def __rshift__(self, array: Union[QByteArray, bytes]) -> QTextStream: ...
    def atEnd(self) -> bool: ...
    def autoDetectUnicode(self) -> bool: ...
    def device(self) -> QIODevice: ...
    def encoding(self) -> QStringConverter.Encoding: ...
    def fieldAlignment(self) -> QTextStream.FieldAlignment: ...
    def fieldWidth(self) -> int: ...
    def flush(self) -> None: ...
    def generateByteOrderMark(self) -> bool: ...
    def integerBase(self) -> int: ...
    def locale(self) -> QLocale: ...
    def numberFlags(self) -> QTextStream.NumberFlags: ...
    def padChar(self) -> str: ...
    def pos(self) -> int: ...
    def read(self, maxlen: int) -> str: ...
    def readAll(self) -> str: ...
    def readLine(self, maxlen: int = ...) -> str: ...
    def realNumberNotation(self) -> QTextStream.RealNumberNotation: ...
    def realNumberPrecision(self) -> int: ...
    def reset(self) -> None: ...
    def resetStatus(self) -> None: ...
    def seek(self, pos: int) -> bool: ...
    def setAutoDetectUnicode(self, enabled: bool) -> None: ...
    def setDevice(self, device: QIODevice) -> None: ...
    def setEncoding(self, encoding: QStringConverter.Encoding) -> None: ...
    def setFieldAlignment(self, alignment: QTextStream.FieldAlignment) -> None: ...
    def setFieldWidth(self, width: int) -> None: ...
    def setGenerateByteOrderMark(self, generate: bool) -> None: ...
    def setIntegerBase(self, base: int) -> None: ...
    def setLocale(self, locale: Union[QLocale, QLocale.Language]) -> None: ...
    def setNumberFlags(self, flags: QTextStream.NumberFlags) -> None: ...
    def setPadChar(self, ch: str) -> None: ...
    def setRealNumberNotation(self, notation: QTextStream.RealNumberNotation) -> None: ...
    def setRealNumberPrecision(self, precision: int) -> None: ...
    def setStatus(self, status: QTextStream.Status) -> None: ...
    def skipWhiteSpace(self) -> None: ...
    def status(self) -> QTextStream.Status: ...
    def string(self) -> List[str]: ...

class QTextStreamManipulator(Shiboken.Object):
    @staticmethod
    def __copy__() -> None: ...
    def exec(self, s: QTextStream) -> None: ...
    def exec_(self, arg__1: QTextStream) -> None: ...

class QThread(QObject):
    finished: QtCore.Signal = ...

    IdlePriority: QThread.Priority = ...  # 0x0
    LowestPriority: QThread.Priority = ...  # 0x1
    LowPriority: QThread.Priority = ...  # 0x2
    NormalPriority: QThread.Priority = ...  # 0x3
    HighPriority: QThread.Priority = ...  # 0x4
    HighestPriority: QThread.Priority = ...  # 0x5
    TimeCriticalPriority: QThread.Priority = ...  # 0x6
    InheritPriority: QThread.Priority = ...  # 0x7
    class Priority(Enum):

        IdlePriority: QThread.Priority = ...  # 0x0
        LowestPriority: QThread.Priority = ...  # 0x1
        LowPriority: QThread.Priority = ...  # 0x2
        NormalPriority: QThread.Priority = ...  # 0x3
        HighPriority: QThread.Priority = ...  # 0x4
        HighestPriority: QThread.Priority = ...  # 0x5
        TimeCriticalPriority: QThread.Priority = ...  # 0x6
        InheritPriority: QThread.Priority = ...  # 0x7
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    @staticmethod
    def currentThread() -> QThread: ...
    def event(self, event: QEvent) -> bool: ...
    def eventDispatcher(self) -> QAbstractEventDispatcher: ...
    def exec(self) -> int: ...
    def exec_(self) -> int: ...
    def exit(self, retcode: int = ...) -> None: ...
    @staticmethod
    def idealThreadCount() -> int: ...
    def isFinished(self) -> bool: ...
    def isInterruptionRequested(self) -> bool: ...
    def isRunning(self) -> bool: ...
    def loopLevel(self) -> int: ...
    @staticmethod
    def msleep(arg__1: int) -> None: ...
    def priority(self) -> QThread.Priority: ...
    def quit(self) -> None: ...
    def requestInterruption(self) -> None: ...
    def run(self) -> None: ...
    def setEventDispatcher(self, eventDispatcher: QAbstractEventDispatcher) -> None: ...
    def setPriority(self, priority: QThread.Priority) -> None: ...
    def setStackSize(self, stackSize: int) -> None: ...
    @staticmethod
    def setTerminationEnabled(enabled: bool = ...) -> None: ...
    @staticmethod
    def sleep(arg__1: int) -> None: ...
    def stackSize(self) -> int: ...
    def start(self, priority: QThread.Priority = ...) -> None: ...
    def terminate(self) -> None: ...
    @staticmethod
    def usleep(arg__1: int) -> None: ...
    @overload
    def wait(
        self,
        deadline: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int] = ...,
    ) -> bool: ...
    @overload
    def wait(self, time: int) -> bool: ...
    @staticmethod
    def yieldCurrentThread() -> None: ...

class QThreadPool(QObject):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def activeThreadCount(self) -> int: ...
    def clear(self) -> None: ...
    def contains(self, thread: QThread) -> bool: ...
    def expiryTimeout(self) -> int: ...
    @staticmethod
    def globalInstance() -> QThreadPool: ...
    def maxThreadCount(self) -> int: ...
    def releaseThread(self) -> None: ...
    def reserveThread(self) -> None: ...
    def setExpiryTimeout(self, expiryTimeout: int) -> None: ...
    def setMaxThreadCount(self, maxThreadCount: int) -> None: ...
    def setStackSize(self, stackSize: int) -> None: ...
    def setThreadPriority(self, priority: QThread.Priority) -> None: ...
    def stackSize(self) -> int: ...
    @overload
    def start(self, arg__1: Callable, priority: int = ...) -> None: ...
    @overload
    def start(self, runnable: QRunnable, priority: int = ...) -> None: ...
    def threadPriority(self) -> QThread.Priority: ...
    @overload
    def tryStart(self, arg__1: Callable) -> bool: ...
    @overload
    def tryStart(self, runnable: QRunnable) -> bool: ...
    def tryTake(self, runnable: QRunnable) -> bool: ...
    def waitForDone(self, msecs: int = ...) -> bool: ...

class QTime(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QTime: QTime) -> None: ...
    @overload
    def __init__(self, h: int, m: int, s: int = ..., ms: int = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def addMSecs(self, ms: int) -> QTime: ...
    def addSecs(self, secs: int) -> QTime: ...
    @staticmethod
    def currentTime() -> QTime: ...
    @staticmethod
    def fromMSecsSinceStartOfDay(msecs: int) -> QTime: ...
    @overload
    @staticmethod
    def fromString(string: str, format: Qt.DateFormat = ...) -> QTime: ...
    @overload
    @staticmethod
    def fromString(string: str, format: str) -> QTime: ...
    def hour(self) -> int: ...
    def isNull(self) -> bool: ...
    @overload
    @staticmethod
    def isValid(h: int, m: int, s: int, ms: int = ...) -> bool: ...
    @overload
    def isValid(self) -> bool: ...
    def minute(self) -> int: ...
    def msec(self) -> int: ...
    def msecsSinceStartOfDay(self) -> int: ...
    def msecsTo(self, t: QTime) -> int: ...
    def second(self) -> int: ...
    def secsTo(self, t: QTime) -> int: ...
    def setHMS(self, h: int, m: int, s: int, ms: int = ...) -> bool: ...
    def toPython(self) -> object: ...
    @overload
    def toString(self, f: Qt.DateFormat = ...) -> str: ...
    @overload
    def toString(self, format: str) -> str: ...

class QTimeLine(QObject):

    Forward: QTimeLine.Direction = ...  # 0x0
    Backward: QTimeLine.Direction = ...  # 0x1
    NotRunning: QTimeLine.State = ...  # 0x0
    Paused: QTimeLine.State = ...  # 0x1
    Running: QTimeLine.State = ...  # 0x2
    class Direction(Enum):

        Forward: QTimeLine.Direction = ...  # 0x0
        Backward: QTimeLine.Direction = ...  # 0x1
    class State(Enum):

        NotRunning: QTimeLine.State = ...  # 0x0
        Paused: QTimeLine.State = ...  # 0x1
        Running: QTimeLine.State = ...  # 0x2
    def __init__(self, duration: int = ..., parent: Optional[QObject] = ...) -> None: ...
    def currentFrame(self) -> int: ...
    def currentTime(self) -> int: ...
    def currentValue(self) -> float: ...
    def direction(self) -> QTimeLine.Direction: ...
    def duration(self) -> int: ...
    def easingCurve(self) -> QEasingCurve: ...
    def endFrame(self) -> int: ...
    def frameForTime(self, msec: int) -> int: ...
    def loopCount(self) -> int: ...
    def resume(self) -> None: ...
    def setCurrentTime(self, msec: int) -> None: ...
    def setDirection(self, direction: QTimeLine.Direction) -> None: ...
    def setDuration(self, duration: int) -> None: ...
    def setEasingCurve(self, curve: Union[QEasingCurve, QEasingCurve.Type]) -> None: ...
    def setEndFrame(self, frame: int) -> None: ...
    def setFrameRange(self, startFrame: int, endFrame: int) -> None: ...
    def setLoopCount(self, count: int) -> None: ...
    def setPaused(self, paused: bool) -> None: ...
    def setStartFrame(self, frame: int) -> None: ...
    def setUpdateInterval(self, interval: int) -> None: ...
    def start(self) -> None: ...
    def startFrame(self) -> int: ...
    def state(self) -> QTimeLine.State: ...
    def stop(self) -> None: ...
    def timerEvent(self, event: QTimerEvent) -> None: ...
    def toggleDirection(self) -> None: ...
    def updateInterval(self) -> int: ...
    def valueForTime(self, msec: int) -> float: ...

class QTimeZone(Shiboken.Object):

    DefaultName: QTimeZone.NameType = ...  # 0x0
    LongName: QTimeZone.NameType = ...  # 0x1
    ShortName: QTimeZone.NameType = ...  # 0x2
    OffsetName: QTimeZone.NameType = ...  # 0x3
    StandardTime: QTimeZone.TimeType = ...  # 0x0
    DaylightTime: QTimeZone.TimeType = ...  # 0x1
    GenericTime: QTimeZone.TimeType = ...  # 0x2
    class NameType(Enum):

        DefaultName: QTimeZone.NameType = ...  # 0x0
        LongName: QTimeZone.NameType = ...  # 0x1
        ShortName: QTimeZone.NameType = ...  # 0x2
        OffsetName: QTimeZone.NameType = ...  # 0x3
    class OffsetData(Shiboken.Object):
        @overload
        def __init__(self) -> None: ...
        @overload
        def __init__(self, OffsetData: QTimeZone.OffsetData) -> None: ...
        @staticmethod
        def __copy__() -> None: ...
    class TimeType(Enum):

        StandardTime: QTimeZone.TimeType = ...  # 0x0
        DaylightTime: QTimeZone.TimeType = ...  # 0x1
        GenericTime: QTimeZone.TimeType = ...  # 0x2
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, ianaId: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, offsetSeconds: int) -> None: ...
    @overload
    def __init__(self, other: QTimeZone) -> None: ...
    @overload
    def __init__(
        self,
        zoneId: Union[QByteArray, bytes],
        offsetSeconds: int,
        name: str,
        abbreviation: str,
        territory: QLocale.Country = ...,
        comment: str = ...,
    ) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def abbreviation(self, atDateTime: QDateTime) -> str: ...
    @overload
    @staticmethod
    def availableTimeZoneIds() -> List[QByteArray]: ...
    @overload
    @staticmethod
    def availableTimeZoneIds(offsetSeconds: int) -> List[QByteArray]: ...
    @overload
    @staticmethod
    def availableTimeZoneIds(territory: QLocale.Country) -> List[QByteArray]: ...
    def comment(self) -> str: ...
    def country(self) -> QLocale.Country: ...
    def daylightTimeOffset(self, atDateTime: QDateTime) -> int: ...
    @overload
    def displayName(
        self,
        atDateTime: QDateTime,
        nameType: QTimeZone.NameType = ...,
        locale: Union[QLocale, QLocale.Language] = ...,
    ) -> str: ...
    @overload
    def displayName(
        self,
        timeType: QTimeZone.TimeType,
        nameType: QTimeZone.NameType = ...,
        locale: Union[QLocale, QLocale.Language] = ...,
    ) -> str: ...
    def hasDaylightTime(self) -> bool: ...
    def hasTransitions(self) -> bool: ...
    @staticmethod
    def ianaIdToWindowsId(ianaId: Union[QByteArray, bytes]) -> QByteArray: ...
    def id(self) -> QByteArray: ...
    def isDaylightTime(self, atDateTime: QDateTime) -> bool: ...
    @staticmethod
    def isTimeZoneIdAvailable(ianaId: Union[QByteArray, bytes]) -> bool: ...
    def isValid(self) -> bool: ...
    def nextTransition(self, afterDateTime: QDateTime) -> QTimeZone.OffsetData: ...
    def offsetData(self, forDateTime: QDateTime) -> QTimeZone.OffsetData: ...
    def offsetFromUtc(self, atDateTime: QDateTime) -> int: ...
    def previousTransition(self, beforeDateTime: QDateTime) -> QTimeZone.OffsetData: ...
    def standardTimeOffset(self, atDateTime: QDateTime) -> int: ...
    def swap(self, other: QTimeZone) -> None: ...
    @staticmethod
    def systemTimeZone() -> QTimeZone: ...
    @staticmethod
    def systemTimeZoneId() -> QByteArray: ...
    def territory(self) -> QLocale.Country: ...
    def transitions(
        self, fromDateTime: QDateTime, toDateTime: QDateTime
    ) -> List[QTimeZone.OffsetData]: ...
    @staticmethod
    def utc() -> QTimeZone: ...
    @overload
    @staticmethod
    def windowsIdToDefaultIanaId(windowsId: Union[QByteArray, bytes]) -> QByteArray: ...
    @overload
    @staticmethod
    def windowsIdToDefaultIanaId(
        windowsId: Union[QByteArray, bytes], territory: QLocale.Country
    ) -> QByteArray: ...
    @overload
    @staticmethod
    def windowsIdToIanaIds(windowsId: Union[QByteArray, bytes]) -> List[QByteArray]: ...
    @overload
    @staticmethod
    def windowsIdToIanaIds(
        windowsId: Union[QByteArray, bytes], territory: QLocale.Country
    ) -> List[QByteArray]: ...

class QTimer(QObject):
    timeout: Signal = ...
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def interval(self) -> int: ...
    def isActive(self) -> bool: ...
    def isSingleShot(self) -> bool: ...
    def killTimer(self, arg__1: int) -> None: ...
    def remainingTime(self) -> int: ...
    def setInterval(self, msec: int) -> None: ...
    def setSingleShot(self, singleShot: bool) -> None: ...
    def setTimerType(self, atype: Qt.TimerType) -> None: ...
    @overload
    @staticmethod
    def singleShot(arg__1: int, arg__2: Callable) -> None: ...
    @overload
    @staticmethod
    def singleShot(msec: int, receiver: QObject, member: bytes) -> None: ...
    @overload
    @staticmethod
    def singleShot(
        msec: int, timerType: Qt.TimerType, receiver: QObject, member: bytes
    ) -> None: ...
    @overload
    def start(self) -> None: ...
    @overload
    def start(self, msec: int) -> None: ...
    def stop(self) -> None: ...
    def timerEvent(self, arg__1: QTimerEvent) -> None: ...
    def timerId(self) -> int: ...
    def timerType(self) -> Qt.TimerType: ...

class QTimerEvent(QEvent):
    @overload
    def __init__(self, arg__1: QTimerEvent) -> None: ...
    @overload
    def __init__(self, timerId: int) -> None: ...
    def clone(self) -> QTimerEvent: ...
    def timerId(self) -> int: ...

class QTranslator(QObject):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def filePath(self) -> str: ...
    def isEmpty(self) -> bool: ...
    def language(self) -> str: ...
    @overload
    def load(self, data: bytes, len: int, directory: str = ...) -> bool: ...
    @overload
    def load(
        self, filename: str, directory: str = ..., search_delimiters: str = ..., suffix: str = ...
    ) -> bool: ...
    @overload
    def load(
        self,
        locale: Union[QLocale, QLocale.Language],
        filename: str,
        prefix: str = ...,
        directory: str = ...,
        suffix: str = ...,
    ) -> bool: ...
    def translate(
        self, context: bytes, sourceText: bytes, disambiguation: Optional[bytes] = ..., n: int = ...
    ) -> str: ...

class QTransposeProxyModel(QAbstractProxyModel):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any: ...
    def index(
        self, row: int, column: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> QModelIndex: ...
    def insertColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def insertRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def itemData(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Dict[int, Any]: ...
    def mapFromSource(
        self, sourceIndex: Union[QModelIndex, QPersistentModelIndex]
    ) -> QModelIndex: ...
    def mapToSource(self, proxyIndex: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def moveColumns(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceColumn: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    def moveRows(
        self,
        sourceParent: Union[QModelIndex, QPersistentModelIndex],
        sourceRow: int,
        count: int,
        destinationParent: Union[QModelIndex, QPersistentModelIndex],
        destinationChild: int,
    ) -> bool: ...
    @overload
    def parent(self) -> QObject: ...
    @overload
    def parent(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QModelIndex: ...
    def removeColumns(
        self, column: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def removeRows(
        self, row: int, count: int, parent: Union[QModelIndex, QPersistentModelIndex] = ...
    ) -> bool: ...
    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int: ...
    def setHeaderData(
        self, section: int, orientation: Qt.Orientation, value: Any, role: int = ...
    ) -> bool: ...
    def setItemData(
        self, index: Union[QModelIndex, QPersistentModelIndex], roles: Dict[int, Any]
    ) -> bool: ...
    def setSourceModel(self, newSourceModel: QAbstractItemModel) -> None: ...
    def sort(self, column: int, order: Qt.SortOrder = ...) -> None: ...
    def span(self, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize: ...

class QUrl(Shiboken.Object):

    PrettyDecoded: QUrl.ComponentFormattingOption = ...  # 0x0
    EncodeSpaces: QUrl.ComponentFormattingOption = ...  # 0x100000
    EncodeUnicode: QUrl.ComponentFormattingOption = ...  # 0x200000
    EncodeDelimiters: QUrl.ComponentFormattingOption = ...  # 0xc00000
    EncodeReserved: QUrl.ComponentFormattingOption = ...  # 0x1000000
    FullyEncoded: QUrl.ComponentFormattingOption = ...  # 0x1f00000
    DecodeReserved: QUrl.ComponentFormattingOption = ...  # 0x2000000
    FullyDecoded: QUrl.ComponentFormattingOption = ...  # 0x7f00000
    TolerantMode: QUrl.ParsingMode = ...  # 0x0
    StrictMode: QUrl.ParsingMode = ...  # 0x1
    DecodedMode: QUrl.ParsingMode = ...  # 0x2
    None_: QUrl.UrlFormattingOption = ...  # 0x0
    RemoveScheme: QUrl.UrlFormattingOption = ...  # 0x1
    RemovePassword: QUrl.UrlFormattingOption = ...  # 0x2
    RemoveUserInfo: QUrl.UrlFormattingOption = ...  # 0x6
    RemovePort: QUrl.UrlFormattingOption = ...  # 0x8
    RemoveAuthority: QUrl.UrlFormattingOption = ...  # 0x1e
    RemovePath: QUrl.UrlFormattingOption = ...  # 0x20
    RemoveQuery: QUrl.UrlFormattingOption = ...  # 0x40
    RemoveFragment: QUrl.UrlFormattingOption = ...  # 0x80
    PreferLocalFile: QUrl.UrlFormattingOption = ...  # 0x200
    StripTrailingSlash: QUrl.UrlFormattingOption = ...  # 0x400
    RemoveFilename: QUrl.UrlFormattingOption = ...  # 0x800
    NormalizePathSegments: QUrl.UrlFormattingOption = ...  # 0x1000
    DefaultResolution: QUrl.UserInputResolutionOption = ...  # 0x0
    AssumeLocalFile: QUrl.UserInputResolutionOption = ...  # 0x1
    class ComponentFormattingOption(Enum):

        PrettyDecoded: QUrl.ComponentFormattingOption = ...  # 0x0
        EncodeSpaces: QUrl.ComponentFormattingOption = ...  # 0x100000
        EncodeUnicode: QUrl.ComponentFormattingOption = ...  # 0x200000
        EncodeDelimiters: QUrl.ComponentFormattingOption = ...  # 0xc00000
        EncodeReserved: QUrl.ComponentFormattingOption = ...  # 0x1000000
        FullyEncoded: QUrl.ComponentFormattingOption = ...  # 0x1f00000
        DecodeReserved: QUrl.ComponentFormattingOption = ...  # 0x2000000
        FullyDecoded: QUrl.ComponentFormattingOption = ...  # 0x7f00000
    class FormattingOptions(object): ...
    class ParsingMode(Enum):

        TolerantMode: QUrl.ParsingMode = ...  # 0x0
        StrictMode: QUrl.ParsingMode = ...  # 0x1
        DecodedMode: QUrl.ParsingMode = ...  # 0x2
    class UrlFormattingOption(Enum):

        None_: QUrl.UrlFormattingOption = ...  # 0x0
        RemoveScheme: QUrl.UrlFormattingOption = ...  # 0x1
        RemovePassword: QUrl.UrlFormattingOption = ...  # 0x2
        RemoveUserInfo: QUrl.UrlFormattingOption = ...  # 0x6
        RemovePort: QUrl.UrlFormattingOption = ...  # 0x8
        RemoveAuthority: QUrl.UrlFormattingOption = ...  # 0x1e
        RemovePath: QUrl.UrlFormattingOption = ...  # 0x20
        RemoveQuery: QUrl.UrlFormattingOption = ...  # 0x40
        RemoveFragment: QUrl.UrlFormattingOption = ...  # 0x80
        PreferLocalFile: QUrl.UrlFormattingOption = ...  # 0x200
        StripTrailingSlash: QUrl.UrlFormattingOption = ...  # 0x400
        RemoveFilename: QUrl.UrlFormattingOption = ...  # 0x800
        NormalizePathSegments: QUrl.UrlFormattingOption = ...  # 0x1000
    class UserInputResolutionOption(Enum):

        DefaultResolution: QUrl.UserInputResolutionOption = ...  # 0x0
        AssumeLocalFile: QUrl.UserInputResolutionOption = ...  # 0x1
    class UserInputResolutionOptions(object): ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, copy: Union[QUrl, str]) -> None: ...
    @overload
    def __init__(self, url: str, mode: QUrl.ParsingMode = ...) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    def adjusted(self, options: QUrl.FormattingOptions) -> QUrl: ...
    def authority(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...
    def clear(self) -> None: ...
    def errorString(self) -> str: ...
    def fileName(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...
    def fragment(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...
    @staticmethod
    def fromAce(arg__1: Union[QByteArray, bytes]) -> str: ...
    @staticmethod
    def fromEncoded(url: Union[QByteArray, bytes], mode: QUrl.ParsingMode = ...) -> QUrl: ...
    @staticmethod
    def fromLocalFile(localfile: Union[str, bytes, os.PathLike]) -> QUrl: ...
    @staticmethod
    def fromPercentEncoding(arg__1: Union[QByteArray, bytes]) -> str: ...
    @staticmethod
    def fromStringList(uris: Sequence[str], mode: QUrl.ParsingMode = ...) -> List[QUrl]: ...
    @staticmethod
    def fromUserInput(
        userInput: str, workingDirectory: str = ..., options: QUrl.UserInputResolutionOptions = ...
    ) -> QUrl: ...
    def hasFragment(self) -> bool: ...
    def hasQuery(self) -> bool: ...
    def host(self, arg__1: QUrl.ComponentFormattingOption = ...) -> str: ...
    @staticmethod
    def idnWhitelist() -> List[str]: ...
    def isEmpty(self) -> bool: ...
    def isLocalFile(self) -> bool: ...
    def isParentOf(self, url: Union[QUrl, str]) -> bool: ...
    def isRelative(self) -> bool: ...
    def isValid(self) -> bool: ...
    def matches(self, url: Union[QUrl, str], options: QUrl.FormattingOptions) -> bool: ...
    def password(self, arg__1: QUrl.ComponentFormattingOption = ...) -> str: ...
    def path(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...
    def port(self, defaultPort: int = ...) -> int: ...
    def query(self, arg__1: QUrl.ComponentFormattingOption = ...) -> str: ...
    def resolved(self, relative: Union[QUrl, str]) -> QUrl: ...
    def scheme(self) -> str: ...
    def setAuthority(self, authority: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setFragment(self, fragment: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setHost(self, host: str, mode: QUrl.ParsingMode = ...) -> None: ...
    @staticmethod
    def setIdnWhitelist(arg__1: Sequence[str]) -> None: ...
    def setPassword(self, password: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setPath(self, path: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setPort(self, port: int) -> None: ...
    @overload
    def setQuery(self, query: QUrlQuery) -> None: ...
    @overload
    def setQuery(self, query: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setScheme(self, scheme: str) -> None: ...
    def setUrl(self, url: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setUserInfo(self, userInfo: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def setUserName(self, userName: str, mode: QUrl.ParsingMode = ...) -> None: ...
    def swap(self, other: Union[QUrl, str]) -> None: ...
    @staticmethod
    def toAce(arg__1: str) -> QByteArray: ...
    def toDisplayString(self, options: QUrl.FormattingOptions = ...) -> str: ...
    def toEncoded(self, options: QUrl.FormattingOptions = ...) -> QByteArray: ...
    def toLocalFile(self) -> str: ...
    @staticmethod
    def toPercentEncoding(
        arg__1: str,
        exclude: Union[QByteArray, bytes] = ...,
        include: Union[QByteArray, bytes] = ...,
    ) -> QByteArray: ...
    def toString(self, options: QUrl.FormattingOptions = ...) -> str: ...
    @staticmethod
    def toStringList(uris: Sequence[QUrl], options: QUrl.FormattingOptions = ...) -> List[str]: ...
    def url(self, options: QUrl.FormattingOptions = ...) -> str: ...
    def userInfo(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...
    def userName(self, options: QUrl.ComponentFormattingOption = ...) -> str: ...

class QUrlQuery(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, other: QUrlQuery) -> None: ...
    @overload
    def __init__(self, queryString: str) -> None: ...
    @overload
    def __init__(self, url: Union[QUrl, str]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def addQueryItem(self, key: str, value: str) -> None: ...
    def allQueryItemValues(
        self, key: str, encoding: QUrl.ComponentFormattingOption = ...
    ) -> List[str]: ...
    def clear(self) -> None: ...
    def hasQueryItem(self, key: str) -> bool: ...
    def isEmpty(self) -> bool: ...
    def query(self, encoding: QUrl.ComponentFormattingOption = ...) -> str: ...
    def queryItemValue(self, key: str, encoding: QUrl.ComponentFormattingOption = ...) -> str: ...
    def queryItems(
        self, encoding: QUrl.ComponentFormattingOption = ...
    ) -> List[Tuple[str, str]]: ...
    def queryPairDelimiter(self) -> str: ...
    def queryValueDelimiter(self) -> str: ...
    def removeAllQueryItems(self, key: str) -> None: ...
    def removeQueryItem(self, key: str) -> None: ...
    def setQuery(self, queryString: str) -> None: ...
    def setQueryDelimiters(self, valueDelimiter: str, pairDelimiter: str) -> None: ...
    def setQueryItems(self, query: Sequence[Tuple[str, str]]) -> None: ...
    def swap(self, other: QUrlQuery) -> None: ...
    def toString(self, encoding: QUrl.ComponentFormattingOption = ...) -> str: ...

class QUuid(Shiboken.Object):

    WithBraces: QUuid.StringFormat = ...  # 0x0
    WithoutBraces: QUuid.StringFormat = ...  # 0x1
    Id128: QUuid.StringFormat = ...  # 0x3
    VarUnknown: QUuid.Variant = ...  # -0x1
    NCS: QUuid.Variant = ...  # 0x0
    DCE: QUuid.Variant = ...  # 0x2
    Microsoft: QUuid.Variant = ...  # 0x6
    Reserved: QUuid.Variant = ...  # 0x7
    VerUnknown: QUuid.Version = ...  # -0x1
    Time: QUuid.Version = ...  # 0x1
    EmbeddedPOSIX: QUuid.Version = ...  # 0x2
    Md5: QUuid.Version = ...  # 0x3
    Name: QUuid.Version = ...  # 0x3
    Random: QUuid.Version = ...  # 0x4
    Sha1: QUuid.Version = ...  # 0x5
    class StringFormat(Enum):

        WithBraces: QUuid.StringFormat = ...  # 0x0
        WithoutBraces: QUuid.StringFormat = ...  # 0x1
        Id128: QUuid.StringFormat = ...  # 0x3
    class Variant(Enum):

        VarUnknown: QUuid.Variant = ...  # -0x1
        NCS: QUuid.Variant = ...  # 0x0
        DCE: QUuid.Variant = ...  # 0x2
        Microsoft: QUuid.Variant = ...  # 0x6
        Reserved: QUuid.Variant = ...  # 0x7
    class Version(Enum):

        VerUnknown: QUuid.Version = ...  # -0x1
        Time: QUuid.Version = ...  # 0x1
        EmbeddedPOSIX: QUuid.Version = ...  # 0x2
        Md5: QUuid.Version = ...  # 0x3
        Name: QUuid.Version = ...  # 0x3
        Random: QUuid.Version = ...  # 0x4
        Sha1: QUuid.Version = ...  # 0x5
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg__1: str) -> None: ...
    @overload
    def __init__(self, arg__1: bytes) -> None: ...
    @overload
    def __init__(self, arg__1: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(
        self,
        l: int,
        w1: int,
        w2: int,
        b1: int,
        b2: int,
        b3: int,
        b4: int,
        b5: int,
        b6: int,
        b7: int,
        b8: int,
    ) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def __reduce__(self) -> object: ...
    def __repr__(self) -> object: ...
    @staticmethod
    def createUuid() -> QUuid: ...
    @overload
    @staticmethod
    def createUuidV3(ns: QUuid, baseData: str) -> QUuid: ...
    @overload
    @staticmethod
    def createUuidV3(ns: QUuid, baseData: Union[QByteArray, bytes]) -> QUuid: ...
    @overload
    @staticmethod
    def createUuidV5(ns: QUuid, baseData: str) -> QUuid: ...
    @overload
    @staticmethod
    def createUuidV5(ns: QUuid, baseData: Union[QByteArray, bytes]) -> QUuid: ...
    @staticmethod
    def fromRfc4122(arg__1: Union[QByteArray, bytes]) -> QUuid: ...
    @staticmethod
    def fromString(string: str) -> QUuid: ...
    def isNull(self) -> bool: ...
    def toByteArray(self, mode: QUuid.StringFormat = ...) -> QByteArray: ...
    def toRfc4122(self) -> QByteArray: ...
    def toString(self, mode: QUuid.StringFormat = ...) -> str: ...
    def variant(self) -> QUuid.Variant: ...
    def version(self) -> QUuid.Version: ...

class QVariantAnimation(QAbstractAnimation):
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def currentValue(self) -> Any: ...
    def duration(self) -> int: ...
    def easingCurve(self) -> QEasingCurve: ...
    def endValue(self) -> Any: ...
    def event(self, event: QEvent) -> bool: ...
    def interpolated(self, from_: Any, to: Any, progress: float) -> Any: ...
    def keyValueAt(self, step: float) -> Any: ...
    def keyValues(self) -> List[Tuple[float, Any]]: ...
    def setDuration(self, msecs: int) -> None: ...
    def setEasingCurve(self, easing: Union[QEasingCurve, QEasingCurve.Type]) -> None: ...
    def setEndValue(self, value: Any) -> None: ...
    def setKeyValueAt(self, step: float, value: Any) -> None: ...
    def setKeyValues(self, values: Sequence[Tuple[float, Any]]) -> None: ...
    def setStartValue(self, value: Any) -> None: ...
    def startValue(self) -> Any: ...
    def updateCurrentTime(self, arg__1: int) -> None: ...
    def updateCurrentValue(self, value: Any) -> None: ...
    def updateState(
        self, newState: QAbstractAnimation.State, oldState: QAbstractAnimation.State
    ) -> None: ...

class QVersionNumber(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, maj: int) -> None: ...
    @overload
    def __init__(self, maj: int, min: int) -> None: ...
    @overload
    def __init__(self, maj: int, min: int, mic: int) -> None: ...
    @overload
    def __init__(self, seg: Sequence[int]) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    @staticmethod
    def commonPrefix(v1: QVersionNumber, v2: QVersionNumber) -> QVersionNumber: ...
    @staticmethod
    def compare(v1: QVersionNumber, v2: QVersionNumber) -> int: ...
    @staticmethod
    def fromString(string: str) -> Tuple[QVersionNumber, int]: ...
    def isNormalized(self) -> bool: ...
    def isNull(self) -> bool: ...
    def isPrefixOf(self, other: QVersionNumber) -> bool: ...
    def majorVersion(self) -> int: ...
    def microVersion(self) -> int: ...
    def minorVersion(self) -> int: ...
    def normalized(self) -> QVersionNumber: ...
    def segmentAt(self, index: int) -> int: ...
    def segmentCount(self) -> int: ...
    def segments(self) -> List[int]: ...
    def toString(self) -> str: ...

class QWaitCondition(Shiboken.Object):
    def __init__(self) -> None: ...
    def notify_all(self) -> None: ...
    def notify_one(self) -> None: ...
    @overload
    def wait(
        self,
        lockedMutex: QMutex,
        deadline: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int] = ...,
    ) -> bool: ...
    @overload
    def wait(self, lockedMutex: QMutex, time: int) -> bool: ...
    @overload
    def wait(
        self,
        lockedReadWriteLock: QReadWriteLock,
        deadline: Union[QDeadlineTimer, QDeadlineTimer.ForeverConstant, Qt.TimerType, int] = ...,
    ) -> bool: ...
    @overload
    def wait(self, lockedReadWriteLock: QReadWriteLock, time: int) -> bool: ...
    def wakeAll(self) -> None: ...
    def wakeOne(self) -> None: ...

class QWinEventNotifier(QObject):
    @overload
    def __init__(self, hEvent: int, parent: Optional[QObject] = ...) -> None: ...
    @overload
    def __init__(self, parent: Optional[QObject] = ...) -> None: ...
    def event(self, e: QEvent) -> bool: ...
    def handle(self) -> int: ...
    def isEnabled(self) -> bool: ...
    def setEnabled(self, enable: bool) -> None: ...
    def setHandle(self, hEvent: int) -> None: ...

class QWriteLocker(Shiboken.Object):
    def __init__(self, readWriteLock: QReadWriteLock) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, arg__1: object, arg__2: object, arg__3: object) -> None: ...
    def readWriteLock(self) -> QReadWriteLock: ...
    def relock(self) -> None: ...
    def unlock(self) -> None: ...

class QXmlStreamAttribute(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QXmlStreamAttribute: QXmlStreamAttribute) -> None: ...
    @overload
    def __init__(self, namespaceUri: str, name: str, value: str) -> None: ...
    @overload
    def __init__(self, qualifiedName: str, value: str) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def isDefault(self) -> bool: ...
    def name(self) -> str: ...
    def namespaceUri(self) -> str: ...
    def prefix(self) -> str: ...
    def qualifiedName(self) -> str: ...
    def value(self) -> str: ...

class QXmlStreamAttributes(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QXmlStreamAttributes: QXmlStreamAttributes) -> None: ...
    def __add__(self, l: Sequence[QXmlStreamAttribute]) -> List[QXmlStreamAttribute]: ...
    @staticmethod
    def __copy__() -> None: ...
    def __lshift__(self, l: Sequence[QXmlStreamAttribute]) -> List[QXmlStreamAttribute]: ...
    @overload
    def append(self, arg__1: QXmlStreamAttribute) -> None: ...
    @overload
    def append(self, l: Sequence[QXmlStreamAttribute]) -> None: ...
    @overload
    def append(self, namespaceUri: str, name: str, value: str) -> None: ...
    @overload
    def append(self, qualifiedName: str, value: str) -> None: ...
    def at(self, i: int) -> QXmlStreamAttribute: ...
    def back(self) -> QXmlStreamAttribute: ...
    def capacity(self) -> int: ...
    def clear(self) -> None: ...
    def constData(self) -> QXmlStreamAttribute: ...
    def constFirst(self) -> QXmlStreamAttribute: ...
    def constLast(self) -> QXmlStreamAttribute: ...
    def count(self) -> int: ...
    def data(self) -> QXmlStreamAttribute: ...
    def empty(self) -> bool: ...
    @overload
    def first(self) -> QXmlStreamAttribute: ...
    @overload
    def first(self, n: int) -> List[QXmlStreamAttribute]: ...
    @staticmethod
    def fromVector(vector: Sequence[QXmlStreamAttribute]) -> List[QXmlStreamAttribute]: ...
    def front(self) -> QXmlStreamAttribute: ...
    @overload
    def hasAttribute(self, namespaceUri: str, name: str) -> bool: ...
    @overload
    def hasAttribute(self, qualifiedName: str) -> bool: ...
    def insert(self, arg__1: int, arg__2: QXmlStreamAttribute) -> None: ...
    def isEmpty(self) -> bool: ...
    def isSharedWith(self, other: Sequence[QXmlStreamAttribute]) -> bool: ...
    @overload
    def last(self) -> QXmlStreamAttribute: ...
    @overload
    def last(self, n: int) -> List[QXmlStreamAttribute]: ...
    def length(self) -> int: ...
    def mid(self, pos: int, len: int = ...) -> List[QXmlStreamAttribute]: ...
    def move(self, from_: int, to: int) -> None: ...
    def prepend(self, arg__1: QXmlStreamAttribute) -> None: ...
    def push_back(self, arg__1: QXmlStreamAttribute) -> None: ...
    def push_front(self, arg__1: QXmlStreamAttribute) -> None: ...
    def remove(self, i: int, n: int = ...) -> None: ...
    def removeAll(self, arg__1: QXmlStreamAttribute) -> None: ...
    def removeAt(self, i: int) -> None: ...
    def removeFirst(self) -> None: ...
    def removeLast(self) -> None: ...
    def removeOne(self, arg__1: QXmlStreamAttribute) -> None: ...
    def reserve(self, size: int) -> None: ...
    def resize(self, size: int) -> None: ...
    def shrink_to_fit(self) -> None: ...
    def size(self) -> int: ...
    @overload
    def sliced(self, pos: int) -> List[QXmlStreamAttribute]: ...
    @overload
    def sliced(self, pos: int, n: int) -> List[QXmlStreamAttribute]: ...
    def squeeze(self) -> None: ...
    def swap(self, other: Sequence[QXmlStreamAttribute]) -> None: ...
    def swapItemsAt(self, i: int, j: int) -> None: ...
    def takeAt(self, i: int) -> QXmlStreamAttribute: ...
    def toVector(self) -> List[QXmlStreamAttribute]: ...
    @overload
    def value(self, namespaceUri: str, name: str) -> str: ...
    @overload
    def value(self, qualifiedName: str) -> str: ...

class QXmlStreamEntityDeclaration(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QXmlStreamEntityDeclaration: QXmlStreamEntityDeclaration) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def name(self) -> str: ...
    def notationName(self) -> str: ...
    def publicId(self) -> str: ...
    def systemId(self) -> str: ...
    def value(self) -> str: ...

class QXmlStreamEntityResolver(Shiboken.Object):
    def __init__(self) -> None: ...
    def resolveEntity(self, publicId: str, systemId: str) -> str: ...
    def resolveUndeclaredEntity(self, name: str) -> str: ...

class QXmlStreamNamespaceDeclaration(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QXmlStreamNamespaceDeclaration: QXmlStreamNamespaceDeclaration) -> None: ...
    @overload
    def __init__(self, prefix: str, namespaceUri: str) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def namespaceUri(self) -> str: ...
    def prefix(self) -> str: ...

class QXmlStreamNotationDeclaration(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, QXmlStreamNotationDeclaration: QXmlStreamNotationDeclaration) -> None: ...
    @staticmethod
    def __copy__() -> None: ...
    def name(self) -> str: ...
    def publicId(self) -> str: ...
    def systemId(self) -> str: ...

class QXmlStreamReader(Shiboken.Object):

    NoError: QXmlStreamReader.Error = ...  # 0x0
    UnexpectedElementError: QXmlStreamReader.Error = ...  # 0x1
    CustomError: QXmlStreamReader.Error = ...  # 0x2
    NotWellFormedError: QXmlStreamReader.Error = ...  # 0x3
    PrematureEndOfDocumentError: QXmlStreamReader.Error = ...  # 0x4
    ErrorOnUnexpectedElement: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x0
    IncludeChildElements: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x1
    SkipChildElements: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x2
    NoToken: QXmlStreamReader.TokenType = ...  # 0x0
    Invalid: QXmlStreamReader.TokenType = ...  # 0x1
    StartDocument: QXmlStreamReader.TokenType = ...  # 0x2
    EndDocument: QXmlStreamReader.TokenType = ...  # 0x3
    StartElement: QXmlStreamReader.TokenType = ...  # 0x4
    EndElement: QXmlStreamReader.TokenType = ...  # 0x5
    Characters: QXmlStreamReader.TokenType = ...  # 0x6
    Comment: QXmlStreamReader.TokenType = ...  # 0x7
    DTD: QXmlStreamReader.TokenType = ...  # 0x8
    EntityReference: QXmlStreamReader.TokenType = ...  # 0x9
    ProcessingInstruction: QXmlStreamReader.TokenType = ...  # 0xa
    class Error(Enum):

        NoError: QXmlStreamReader.Error = ...  # 0x0
        UnexpectedElementError: QXmlStreamReader.Error = ...  # 0x1
        CustomError: QXmlStreamReader.Error = ...  # 0x2
        NotWellFormedError: QXmlStreamReader.Error = ...  # 0x3
        PrematureEndOfDocumentError: QXmlStreamReader.Error = ...  # 0x4
    class ReadElementTextBehaviour(Enum):

        ErrorOnUnexpectedElement: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x0
        IncludeChildElements: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x1
        SkipChildElements: QXmlStreamReader.ReadElementTextBehaviour = ...  # 0x2
    class TokenType(Enum):

        NoToken: QXmlStreamReader.TokenType = ...  # 0x0
        Invalid: QXmlStreamReader.TokenType = ...  # 0x1
        StartDocument: QXmlStreamReader.TokenType = ...  # 0x2
        EndDocument: QXmlStreamReader.TokenType = ...  # 0x3
        StartElement: QXmlStreamReader.TokenType = ...  # 0x4
        EndElement: QXmlStreamReader.TokenType = ...  # 0x5
        Characters: QXmlStreamReader.TokenType = ...  # 0x6
        Comment: QXmlStreamReader.TokenType = ...  # 0x7
        DTD: QXmlStreamReader.TokenType = ...  # 0x8
        EntityReference: QXmlStreamReader.TokenType = ...  # 0x9
        ProcessingInstruction: QXmlStreamReader.TokenType = ...  # 0xa
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, data: str) -> None: ...
    @overload
    def __init__(self, data: bytes) -> None: ...
    @overload
    def __init__(self, data: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, device: QIODevice) -> None: ...
    @overload
    def addData(self, data: str) -> None: ...
    @overload
    def addData(self, data: bytes) -> None: ...
    @overload
    def addData(self, data: Union[QByteArray, bytes]) -> None: ...
    def addExtraNamespaceDeclaration(
        self, extraNamespaceDeclaraction: QXmlStreamNamespaceDeclaration
    ) -> None: ...
    def addExtraNamespaceDeclarations(
        self, extraNamespaceDeclaractions: Sequence[QXmlStreamNamespaceDeclaration]
    ) -> None: ...
    def atEnd(self) -> bool: ...
    def attributes(self) -> QXmlStreamAttributes: ...
    def characterOffset(self) -> int: ...
    def clear(self) -> None: ...
    def columnNumber(self) -> int: ...
    def device(self) -> QIODevice: ...
    def documentEncoding(self) -> str: ...
    def documentVersion(self) -> str: ...
    def dtdName(self) -> str: ...
    def dtdPublicId(self) -> str: ...
    def dtdSystemId(self) -> str: ...
    def entityDeclarations(self) -> List[QXmlStreamEntityDeclaration]: ...
    def entityExpansionLimit(self) -> int: ...
    def entityResolver(self) -> QXmlStreamEntityResolver: ...
    def error(self) -> QXmlStreamReader.Error: ...
    def errorString(self) -> str: ...
    def hasError(self) -> bool: ...
    def isCDATA(self) -> bool: ...
    def isCharacters(self) -> bool: ...
    def isComment(self) -> bool: ...
    def isDTD(self) -> bool: ...
    def isEndDocument(self) -> bool: ...
    def isEndElement(self) -> bool: ...
    def isEntityReference(self) -> bool: ...
    def isProcessingInstruction(self) -> bool: ...
    def isStandaloneDocument(self) -> bool: ...
    def isStartDocument(self) -> bool: ...
    def isStartElement(self) -> bool: ...
    def isWhitespace(self) -> bool: ...
    def lineNumber(self) -> int: ...
    def name(self) -> str: ...
    def namespaceDeclarations(self) -> List[QXmlStreamNamespaceDeclaration]: ...
    def namespaceProcessing(self) -> bool: ...
    def namespaceUri(self) -> str: ...
    def notationDeclarations(self) -> List[QXmlStreamNotationDeclaration]: ...
    def prefix(self) -> str: ...
    def processingInstructionData(self) -> str: ...
    def processingInstructionTarget(self) -> str: ...
    def qualifiedName(self) -> str: ...
    def raiseError(self, message: str = ...) -> None: ...
    def readElementText(
        self, behaviour: QXmlStreamReader.ReadElementTextBehaviour = ...
    ) -> str: ...
    def readNext(self) -> QXmlStreamReader.TokenType: ...
    def readNextStartElement(self) -> bool: ...
    def setDevice(self, device: QIODevice) -> None: ...
    def setEntityExpansionLimit(self, limit: int) -> None: ...
    def setEntityResolver(self, resolver: QXmlStreamEntityResolver) -> None: ...
    def setNamespaceProcessing(self, arg__1: bool) -> None: ...
    def skipCurrentElement(self) -> None: ...
    def text(self) -> str: ...
    def tokenString(self) -> str: ...
    def tokenType(self) -> QXmlStreamReader.TokenType: ...

class QXmlStreamWriter(Shiboken.Object):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, array: Union[QByteArray, bytes]) -> None: ...
    @overload
    def __init__(self, device: QIODevice) -> None: ...
    def autoFormatting(self) -> bool: ...
    def autoFormattingIndent(self) -> int: ...
    def device(self) -> QIODevice: ...
    def hasError(self) -> bool: ...
    def setAutoFormatting(self, arg__1: bool) -> None: ...
    def setAutoFormattingIndent(self, spacesOrTabs: int) -> None: ...
    def setDevice(self, device: QIODevice) -> None: ...
    @overload
    def writeAttribute(self, attribute: QXmlStreamAttribute) -> None: ...
    @overload
    def writeAttribute(self, namespaceUri: str, name: str, value: str) -> None: ...
    @overload
    def writeAttribute(self, qualifiedName: str, value: str) -> None: ...
    def writeAttributes(self, attributes: QXmlStreamAttributes) -> None: ...
    def writeCDATA(self, text: str) -> None: ...
    def writeCharacters(self, text: str) -> None: ...
    def writeComment(self, text: str) -> None: ...
    def writeCurrentToken(self, reader: QXmlStreamReader) -> None: ...
    def writeDTD(self, dtd: str) -> None: ...
    def writeDefaultNamespace(self, namespaceUri: str) -> None: ...
    @overload
    def writeEmptyElement(self, namespaceUri: str, name: str) -> None: ...
    @overload
    def writeEmptyElement(self, qualifiedName: str) -> None: ...
    def writeEndDocument(self) -> None: ...
    def writeEndElement(self) -> None: ...
    def writeEntityReference(self, name: str) -> None: ...
    def writeNamespace(self, namespaceUri: str, prefix: str = ...) -> None: ...
    def writeProcessingInstruction(self, target: str, data: str = ...) -> None: ...
    @overload
    def writeStartDocument(self) -> None: ...
    @overload
    def writeStartDocument(self, version: str) -> None: ...
    @overload
    def writeStartDocument(self, version: str, standalone: bool) -> None: ...
    @overload
    def writeStartElement(self, namespaceUri: str, name: str) -> None: ...
    @overload
    def writeStartElement(self, qualifiedName: str) -> None: ...
    @overload
    def writeTextElement(self, namespaceUri: str, name: str, text: str) -> None: ...
    @overload
    def writeTextElement(self, qualifiedName: str, text: str) -> None: ...

class Qt(Shiboken.Object):

    AlignLeading: Qt.AlignmentFlag = ...  # 0x1
    AlignLeft: Qt.AlignmentFlag = ...  # 0x1
    AlignRight: Qt.AlignmentFlag = ...  # 0x2
    AlignTrailing: Qt.AlignmentFlag = ...  # 0x2
    AlignHCenter: Qt.AlignmentFlag = ...  # 0x4
    AlignJustify: Qt.AlignmentFlag = ...  # 0x8
    AlignAbsolute: Qt.AlignmentFlag = ...  # 0x10
    AlignHorizontal_Mask: Qt.AlignmentFlag = ...  # 0x1f
    AlignTop: Qt.AlignmentFlag = ...  # 0x20
    AlignBottom: Qt.AlignmentFlag = ...  # 0x40
    AlignVCenter: Qt.AlignmentFlag = ...  # 0x80
    AlignCenter: Qt.AlignmentFlag = ...  # 0x84
    AlignBaseline: Qt.AlignmentFlag = ...  # 0x100
    AlignVertical_Mask: Qt.AlignmentFlag = ...  # 0x1e0
    AnchorLeft: Qt.AnchorPoint = ...  # 0x0
    AnchorHorizontalCenter: Qt.AnchorPoint = ...  # 0x1
    AnchorRight: Qt.AnchorPoint = ...  # 0x2
    AnchorTop: Qt.AnchorPoint = ...  # 0x3
    AnchorVerticalCenter: Qt.AnchorPoint = ...  # 0x4
    AnchorBottom: Qt.AnchorPoint = ...  # 0x5
    AA_DontShowIconsInMenus: Qt.ApplicationAttribute = ...  # 0x2
    AA_NativeWindows: Qt.ApplicationAttribute = ...  # 0x3
    AA_DontCreateNativeWidgetSiblings: Qt.ApplicationAttribute = ...  # 0x4
    AA_PluginApplication: Qt.ApplicationAttribute = ...  # 0x5
    AA_DontUseNativeMenuBar: Qt.ApplicationAttribute = ...  # 0x6
    AA_MacDontSwapCtrlAndMeta: Qt.ApplicationAttribute = ...  # 0x7
    AA_Use96Dpi: Qt.ApplicationAttribute = ...  # 0x8
    AA_DisableNativeVirtualKeyboard: Qt.ApplicationAttribute = ...  # 0x9
    AA_SynthesizeTouchForUnhandledMouseEvents: Qt.ApplicationAttribute = ...  # 0xb
    AA_SynthesizeMouseForUnhandledTouchEvents: Qt.ApplicationAttribute = ...  # 0xc
    AA_UseHighDpiPixmaps: Qt.ApplicationAttribute = ...  # 0xd
    AA_ForceRasterWidgets: Qt.ApplicationAttribute = ...  # 0xe
    AA_UseDesktopOpenGL: Qt.ApplicationAttribute = ...  # 0xf
    AA_UseOpenGLES: Qt.ApplicationAttribute = ...  # 0x10
    AA_UseSoftwareOpenGL: Qt.ApplicationAttribute = ...  # 0x11
    AA_ShareOpenGLContexts: Qt.ApplicationAttribute = ...  # 0x12
    AA_SetPalette: Qt.ApplicationAttribute = ...  # 0x13
    AA_EnableHighDpiScaling: Qt.ApplicationAttribute = ...  # 0x14
    AA_DisableHighDpiScaling: Qt.ApplicationAttribute = ...  # 0x15
    AA_UseStyleSheetPropagationInWidgetStyles: Qt.ApplicationAttribute = ...  # 0x16
    AA_DontUseNativeDialogs: Qt.ApplicationAttribute = ...  # 0x17
    AA_SynthesizeMouseForUnhandledTabletEvents: Qt.ApplicationAttribute = ...  # 0x18
    AA_CompressHighFrequencyEvents: Qt.ApplicationAttribute = ...  # 0x19
    AA_DontCheckOpenGLContextThreadAffinity: Qt.ApplicationAttribute = ...  # 0x1a
    AA_DisableShaderDiskCache: Qt.ApplicationAttribute = ...  # 0x1b
    AA_DontShowShortcutsInContextMenus: Qt.ApplicationAttribute = ...  # 0x1c
    AA_CompressTabletEvents: Qt.ApplicationAttribute = ...  # 0x1d
    AA_DisableSessionManager: Qt.ApplicationAttribute = ...  # 0x1f
    AA_AttributeCount: Qt.ApplicationAttribute = ...  # 0x20
    ApplicationSuspended: Qt.ApplicationState = ...  # 0x0
    ApplicationHidden: Qt.ApplicationState = ...  # 0x1
    ApplicationInactive: Qt.ApplicationState = ...  # 0x2
    ApplicationActive: Qt.ApplicationState = ...  # 0x4
    NoArrow: Qt.ArrowType = ...  # 0x0
    UpArrow: Qt.ArrowType = ...  # 0x1
    DownArrow: Qt.ArrowType = ...  # 0x2
    LeftArrow: Qt.ArrowType = ...  # 0x3
    RightArrow: Qt.ArrowType = ...  # 0x4
    IgnoreAspectRatio: Qt.AspectRatioMode = ...  # 0x0
    KeepAspectRatio: Qt.AspectRatioMode = ...  # 0x1
    KeepAspectRatioByExpanding: Qt.AspectRatioMode = ...  # 0x2
    XAxis: Qt.Axis = ...  # 0x0
    YAxis: Qt.Axis = ...  # 0x1
    ZAxis: Qt.Axis = ...  # 0x2
    TransparentMode: Qt.BGMode = ...  # 0x0
    OpaqueMode: Qt.BGMode = ...  # 0x1
    NoBrush: Qt.BrushStyle = ...  # 0x0
    SolidPattern: Qt.BrushStyle = ...  # 0x1
    Dense1Pattern: Qt.BrushStyle = ...  # 0x2
    Dense2Pattern: Qt.BrushStyle = ...  # 0x3
    Dense3Pattern: Qt.BrushStyle = ...  # 0x4
    Dense4Pattern: Qt.BrushStyle = ...  # 0x5
    Dense5Pattern: Qt.BrushStyle = ...  # 0x6
    Dense6Pattern: Qt.BrushStyle = ...  # 0x7
    Dense7Pattern: Qt.BrushStyle = ...  # 0x8
    HorPattern: Qt.BrushStyle = ...  # 0x9
    VerPattern: Qt.BrushStyle = ...  # 0xa
    CrossPattern: Qt.BrushStyle = ...  # 0xb
    BDiagPattern: Qt.BrushStyle = ...  # 0xc
    FDiagPattern: Qt.BrushStyle = ...  # 0xd
    DiagCrossPattern: Qt.BrushStyle = ...  # 0xe
    LinearGradientPattern: Qt.BrushStyle = ...  # 0xf
    RadialGradientPattern: Qt.BrushStyle = ...  # 0x10
    ConicalGradientPattern: Qt.BrushStyle = ...  # 0x11
    TexturePattern: Qt.BrushStyle = ...  # 0x18
    CaseInsensitive: Qt.CaseSensitivity = ...  # 0x0
    CaseSensitive: Qt.CaseSensitivity = ...  # 0x1
    Unchecked: Qt.CheckState = ...  # 0x0
    PartiallyChecked: Qt.CheckState = ...  # 0x1
    Checked: Qt.CheckState = ...  # 0x2
    ChecksumIso3309: Qt.ChecksumType = ...  # 0x0
    ChecksumItuV41: Qt.ChecksumType = ...  # 0x1
    NoClip: Qt.ClipOperation = ...  # 0x0
    ReplaceClip: Qt.ClipOperation = ...  # 0x1
    IntersectClip: Qt.ClipOperation = ...  # 0x2
    AutoConnection: Qt.ConnectionType = ...  # 0x0
    DirectConnection: Qt.ConnectionType = ...  # 0x1
    QueuedConnection: Qt.ConnectionType = ...  # 0x2
    BlockingQueuedConnection: Qt.ConnectionType = ...  # 0x3
    UniqueConnection: Qt.ConnectionType = ...  # 0x80
    SingleShotConnection: Qt.ConnectionType = ...  # 0x100
    NoContextMenu: Qt.ContextMenuPolicy = ...  # 0x0
    DefaultContextMenu: Qt.ContextMenuPolicy = ...  # 0x1
    ActionsContextMenu: Qt.ContextMenuPolicy = ...  # 0x2
    CustomContextMenu: Qt.ContextMenuPolicy = ...  # 0x3
    PreventContextMenu: Qt.ContextMenuPolicy = ...  # 0x4
    DeviceCoordinates: Qt.CoordinateSystem = ...  # 0x0
    LogicalCoordinates: Qt.CoordinateSystem = ...  # 0x1
    TopLeftCorner: Qt.Corner = ...  # 0x0
    TopRightCorner: Qt.Corner = ...  # 0x1
    BottomLeftCorner: Qt.Corner = ...  # 0x2
    BottomRightCorner: Qt.Corner = ...  # 0x3
    LogicalMoveStyle: Qt.CursorMoveStyle = ...  # 0x0
    VisualMoveStyle: Qt.CursorMoveStyle = ...  # 0x1
    ArrowCursor: Qt.CursorShape = ...  # 0x0
    UpArrowCursor: Qt.CursorShape = ...  # 0x1
    CrossCursor: Qt.CursorShape = ...  # 0x2
    WaitCursor: Qt.CursorShape = ...  # 0x3
    IBeamCursor: Qt.CursorShape = ...  # 0x4
    SizeVerCursor: Qt.CursorShape = ...  # 0x5
    SizeHorCursor: Qt.CursorShape = ...  # 0x6
    SizeBDiagCursor: Qt.CursorShape = ...  # 0x7
    SizeFDiagCursor: Qt.CursorShape = ...  # 0x8
    SizeAllCursor: Qt.CursorShape = ...  # 0x9
    BlankCursor: Qt.CursorShape = ...  # 0xa
    SplitVCursor: Qt.CursorShape = ...  # 0xb
    SplitHCursor: Qt.CursorShape = ...  # 0xc
    PointingHandCursor: Qt.CursorShape = ...  # 0xd
    ForbiddenCursor: Qt.CursorShape = ...  # 0xe
    WhatsThisCursor: Qt.CursorShape = ...  # 0xf
    BusyCursor: Qt.CursorShape = ...  # 0x10
    OpenHandCursor: Qt.CursorShape = ...  # 0x11
    ClosedHandCursor: Qt.CursorShape = ...  # 0x12
    DragCopyCursor: Qt.CursorShape = ...  # 0x13
    DragMoveCursor: Qt.CursorShape = ...  # 0x14
    DragLinkCursor: Qt.CursorShape = ...  # 0x15
    LastCursor: Qt.CursorShape = ...  # 0x15
    BitmapCursor: Qt.CursorShape = ...  # 0x18
    CustomCursor: Qt.CursorShape = ...  # 0x19
    TextDate: Qt.DateFormat = ...  # 0x0
    ISODate: Qt.DateFormat = ...  # 0x1
    RFC2822Date: Qt.DateFormat = ...  # 0x8
    ISODateWithMs: Qt.DateFormat = ...  # 0x9
    Monday: Qt.DayOfWeek = ...  # 0x1
    Tuesday: Qt.DayOfWeek = ...  # 0x2
    Wednesday: Qt.DayOfWeek = ...  # 0x3
    Thursday: Qt.DayOfWeek = ...  # 0x4
    Friday: Qt.DayOfWeek = ...  # 0x5
    Saturday: Qt.DayOfWeek = ...  # 0x6
    Sunday: Qt.DayOfWeek = ...  # 0x7
    NoDockWidgetArea: Qt.DockWidgetArea = ...  # 0x0
    LeftDockWidgetArea: Qt.DockWidgetArea = ...  # 0x1
    RightDockWidgetArea: Qt.DockWidgetArea = ...  # 0x2
    TopDockWidgetArea: Qt.DockWidgetArea = ...  # 0x4
    BottomDockWidgetArea: Qt.DockWidgetArea = ...  # 0x8
    AllDockWidgetAreas: Qt.DockWidgetArea = ...  # 0xf
    DockWidgetArea_Mask: Qt.DockWidgetArea = ...  # 0xf
    NDockWidgetAreas: Qt.DockWidgetAreaSizes = ...  # 0x4
    IgnoreAction: Qt.DropAction = ...  # 0x0
    CopyAction: Qt.DropAction = ...  # 0x1
    MoveAction: Qt.DropAction = ...  # 0x2
    LinkAction: Qt.DropAction = ...  # 0x4
    ActionMask: Qt.DropAction = ...  # 0xff
    TargetMoveAction: Qt.DropAction = ...  # 0x8002
    TopEdge: Qt.Edge = ...  # 0x1
    LeftEdge: Qt.Edge = ...  # 0x2
    RightEdge: Qt.Edge = ...  # 0x4
    BottomEdge: Qt.Edge = ...  # 0x8
    EnterKeyDefault: Qt.EnterKeyType = ...  # 0x0
    EnterKeyReturn: Qt.EnterKeyType = ...  # 0x1
    EnterKeyDone: Qt.EnterKeyType = ...  # 0x2
    EnterKeyGo: Qt.EnterKeyType = ...  # 0x3
    EnterKeySend: Qt.EnterKeyType = ...  # 0x4
    EnterKeySearch: Qt.EnterKeyType = ...  # 0x5
    EnterKeyNext: Qt.EnterKeyType = ...  # 0x6
    EnterKeyPrevious: Qt.EnterKeyType = ...  # 0x7
    LowEventPriority: Qt.EventPriority = ...  # -0x1
    NormalEventPriority: Qt.EventPriority = ...  # 0x0
    HighEventPriority: Qt.EventPriority = ...  # 0x1
    OddEvenFill: Qt.FillRule = ...  # 0x0
    WindingFill: Qt.FillRule = ...  # 0x1
    FindDirectChildrenOnly: Qt.FindChildOption = ...  # 0x0
    FindChildrenRecursively: Qt.FindChildOption = ...  # 0x1
    NoFocus: Qt.FocusPolicy = ...  # 0x0
    TabFocus: Qt.FocusPolicy = ...  # 0x1
    ClickFocus: Qt.FocusPolicy = ...  # 0x2
    StrongFocus: Qt.FocusPolicy = ...  # 0xb
    WheelFocus: Qt.FocusPolicy = ...  # 0xf
    MouseFocusReason: Qt.FocusReason = ...  # 0x0
    TabFocusReason: Qt.FocusReason = ...  # 0x1
    BacktabFocusReason: Qt.FocusReason = ...  # 0x2
    ActiveWindowFocusReason: Qt.FocusReason = ...  # 0x3
    PopupFocusReason: Qt.FocusReason = ...  # 0x4
    ShortcutFocusReason: Qt.FocusReason = ...  # 0x5
    MenuBarFocusReason: Qt.FocusReason = ...  # 0x6
    OtherFocusReason: Qt.FocusReason = ...  # 0x7
    NoFocusReason: Qt.FocusReason = ...  # 0x8
    DontStartGestureOnChildren: Qt.GestureFlag = ...  # 0x1
    ReceivePartialGestures: Qt.GestureFlag = ...  # 0x2
    IgnoredGesturesPropagateToParent: Qt.GestureFlag = ...  # 0x4
    NoGesture: Qt.GestureState = ...  # 0x0
    GestureStarted: Qt.GestureState = ...  # 0x1
    GestureUpdated: Qt.GestureState = ...  # 0x2
    GestureFinished: Qt.GestureState = ...  # 0x3
    GestureCanceled: Qt.GestureState = ...  # 0x4
    LastGestureType: Qt.GestureType = ...  # -0x1
    TapGesture: Qt.GestureType = ...  # 0x1
    TapAndHoldGesture: Qt.GestureType = ...  # 0x2
    PanGesture: Qt.GestureType = ...  # 0x3
    PinchGesture: Qt.GestureType = ...  # 0x4
    SwipeGesture: Qt.GestureType = ...  # 0x5
    CustomGesture: Qt.GestureType = ...  # 0x100
    color0: Qt.GlobalColor = ...  # 0x0
    color1: Qt.GlobalColor = ...  # 0x1
    black: Qt.GlobalColor = ...  # 0x2
    white: Qt.GlobalColor = ...  # 0x3
    darkGray: Qt.GlobalColor = ...  # 0x4
    gray: Qt.GlobalColor = ...  # 0x5
    lightGray: Qt.GlobalColor = ...  # 0x6
    red: Qt.GlobalColor = ...  # 0x7
    green: Qt.GlobalColor = ...  # 0x8
    blue: Qt.GlobalColor = ...  # 0x9
    cyan: Qt.GlobalColor = ...  # 0xa
    magenta: Qt.GlobalColor = ...  # 0xb
    yellow: Qt.GlobalColor = ...  # 0xc
    darkRed: Qt.GlobalColor = ...  # 0xd
    darkGreen: Qt.GlobalColor = ...  # 0xe
    darkBlue: Qt.GlobalColor = ...  # 0xf
    darkCyan: Qt.GlobalColor = ...  # 0x10
    darkMagenta: Qt.GlobalColor = ...  # 0x11
    darkYellow: Qt.GlobalColor = ...  # 0x12
    transparent: Qt.GlobalColor = ...  # 0x13
    ExactHit: Qt.HitTestAccuracy = ...  # 0x0
    FuzzyHit: Qt.HitTestAccuracy = ...  # 0x1
    AutoColor: Qt.ImageConversionFlag = ...  # 0x0
    AutoDither: Qt.ImageConversionFlag = ...  # 0x0
    DiffuseDither: Qt.ImageConversionFlag = ...  # 0x0
    ThresholdAlphaDither: Qt.ImageConversionFlag = ...  # 0x0
    MonoOnly: Qt.ImageConversionFlag = ...  # 0x2
    ColorMode_Mask: Qt.ImageConversionFlag = ...  # 0x3
    ColorOnly: Qt.ImageConversionFlag = ...  # 0x3
    OrderedAlphaDither: Qt.ImageConversionFlag = ...  # 0x4
    DiffuseAlphaDither: Qt.ImageConversionFlag = ...  # 0x8
    AlphaDither_Mask: Qt.ImageConversionFlag = ...  # 0xc
    NoAlpha: Qt.ImageConversionFlag = ...  # 0xc
    OrderedDither: Qt.ImageConversionFlag = ...  # 0x10
    ThresholdDither: Qt.ImageConversionFlag = ...  # 0x20
    Dither_Mask: Qt.ImageConversionFlag = ...  # 0x30
    PreferDither: Qt.ImageConversionFlag = ...  # 0x40
    AvoidDither: Qt.ImageConversionFlag = ...  # 0x80
    DitherMode_Mask: Qt.ImageConversionFlag = ...  # 0xc0
    NoOpaqueDetection: Qt.ImageConversionFlag = ...  # 0x100
    NoFormatConversion: Qt.ImageConversionFlag = ...  # 0x200
    ImhExclusiveInputMask: Qt.InputMethodHint = ...  # -0x10000
    ImhNone: Qt.InputMethodHint = ...  # 0x0
    ImhHiddenText: Qt.InputMethodHint = ...  # 0x1
    ImhSensitiveData: Qt.InputMethodHint = ...  # 0x2
    ImhNoAutoUppercase: Qt.InputMethodHint = ...  # 0x4
    ImhPreferNumbers: Qt.InputMethodHint = ...  # 0x8
    ImhPreferUppercase: Qt.InputMethodHint = ...  # 0x10
    ImhPreferLowercase: Qt.InputMethodHint = ...  # 0x20
    ImhNoPredictiveText: Qt.InputMethodHint = ...  # 0x40
    ImhDate: Qt.InputMethodHint = ...  # 0x80
    ImhTime: Qt.InputMethodHint = ...  # 0x100
    ImhPreferLatin: Qt.InputMethodHint = ...  # 0x200
    ImhMultiLine: Qt.InputMethodHint = ...  # 0x400
    ImhNoEditMenu: Qt.InputMethodHint = ...  # 0x800
    ImhNoTextHandles: Qt.InputMethodHint = ...  # 0x1000
    ImhDigitsOnly: Qt.InputMethodHint = ...  # 0x10000
    ImhFormattedNumbersOnly: Qt.InputMethodHint = ...  # 0x20000
    ImhUppercaseOnly: Qt.InputMethodHint = ...  # 0x40000
    ImhLowercaseOnly: Qt.InputMethodHint = ...  # 0x80000
    ImhDialableCharactersOnly: Qt.InputMethodHint = ...  # 0x100000
    ImhEmailCharactersOnly: Qt.InputMethodHint = ...  # 0x200000
    ImhUrlCharactersOnly: Qt.InputMethodHint = ...  # 0x400000
    ImhLatinOnly: Qt.InputMethodHint = ...  # 0x800000
    ImPlatformData: Qt.InputMethodQuery = ...  # -0x80000000
    ImQueryAll: Qt.InputMethodQuery = ...  # -0x1
    ImEnabled: Qt.InputMethodQuery = ...  # 0x1
    ImCursorRectangle: Qt.InputMethodQuery = ...  # 0x2
    ImFont: Qt.InputMethodQuery = ...  # 0x4
    ImCursorPosition: Qt.InputMethodQuery = ...  # 0x8
    ImSurroundingText: Qt.InputMethodQuery = ...  # 0x10
    ImCurrentSelection: Qt.InputMethodQuery = ...  # 0x20
    ImMaximumTextLength: Qt.InputMethodQuery = ...  # 0x40
    ImAnchorPosition: Qt.InputMethodQuery = ...  # 0x80
    ImHints: Qt.InputMethodQuery = ...  # 0x100
    ImPreferredLanguage: Qt.InputMethodQuery = ...  # 0x200
    ImAbsolutePosition: Qt.InputMethodQuery = ...  # 0x400
    ImTextBeforeCursor: Qt.InputMethodQuery = ...  # 0x800
    ImTextAfterCursor: Qt.InputMethodQuery = ...  # 0x1000
    ImEnterKeyType: Qt.InputMethodQuery = ...  # 0x2000
    ImAnchorRectangle: Qt.InputMethodQuery = ...  # 0x4000
    ImQueryInput: Qt.InputMethodQuery = ...  # 0x40ba
    ImInputItemClipRectangle: Qt.InputMethodQuery = ...  # 0x8000
    ImReadOnly: Qt.InputMethodQuery = ...  # 0x10000
    DisplayRole: Qt.ItemDataRole = ...  # 0x0
    DecorationRole: Qt.ItemDataRole = ...  # 0x1
    EditRole: Qt.ItemDataRole = ...  # 0x2
    ToolTipRole: Qt.ItemDataRole = ...  # 0x3
    StatusTipRole: Qt.ItemDataRole = ...  # 0x4
    WhatsThisRole: Qt.ItemDataRole = ...  # 0x5
    FontRole: Qt.ItemDataRole = ...  # 0x6
    TextAlignmentRole: Qt.ItemDataRole = ...  # 0x7
    BackgroundRole: Qt.ItemDataRole = ...  # 0x8
    ForegroundRole: Qt.ItemDataRole = ...  # 0x9
    CheckStateRole: Qt.ItemDataRole = ...  # 0xa
    AccessibleTextRole: Qt.ItemDataRole = ...  # 0xb
    AccessibleDescriptionRole: Qt.ItemDataRole = ...  # 0xc
    SizeHintRole: Qt.ItemDataRole = ...  # 0xd
    InitialSortOrderRole: Qt.ItemDataRole = ...  # 0xe
    DisplayPropertyRole: Qt.ItemDataRole = ...  # 0x1b
    DecorationPropertyRole: Qt.ItemDataRole = ...  # 0x1c
    ToolTipPropertyRole: Qt.ItemDataRole = ...  # 0x1d
    StatusTipPropertyRole: Qt.ItemDataRole = ...  # 0x1e
    WhatsThisPropertyRole: Qt.ItemDataRole = ...  # 0x1f
    UserRole: Qt.ItemDataRole = ...  # 0x100
    NoItemFlags: Qt.ItemFlag = ...  # 0x0
    ItemIsSelectable: Qt.ItemFlag = ...  # 0x1
    ItemIsEditable: Qt.ItemFlag = ...  # 0x2
    ItemIsDragEnabled: Qt.ItemFlag = ...  # 0x4
    ItemIsDropEnabled: Qt.ItemFlag = ...  # 0x8
    ItemIsUserCheckable: Qt.ItemFlag = ...  # 0x10
    ItemIsEnabled: Qt.ItemFlag = ...  # 0x20
    ItemIsAutoTristate: Qt.ItemFlag = ...  # 0x40
    ItemNeverHasChildren: Qt.ItemFlag = ...  # 0x80
    ItemIsUserTristate: Qt.ItemFlag = ...  # 0x100
    ContainsItemShape: Qt.ItemSelectionMode = ...  # 0x0
    IntersectsItemShape: Qt.ItemSelectionMode = ...  # 0x1
    ContainsItemBoundingRect: Qt.ItemSelectionMode = ...  # 0x2
    IntersectsItemBoundingRect: Qt.ItemSelectionMode = ...  # 0x3
    ReplaceSelection: Qt.ItemSelectionOperation = ...  # 0x0
    AddToSelection: Qt.ItemSelectionOperation = ...  # 0x1
    Key_Any: Qt.Key = ...  # 0x20
    Key_Space: Qt.Key = ...  # 0x20
    Key_Exclam: Qt.Key = ...  # 0x21
    Key_QuoteDbl: Qt.Key = ...  # 0x22
    Key_NumberSign: Qt.Key = ...  # 0x23
    Key_Dollar: Qt.Key = ...  # 0x24
    Key_Percent: Qt.Key = ...  # 0x25
    Key_Ampersand: Qt.Key = ...  # 0x26
    Key_Apostrophe: Qt.Key = ...  # 0x27
    Key_ParenLeft: Qt.Key = ...  # 0x28
    Key_ParenRight: Qt.Key = ...  # 0x29
    Key_Asterisk: Qt.Key = ...  # 0x2a
    Key_Plus: Qt.Key = ...  # 0x2b
    Key_Comma: Qt.Key = ...  # 0x2c
    Key_Minus: Qt.Key = ...  # 0x2d
    Key_Period: Qt.Key = ...  # 0x2e
    Key_Slash: Qt.Key = ...  # 0x2f
    Key_0: Qt.Key = ...  # 0x30
    Key_1: Qt.Key = ...  # 0x31
    Key_2: Qt.Key = ...  # 0x32
    Key_3: Qt.Key = ...  # 0x33
    Key_4: Qt.Key = ...  # 0x34
    Key_5: Qt.Key = ...  # 0x35
    Key_6: Qt.Key = ...  # 0x36
    Key_7: Qt.Key = ...  # 0x37
    Key_8: Qt.Key = ...  # 0x38
    Key_9: Qt.Key = ...  # 0x39
    Key_Colon: Qt.Key = ...  # 0x3a
    Key_Semicolon: Qt.Key = ...  # 0x3b
    Key_Less: Qt.Key = ...  # 0x3c
    Key_Equal: Qt.Key = ...  # 0x3d
    Key_Greater: Qt.Key = ...  # 0x3e
    Key_Question: Qt.Key = ...  # 0x3f
    Key_At: Qt.Key = ...  # 0x40
    Key_A: Qt.Key = ...  # 0x41
    Key_B: Qt.Key = ...  # 0x42
    Key_C: Qt.Key = ...  # 0x43
    Key_D: Qt.Key = ...  # 0x44
    Key_E: Qt.Key = ...  # 0x45
    Key_F: Qt.Key = ...  # 0x46
    Key_G: Qt.Key = ...  # 0x47
    Key_H: Qt.Key = ...  # 0x48
    Key_I: Qt.Key = ...  # 0x49
    Key_J: Qt.Key = ...  # 0x4a
    Key_K: Qt.Key = ...  # 0x4b
    Key_L: Qt.Key = ...  # 0x4c
    Key_M: Qt.Key = ...  # 0x4d
    Key_N: Qt.Key = ...  # 0x4e
    Key_O: Qt.Key = ...  # 0x4f
    Key_P: Qt.Key = ...  # 0x50
    Key_Q: Qt.Key = ...  # 0x51
    Key_R: Qt.Key = ...  # 0x52
    Key_S: Qt.Key = ...  # 0x53
    Key_T: Qt.Key = ...  # 0x54
    Key_U: Qt.Key = ...  # 0x55
    Key_V: Qt.Key = ...  # 0x56
    Key_W: Qt.Key = ...  # 0x57
    Key_X: Qt.Key = ...  # 0x58
    Key_Y: Qt.Key = ...  # 0x59
    Key_Z: Qt.Key = ...  # 0x5a
    Key_BracketLeft: Qt.Key = ...  # 0x5b
    Key_Backslash: Qt.Key = ...  # 0x5c
    Key_BracketRight: Qt.Key = ...  # 0x5d
    Key_AsciiCircum: Qt.Key = ...  # 0x5e
    Key_Underscore: Qt.Key = ...  # 0x5f
    Key_QuoteLeft: Qt.Key = ...  # 0x60
    Key_BraceLeft: Qt.Key = ...  # 0x7b
    Key_Bar: Qt.Key = ...  # 0x7c
    Key_BraceRight: Qt.Key = ...  # 0x7d
    Key_AsciiTilde: Qt.Key = ...  # 0x7e
    Key_nobreakspace: Qt.Key = ...  # 0xa0
    Key_exclamdown: Qt.Key = ...  # 0xa1
    Key_cent: Qt.Key = ...  # 0xa2
    Key_sterling: Qt.Key = ...  # 0xa3
    Key_currency: Qt.Key = ...  # 0xa4
    Key_yen: Qt.Key = ...  # 0xa5
    Key_brokenbar: Qt.Key = ...  # 0xa6
    Key_section: Qt.Key = ...  # 0xa7
    Key_diaeresis: Qt.Key = ...  # 0xa8
    Key_copyright: Qt.Key = ...  # 0xa9
    Key_ordfeminine: Qt.Key = ...  # 0xaa
    Key_guillemotleft: Qt.Key = ...  # 0xab
    Key_notsign: Qt.Key = ...  # 0xac
    Key_hyphen: Qt.Key = ...  # 0xad
    Key_registered: Qt.Key = ...  # 0xae
    Key_macron: Qt.Key = ...  # 0xaf
    Key_degree: Qt.Key = ...  # 0xb0
    Key_plusminus: Qt.Key = ...  # 0xb1
    Key_twosuperior: Qt.Key = ...  # 0xb2
    Key_threesuperior: Qt.Key = ...  # 0xb3
    Key_acute: Qt.Key = ...  # 0xb4
    Key_mu: Qt.Key = ...  # 0xb5
    Key_paragraph: Qt.Key = ...  # 0xb6
    Key_periodcentered: Qt.Key = ...  # 0xb7
    Key_cedilla: Qt.Key = ...  # 0xb8
    Key_onesuperior: Qt.Key = ...  # 0xb9
    Key_masculine: Qt.Key = ...  # 0xba
    Key_guillemotright: Qt.Key = ...  # 0xbb
    Key_onequarter: Qt.Key = ...  # 0xbc
    Key_onehalf: Qt.Key = ...  # 0xbd
    Key_threequarters: Qt.Key = ...  # 0xbe
    Key_questiondown: Qt.Key = ...  # 0xbf
    Key_Agrave: Qt.Key = ...  # 0xc0
    Key_Aacute: Qt.Key = ...  # 0xc1
    Key_Acircumflex: Qt.Key = ...  # 0xc2
    Key_Atilde: Qt.Key = ...  # 0xc3
    Key_Adiaeresis: Qt.Key = ...  # 0xc4
    Key_Aring: Qt.Key = ...  # 0xc5
    Key_AE: Qt.Key = ...  # 0xc6
    Key_Ccedilla: Qt.Key = ...  # 0xc7
    Key_Egrave: Qt.Key = ...  # 0xc8
    Key_Eacute: Qt.Key = ...  # 0xc9
    Key_Ecircumflex: Qt.Key = ...  # 0xca
    Key_Ediaeresis: Qt.Key = ...  # 0xcb
    Key_Igrave: Qt.Key = ...  # 0xcc
    Key_Iacute: Qt.Key = ...  # 0xcd
    Key_Icircumflex: Qt.Key = ...  # 0xce
    Key_Idiaeresis: Qt.Key = ...  # 0xcf
    Key_ETH: Qt.Key = ...  # 0xd0
    Key_Ntilde: Qt.Key = ...  # 0xd1
    Key_Ograve: Qt.Key = ...  # 0xd2
    Key_Oacute: Qt.Key = ...  # 0xd3
    Key_Ocircumflex: Qt.Key = ...  # 0xd4
    Key_Otilde: Qt.Key = ...  # 0xd5
    Key_Odiaeresis: Qt.Key = ...  # 0xd6
    Key_multiply: Qt.Key = ...  # 0xd7
    Key_Ooblique: Qt.Key = ...  # 0xd8
    Key_Ugrave: Qt.Key = ...  # 0xd9
    Key_Uacute: Qt.Key = ...  # 0xda
    Key_Ucircumflex: Qt.Key = ...  # 0xdb
    Key_Udiaeresis: Qt.Key = ...  # 0xdc
    Key_Yacute: Qt.Key = ...  # 0xdd
    Key_THORN: Qt.Key = ...  # 0xde
    Key_ssharp: Qt.Key = ...  # 0xdf
    Key_division: Qt.Key = ...  # 0xf7
    Key_ydiaeresis: Qt.Key = ...  # 0xff
    Key_Escape: Qt.Key = ...  # 0x1000000
    Key_Tab: Qt.Key = ...  # 0x1000001
    Key_Backtab: Qt.Key = ...  # 0x1000002
    Key_Backspace: Qt.Key = ...  # 0x1000003
    Key_Return: Qt.Key = ...  # 0x1000004
    Key_Enter: Qt.Key = ...  # 0x1000005
    Key_Insert: Qt.Key = ...  # 0x1000006
    Key_Delete: Qt.Key = ...  # 0x1000007
    Key_Pause: Qt.Key = ...  # 0x1000008
    Key_Print: Qt.Key = ...  # 0x1000009
    Key_SysReq: Qt.Key = ...  # 0x100000a
    Key_Clear: Qt.Key = ...  # 0x100000b
    Key_Home: Qt.Key = ...  # 0x1000010
    Key_End: Qt.Key = ...  # 0x1000011
    Key_Left: Qt.Key = ...  # 0x1000012
    Key_Up: Qt.Key = ...  # 0x1000013
    Key_Right: Qt.Key = ...  # 0x1000014
    Key_Down: Qt.Key = ...  # 0x1000015
    Key_PageUp: Qt.Key = ...  # 0x1000016
    Key_PageDown: Qt.Key = ...  # 0x1000017
    Key_Shift: Qt.Key = ...  # 0x1000020
    Key_Control: Qt.Key = ...  # 0x1000021
    Key_Meta: Qt.Key = ...  # 0x1000022
    Key_Alt: Qt.Key = ...  # 0x1000023
    Key_CapsLock: Qt.Key = ...  # 0x1000024
    Key_NumLock: Qt.Key = ...  # 0x1000025
    Key_ScrollLock: Qt.Key = ...  # 0x1000026
    Key_F1: Qt.Key = ...  # 0x1000030
    Key_F2: Qt.Key = ...  # 0x1000031
    Key_F3: Qt.Key = ...  # 0x1000032
    Key_F4: Qt.Key = ...  # 0x1000033
    Key_F5: Qt.Key = ...  # 0x1000034
    Key_F6: Qt.Key = ...  # 0x1000035
    Key_F7: Qt.Key = ...  # 0x1000036
    Key_F8: Qt.Key = ...  # 0x1000037
    Key_F9: Qt.Key = ...  # 0x1000038
    Key_F10: Qt.Key = ...  # 0x1000039
    Key_F11: Qt.Key = ...  # 0x100003a
    Key_F12: Qt.Key = ...  # 0x100003b
    Key_F13: Qt.Key = ...  # 0x100003c
    Key_F14: Qt.Key = ...  # 0x100003d
    Key_F15: Qt.Key = ...  # 0x100003e
    Key_F16: Qt.Key = ...  # 0x100003f
    Key_F17: Qt.Key = ...  # 0x1000040
    Key_F18: Qt.Key = ...  # 0x1000041
    Key_F19: Qt.Key = ...  # 0x1000042
    Key_F20: Qt.Key = ...  # 0x1000043
    Key_F21: Qt.Key = ...  # 0x1000044
    Key_F22: Qt.Key = ...  # 0x1000045
    Key_F23: Qt.Key = ...  # 0x1000046
    Key_F24: Qt.Key = ...  # 0x1000047
    Key_F25: Qt.Key = ...  # 0x1000048
    Key_F26: Qt.Key = ...  # 0x1000049
    Key_F27: Qt.Key = ...  # 0x100004a
    Key_F28: Qt.Key = ...  # 0x100004b
    Key_F29: Qt.Key = ...  # 0x100004c
    Key_F30: Qt.Key = ...  # 0x100004d
    Key_F31: Qt.Key = ...  # 0x100004e
    Key_F32: Qt.Key = ...  # 0x100004f
    Key_F33: Qt.Key = ...  # 0x1000050
    Key_F34: Qt.Key = ...  # 0x1000051
    Key_F35: Qt.Key = ...  # 0x1000052
    Key_Super_L: Qt.Key = ...  # 0x1000053
    Key_Super_R: Qt.Key = ...  # 0x1000054
    Key_Menu: Qt.Key = ...  # 0x1000055
    Key_Hyper_L: Qt.Key = ...  # 0x1000056
    Key_Hyper_R: Qt.Key = ...  # 0x1000057
    Key_Help: Qt.Key = ...  # 0x1000058
    Key_Direction_L: Qt.Key = ...  # 0x1000059
    Key_Direction_R: Qt.Key = ...  # 0x1000060
    Key_Back: Qt.Key = ...  # 0x1000061
    Key_Forward: Qt.Key = ...  # 0x1000062
    Key_Stop: Qt.Key = ...  # 0x1000063
    Key_Refresh: Qt.Key = ...  # 0x1000064
    Key_VolumeDown: Qt.Key = ...  # 0x1000070
    Key_VolumeMute: Qt.Key = ...  # 0x1000071
    Key_VolumeUp: Qt.Key = ...  # 0x1000072
    Key_BassBoost: Qt.Key = ...  # 0x1000073
    Key_BassUp: Qt.Key = ...  # 0x1000074
    Key_BassDown: Qt.Key = ...  # 0x1000075
    Key_TrebleUp: Qt.Key = ...  # 0x1000076
    Key_TrebleDown: Qt.Key = ...  # 0x1000077
    Key_MediaPlay: Qt.Key = ...  # 0x1000080
    Key_MediaStop: Qt.Key = ...  # 0x1000081
    Key_MediaPrevious: Qt.Key = ...  # 0x1000082
    Key_MediaNext: Qt.Key = ...  # 0x1000083
    Key_MediaRecord: Qt.Key = ...  # 0x1000084
    Key_MediaPause: Qt.Key = ...  # 0x1000085
    Key_MediaTogglePlayPause: Qt.Key = ...  # 0x1000086
    Key_HomePage: Qt.Key = ...  # 0x1000090
    Key_Favorites: Qt.Key = ...  # 0x1000091
    Key_Search: Qt.Key = ...  # 0x1000092
    Key_Standby: Qt.Key = ...  # 0x1000093
    Key_OpenUrl: Qt.Key = ...  # 0x1000094
    Key_LaunchMail: Qt.Key = ...  # 0x10000a0
    Key_LaunchMedia: Qt.Key = ...  # 0x10000a1
    Key_Launch0: Qt.Key = ...  # 0x10000a2
    Key_Launch1: Qt.Key = ...  # 0x10000a3
    Key_Launch2: Qt.Key = ...  # 0x10000a4
    Key_Launch3: Qt.Key = ...  # 0x10000a5
    Key_Launch4: Qt.Key = ...  # 0x10000a6
    Key_Launch5: Qt.Key = ...  # 0x10000a7
    Key_Launch6: Qt.Key = ...  # 0x10000a8
    Key_Launch7: Qt.Key = ...  # 0x10000a9
    Key_Launch8: Qt.Key = ...  # 0x10000aa
    Key_Launch9: Qt.Key = ...  # 0x10000ab
    Key_LaunchA: Qt.Key = ...  # 0x10000ac
    Key_LaunchB: Qt.Key = ...  # 0x10000ad
    Key_LaunchC: Qt.Key = ...  # 0x10000ae
    Key_LaunchD: Qt.Key = ...  # 0x10000af
    Key_LaunchE: Qt.Key = ...  # 0x10000b0
    Key_LaunchF: Qt.Key = ...  # 0x10000b1
    Key_MonBrightnessUp: Qt.Key = ...  # 0x10000b2
    Key_MonBrightnessDown: Qt.Key = ...  # 0x10000b3
    Key_KeyboardLightOnOff: Qt.Key = ...  # 0x10000b4
    Key_KeyboardBrightnessUp: Qt.Key = ...  # 0x10000b5
    Key_KeyboardBrightnessDown: Qt.Key = ...  # 0x10000b6
    Key_PowerOff: Qt.Key = ...  # 0x10000b7
    Key_WakeUp: Qt.Key = ...  # 0x10000b8
    Key_Eject: Qt.Key = ...  # 0x10000b9
    Key_ScreenSaver: Qt.Key = ...  # 0x10000ba
    Key_WWW: Qt.Key = ...  # 0x10000bb
    Key_Memo: Qt.Key = ...  # 0x10000bc
    Key_LightBulb: Qt.Key = ...  # 0x10000bd
    Key_Shop: Qt.Key = ...  # 0x10000be
    Key_History: Qt.Key = ...  # 0x10000bf
    Key_AddFavorite: Qt.Key = ...  # 0x10000c0
    Key_HotLinks: Qt.Key = ...  # 0x10000c1
    Key_BrightnessAdjust: Qt.Key = ...  # 0x10000c2
    Key_Finance: Qt.Key = ...  # 0x10000c3
    Key_Community: Qt.Key = ...  # 0x10000c4
    Key_AudioRewind: Qt.Key = ...  # 0x10000c5
    Key_BackForward: Qt.Key = ...  # 0x10000c6
    Key_ApplicationLeft: Qt.Key = ...  # 0x10000c7
    Key_ApplicationRight: Qt.Key = ...  # 0x10000c8
    Key_Book: Qt.Key = ...  # 0x10000c9
    Key_CD: Qt.Key = ...  # 0x10000ca
    Key_Calculator: Qt.Key = ...  # 0x10000cb
    Key_ToDoList: Qt.Key = ...  # 0x10000cc
    Key_ClearGrab: Qt.Key = ...  # 0x10000cd
    Key_Close: Qt.Key = ...  # 0x10000ce
    Key_Copy: Qt.Key = ...  # 0x10000cf
    Key_Cut: Qt.Key = ...  # 0x10000d0
    Key_Display: Qt.Key = ...  # 0x10000d1
    Key_DOS: Qt.Key = ...  # 0x10000d2
    Key_Documents: Qt.Key = ...  # 0x10000d3
    Key_Excel: Qt.Key = ...  # 0x10000d4
    Key_Explorer: Qt.Key = ...  # 0x10000d5
    Key_Game: Qt.Key = ...  # 0x10000d6
    Key_Go: Qt.Key = ...  # 0x10000d7
    Key_iTouch: Qt.Key = ...  # 0x10000d8
    Key_LogOff: Qt.Key = ...  # 0x10000d9
    Key_Market: Qt.Key = ...  # 0x10000da
    Key_Meeting: Qt.Key = ...  # 0x10000db
    Key_MenuKB: Qt.Key = ...  # 0x10000dc
    Key_MenuPB: Qt.Key = ...  # 0x10000dd
    Key_MySites: Qt.Key = ...  # 0x10000de
    Key_News: Qt.Key = ...  # 0x10000df
    Key_OfficeHome: Qt.Key = ...  # 0x10000e0
    Key_Option: Qt.Key = ...  # 0x10000e1
    Key_Paste: Qt.Key = ...  # 0x10000e2
    Key_Phone: Qt.Key = ...  # 0x10000e3
    Key_Calendar: Qt.Key = ...  # 0x10000e4
    Key_Reply: Qt.Key = ...  # 0x10000e5
    Key_Reload: Qt.Key = ...  # 0x10000e6
    Key_RotateWindows: Qt.Key = ...  # 0x10000e7
    Key_RotationPB: Qt.Key = ...  # 0x10000e8
    Key_RotationKB: Qt.Key = ...  # 0x10000e9
    Key_Save: Qt.Key = ...  # 0x10000ea
    Key_Send: Qt.Key = ...  # 0x10000eb
    Key_Spell: Qt.Key = ...  # 0x10000ec
    Key_SplitScreen: Qt.Key = ...  # 0x10000ed
    Key_Support: Qt.Key = ...  # 0x10000ee
    Key_TaskPane: Qt.Key = ...  # 0x10000ef
    Key_Terminal: Qt.Key = ...  # 0x10000f0
    Key_Tools: Qt.Key = ...  # 0x10000f1
    Key_Travel: Qt.Key = ...  # 0x10000f2
    Key_Video: Qt.Key = ...  # 0x10000f3
    Key_Word: Qt.Key = ...  # 0x10000f4
    Key_Xfer: Qt.Key = ...  # 0x10000f5
    Key_ZoomIn: Qt.Key = ...  # 0x10000f6
    Key_ZoomOut: Qt.Key = ...  # 0x10000f7
    Key_Away: Qt.Key = ...  # 0x10000f8
    Key_Messenger: Qt.Key = ...  # 0x10000f9
    Key_WebCam: Qt.Key = ...  # 0x10000fa
    Key_MailForward: Qt.Key = ...  # 0x10000fb
    Key_Pictures: Qt.Key = ...  # 0x10000fc
    Key_Music: Qt.Key = ...  # 0x10000fd
    Key_Battery: Qt.Key = ...  # 0x10000fe
    Key_Bluetooth: Qt.Key = ...  # 0x10000ff
    Key_WLAN: Qt.Key = ...  # 0x1000100
    Key_UWB: Qt.Key = ...  # 0x1000101
    Key_AudioForward: Qt.Key = ...  # 0x1000102
    Key_AudioRepeat: Qt.Key = ...  # 0x1000103
    Key_AudioRandomPlay: Qt.Key = ...  # 0x1000104
    Key_Subtitle: Qt.Key = ...  # 0x1000105
    Key_AudioCycleTrack: Qt.Key = ...  # 0x1000106
    Key_Time: Qt.Key = ...  # 0x1000107
    Key_Hibernate: Qt.Key = ...  # 0x1000108
    Key_View: Qt.Key = ...  # 0x1000109
    Key_TopMenu: Qt.Key = ...  # 0x100010a
    Key_PowerDown: Qt.Key = ...  # 0x100010b
    Key_Suspend: Qt.Key = ...  # 0x100010c
    Key_ContrastAdjust: Qt.Key = ...  # 0x100010d
    Key_LaunchG: Qt.Key = ...  # 0x100010e
    Key_LaunchH: Qt.Key = ...  # 0x100010f
    Key_TouchpadToggle: Qt.Key = ...  # 0x1000110
    Key_TouchpadOn: Qt.Key = ...  # 0x1000111
    Key_TouchpadOff: Qt.Key = ...  # 0x1000112
    Key_MicMute: Qt.Key = ...  # 0x1000113
    Key_Red: Qt.Key = ...  # 0x1000114
    Key_Green: Qt.Key = ...  # 0x1000115
    Key_Yellow: Qt.Key = ...  # 0x1000116
    Key_Blue: Qt.Key = ...  # 0x1000117
    Key_ChannelUp: Qt.Key = ...  # 0x1000118
    Key_ChannelDown: Qt.Key = ...  # 0x1000119
    Key_Guide: Qt.Key = ...  # 0x100011a
    Key_Info: Qt.Key = ...  # 0x100011b
    Key_Settings: Qt.Key = ...  # 0x100011c
    Key_MicVolumeUp: Qt.Key = ...  # 0x100011d
    Key_MicVolumeDown: Qt.Key = ...  # 0x100011e
    Key_New: Qt.Key = ...  # 0x1000120
    Key_Open: Qt.Key = ...  # 0x1000121
    Key_Find: Qt.Key = ...  # 0x1000122
    Key_Undo: Qt.Key = ...  # 0x1000123
    Key_Redo: Qt.Key = ...  # 0x1000124
    Key_AltGr: Qt.Key = ...  # 0x1001103
    Key_Multi_key: Qt.Key = ...  # 0x1001120
    Key_Kanji: Qt.Key = ...  # 0x1001121
    Key_Muhenkan: Qt.Key = ...  # 0x1001122
    Key_Henkan: Qt.Key = ...  # 0x1001123
    Key_Romaji: Qt.Key = ...  # 0x1001124
    Key_Hiragana: Qt.Key = ...  # 0x1001125
    Key_Katakana: Qt.Key = ...  # 0x1001126
    Key_Hiragana_Katakana: Qt.Key = ...  # 0x1001127
    Key_Zenkaku: Qt.Key = ...  # 0x1001128
    Key_Hankaku: Qt.Key = ...  # 0x1001129
    Key_Zenkaku_Hankaku: Qt.Key = ...  # 0x100112a
    Key_Touroku: Qt.Key = ...  # 0x100112b
    Key_Massyo: Qt.Key = ...  # 0x100112c
    Key_Kana_Lock: Qt.Key = ...  # 0x100112d
    Key_Kana_Shift: Qt.Key = ...  # 0x100112e
    Key_Eisu_Shift: Qt.Key = ...  # 0x100112f
    Key_Eisu_toggle: Qt.Key = ...  # 0x1001130
    Key_Hangul: Qt.Key = ...  # 0x1001131
    Key_Hangul_Start: Qt.Key = ...  # 0x1001132
    Key_Hangul_End: Qt.Key = ...  # 0x1001133
    Key_Hangul_Hanja: Qt.Key = ...  # 0x1001134
    Key_Hangul_Jamo: Qt.Key = ...  # 0x1001135
    Key_Hangul_Romaja: Qt.Key = ...  # 0x1001136
    Key_Codeinput: Qt.Key = ...  # 0x1001137
    Key_Hangul_Jeonja: Qt.Key = ...  # 0x1001138
    Key_Hangul_Banja: Qt.Key = ...  # 0x1001139
    Key_Hangul_PreHanja: Qt.Key = ...  # 0x100113a
    Key_Hangul_PostHanja: Qt.Key = ...  # 0x100113b
    Key_SingleCandidate: Qt.Key = ...  # 0x100113c
    Key_MultipleCandidate: Qt.Key = ...  # 0x100113d
    Key_PreviousCandidate: Qt.Key = ...  # 0x100113e
    Key_Hangul_Special: Qt.Key = ...  # 0x100113f
    Key_Mode_switch: Qt.Key = ...  # 0x100117e
    Key_Dead_Grave: Qt.Key = ...  # 0x1001250
    Key_Dead_Acute: Qt.Key = ...  # 0x1001251
    Key_Dead_Circumflex: Qt.Key = ...  # 0x1001252
    Key_Dead_Tilde: Qt.Key = ...  # 0x1001253
    Key_Dead_Macron: Qt.Key = ...  # 0x1001254
    Key_Dead_Breve: Qt.Key = ...  # 0x1001255
    Key_Dead_Abovedot: Qt.Key = ...  # 0x1001256
    Key_Dead_Diaeresis: Qt.Key = ...  # 0x1001257
    Key_Dead_Abovering: Qt.Key = ...  # 0x1001258
    Key_Dead_Doubleacute: Qt.Key = ...  # 0x1001259
    Key_Dead_Caron: Qt.Key = ...  # 0x100125a
    Key_Dead_Cedilla: Qt.Key = ...  # 0x100125b
    Key_Dead_Ogonek: Qt.Key = ...  # 0x100125c
    Key_Dead_Iota: Qt.Key = ...  # 0x100125d
    Key_Dead_Voiced_Sound: Qt.Key = ...  # 0x100125e
    Key_Dead_Semivoiced_Sound: Qt.Key = ...  # 0x100125f
    Key_Dead_Belowdot: Qt.Key = ...  # 0x1001260
    Key_Dead_Hook: Qt.Key = ...  # 0x1001261
    Key_Dead_Horn: Qt.Key = ...  # 0x1001262
    Key_Dead_Stroke: Qt.Key = ...  # 0x1001263
    Key_Dead_Abovecomma: Qt.Key = ...  # 0x1001264
    Key_Dead_Abovereversedcomma: Qt.Key = ...  # 0x1001265
    Key_Dead_Doublegrave: Qt.Key = ...  # 0x1001266
    Key_Dead_Belowring: Qt.Key = ...  # 0x1001267
    Key_Dead_Belowmacron: Qt.Key = ...  # 0x1001268
    Key_Dead_Belowcircumflex: Qt.Key = ...  # 0x1001269
    Key_Dead_Belowtilde: Qt.Key = ...  # 0x100126a
    Key_Dead_Belowbreve: Qt.Key = ...  # 0x100126b
    Key_Dead_Belowdiaeresis: Qt.Key = ...  # 0x100126c
    Key_Dead_Invertedbreve: Qt.Key = ...  # 0x100126d
    Key_Dead_Belowcomma: Qt.Key = ...  # 0x100126e
    Key_Dead_Currency: Qt.Key = ...  # 0x100126f
    Key_Dead_a: Qt.Key = ...  # 0x1001280
    Key_Dead_A: Qt.Key = ...  # 0x1001281
    Key_Dead_e: Qt.Key = ...  # 0x1001282
    Key_Dead_E: Qt.Key = ...  # 0x1001283
    Key_Dead_i: Qt.Key = ...  # 0x1001284
    Key_Dead_I: Qt.Key = ...  # 0x1001285
    Key_Dead_o: Qt.Key = ...  # 0x1001286
    Key_Dead_O: Qt.Key = ...  # 0x1001287
    Key_Dead_u: Qt.Key = ...  # 0x1001288
    Key_Dead_U: Qt.Key = ...  # 0x1001289
    Key_Dead_Small_Schwa: Qt.Key = ...  # 0x100128a
    Key_Dead_Capital_Schwa: Qt.Key = ...  # 0x100128b
    Key_Dead_Greek: Qt.Key = ...  # 0x100128c
    Key_Dead_Lowline: Qt.Key = ...  # 0x1001290
    Key_Dead_Aboveverticalline: Qt.Key = ...  # 0x1001291
    Key_Dead_Belowverticalline: Qt.Key = ...  # 0x1001292
    Key_Dead_Longsolidusoverlay: Qt.Key = ...  # 0x1001293
    Key_MediaLast: Qt.Key = ...  # 0x100ffff
    Key_Select: Qt.Key = ...  # 0x1010000
    Key_Yes: Qt.Key = ...  # 0x1010001
    Key_No: Qt.Key = ...  # 0x1010002
    Key_Cancel: Qt.Key = ...  # 0x1020001
    Key_Printer: Qt.Key = ...  # 0x1020002
    Key_Execute: Qt.Key = ...  # 0x1020003
    Key_Sleep: Qt.Key = ...  # 0x1020004
    Key_Play: Qt.Key = ...  # 0x1020005
    Key_Zoom: Qt.Key = ...  # 0x1020006
    Key_Exit: Qt.Key = ...  # 0x102000a
    Key_Context1: Qt.Key = ...  # 0x1100000
    Key_Context2: Qt.Key = ...  # 0x1100001
    Key_Context3: Qt.Key = ...  # 0x1100002
    Key_Context4: Qt.Key = ...  # 0x1100003
    Key_Call: Qt.Key = ...  # 0x1100004
    Key_Hangup: Qt.Key = ...  # 0x1100005
    Key_Flip: Qt.Key = ...  # 0x1100006
    Key_ToggleCallHangup: Qt.Key = ...  # 0x1100007
    Key_VoiceDial: Qt.Key = ...  # 0x1100008
    Key_LastNumberRedial: Qt.Key = ...  # 0x1100009
    Key_Camera: Qt.Key = ...  # 0x1100020
    Key_CameraFocus: Qt.Key = ...  # 0x1100021
    Key_unknown: Qt.Key = ...  # 0x1ffffff
    KeyboardModifierMask: Qt.KeyboardModifier = ...  # -0x2000000
    NoModifier: Qt.KeyboardModifier = ...  # 0x0
    ShiftModifier: Qt.KeyboardModifier = ...  # 0x2000000
    ControlModifier: Qt.KeyboardModifier = ...  # 0x4000000
    AltModifier: Qt.KeyboardModifier = ...  # 0x8000000
    MetaModifier: Qt.KeyboardModifier = ...  # 0x10000000
    KeypadModifier: Qt.KeyboardModifier = ...  # 0x20000000
    GroupSwitchModifier: Qt.KeyboardModifier = ...  # 0x40000000
    LeftToRight: Qt.LayoutDirection = ...  # 0x0
    RightToLeft: Qt.LayoutDirection = ...  # 0x1
    LayoutDirectionAuto: Qt.LayoutDirection = ...  # 0x2
    MaskInColor: Qt.MaskMode = ...  # 0x0
    MaskOutColor: Qt.MaskMode = ...  # 0x1
    MatchExactly: Qt.MatchFlag = ...  # 0x0
    MatchContains: Qt.MatchFlag = ...  # 0x1
    MatchStartsWith: Qt.MatchFlag = ...  # 0x2
    MatchEndsWith: Qt.MatchFlag = ...  # 0x3
    MatchRegularExpression: Qt.MatchFlag = ...  # 0x4
    MatchWildcard: Qt.MatchFlag = ...  # 0x5
    MatchFixedString: Qt.MatchFlag = ...  # 0x8
    MatchTypeMask: Qt.MatchFlag = ...  # 0xf
    MatchCaseSensitive: Qt.MatchFlag = ...  # 0x10
    MatchWrap: Qt.MatchFlag = ...  # 0x20
    MatchRecursive: Qt.MatchFlag = ...  # 0x40
    MODIFIER_MASK: Qt.Modifier = ...  # -0x2000000
    SHIFT: Qt.Modifier = ...  # 0x2000000
    CTRL: Qt.Modifier = ...  # 0x4000000
    ALT: Qt.Modifier = ...  # 0x8000000
    META: Qt.Modifier = ...  # 0x10000000
    MouseButtonMask: Qt.MouseButton = ...  # -0x1
    NoButton: Qt.MouseButton = ...  # 0x0
    LeftButton: Qt.MouseButton = ...  # 0x1
    RightButton: Qt.MouseButton = ...  # 0x2
    MiddleButton: Qt.MouseButton = ...  # 0x4
    BackButton: Qt.MouseButton = ...  # 0x8
    ExtraButton1: Qt.MouseButton = ...  # 0x8
    XButton1: Qt.MouseButton = ...  # 0x8
    ExtraButton2: Qt.MouseButton = ...  # 0x10
    ForwardButton: Qt.MouseButton = ...  # 0x10
    XButton2: Qt.MouseButton = ...  # 0x10
    ExtraButton3: Qt.MouseButton = ...  # 0x20
    TaskButton: Qt.MouseButton = ...  # 0x20
    ExtraButton4: Qt.MouseButton = ...  # 0x40
    ExtraButton5: Qt.MouseButton = ...  # 0x80
    ExtraButton6: Qt.MouseButton = ...  # 0x100
    ExtraButton7: Qt.MouseButton = ...  # 0x200
    ExtraButton8: Qt.MouseButton = ...  # 0x400
    ExtraButton9: Qt.MouseButton = ...  # 0x800
    ExtraButton10: Qt.MouseButton = ...  # 0x1000
    ExtraButton11: Qt.MouseButton = ...  # 0x2000
    ExtraButton12: Qt.MouseButton = ...  # 0x4000
    ExtraButton13: Qt.MouseButton = ...  # 0x8000
    ExtraButton14: Qt.MouseButton = ...  # 0x10000
    ExtraButton15: Qt.MouseButton = ...  # 0x20000
    ExtraButton16: Qt.MouseButton = ...  # 0x40000
    ExtraButton17: Qt.MouseButton = ...  # 0x80000
    ExtraButton18: Qt.MouseButton = ...  # 0x100000
    ExtraButton19: Qt.MouseButton = ...  # 0x200000
    ExtraButton20: Qt.MouseButton = ...  # 0x400000
    ExtraButton21: Qt.MouseButton = ...  # 0x800000
    ExtraButton22: Qt.MouseButton = ...  # 0x1000000
    ExtraButton23: Qt.MouseButton = ...  # 0x2000000
    ExtraButton24: Qt.MouseButton = ...  # 0x4000000
    MaxMouseButton: Qt.MouseButton = ...  # 0x4000000
    AllButtons: Qt.MouseButton = ...  # 0x7ffffff
    NoMouseEventFlag: Qt.MouseEventFlag = ...  # 0x0
    MouseEventCreatedDoubleClick: Qt.MouseEventFlag = ...  # 0x1
    MouseEventFlagMask: Qt.MouseEventFlag = ...  # 0xff
    MouseEventNotSynthesized: Qt.MouseEventSource = ...  # 0x0
    MouseEventSynthesizedBySystem: Qt.MouseEventSource = ...  # 0x1
    MouseEventSynthesizedByQt: Qt.MouseEventSource = ...  # 0x2
    MouseEventSynthesizedByApplication: Qt.MouseEventSource = ...  # 0x3
    BeginNativeGesture: Qt.NativeGestureType = ...  # 0x0
    EndNativeGesture: Qt.NativeGestureType = ...  # 0x1
    PanNativeGesture: Qt.NativeGestureType = ...  # 0x2
    ZoomNativeGesture: Qt.NativeGestureType = ...  # 0x3
    SmartZoomNativeGesture: Qt.NativeGestureType = ...  # 0x4
    RotateNativeGesture: Qt.NativeGestureType = ...  # 0x5
    SwipeNativeGesture: Qt.NativeGestureType = ...  # 0x6
    NavigationModeNone: Qt.NavigationMode = ...  # 0x0
    NavigationModeKeypadTabOrder: Qt.NavigationMode = ...  # 0x1
    NavigationModeKeypadDirectional: Qt.NavigationMode = ...  # 0x2
    NavigationModeCursorAuto: Qt.NavigationMode = ...  # 0x3
    NavigationModeCursorForceVisible: Qt.NavigationMode = ...  # 0x4
    Horizontal: Qt.Orientation = ...  # 0x1
    Vertical: Qt.Orientation = ...  # 0x2
    FlatCap: Qt.PenCapStyle = ...  # 0x0
    SquareCap: Qt.PenCapStyle = ...  # 0x10
    RoundCap: Qt.PenCapStyle = ...  # 0x20
    MPenCapStyle: Qt.PenCapStyle = ...  # 0x30
    MiterJoin: Qt.PenJoinStyle = ...  # 0x0
    BevelJoin: Qt.PenJoinStyle = ...  # 0x40
    RoundJoin: Qt.PenJoinStyle = ...  # 0x80
    SvgMiterJoin: Qt.PenJoinStyle = ...  # 0x100
    MPenJoinStyle: Qt.PenJoinStyle = ...  # 0x1c0
    NoPen: Qt.PenStyle = ...  # 0x0
    SolidLine: Qt.PenStyle = ...  # 0x1
    DashLine: Qt.PenStyle = ...  # 0x2
    DotLine: Qt.PenStyle = ...  # 0x3
    DashDotLine: Qt.PenStyle = ...  # 0x4
    DashDotDotLine: Qt.PenStyle = ...  # 0x5
    CustomDashLine: Qt.PenStyle = ...  # 0x6
    MPenStyle: Qt.PenStyle = ...  # 0xf
    ReturnByValue: Qt.ReturnByValueConstant = ...  # 0x0
    PrimaryOrientation: Qt.ScreenOrientation = ...  # 0x0
    PortraitOrientation: Qt.ScreenOrientation = ...  # 0x1
    LandscapeOrientation: Qt.ScreenOrientation = ...  # 0x2
    InvertedPortraitOrientation: Qt.ScreenOrientation = ...  # 0x4
    InvertedLandscapeOrientation: Qt.ScreenOrientation = ...  # 0x8
    ScrollBarAsNeeded: Qt.ScrollBarPolicy = ...  # 0x0
    ScrollBarAlwaysOff: Qt.ScrollBarPolicy = ...  # 0x1
    ScrollBarAlwaysOn: Qt.ScrollBarPolicy = ...  # 0x2
    NoScrollPhase: Qt.ScrollPhase = ...  # 0x0
    ScrollBegin: Qt.ScrollPhase = ...  # 0x1
    ScrollUpdate: Qt.ScrollPhase = ...  # 0x2
    ScrollEnd: Qt.ScrollPhase = ...  # 0x3
    ScrollMomentum: Qt.ScrollPhase = ...  # 0x4
    WidgetShortcut: Qt.ShortcutContext = ...  # 0x0
    WindowShortcut: Qt.ShortcutContext = ...  # 0x1
    ApplicationShortcut: Qt.ShortcutContext = ...  # 0x2
    WidgetWithChildrenShortcut: Qt.ShortcutContext = ...  # 0x3
    MinimumSize: Qt.SizeHint = ...  # 0x0
    PreferredSize: Qt.SizeHint = ...  # 0x1
    MaximumSize: Qt.SizeHint = ...  # 0x2
    MinimumDescent: Qt.SizeHint = ...  # 0x3
    NSizeHints: Qt.SizeHint = ...  # 0x4
    AbsoluteSize: Qt.SizeMode = ...  # 0x0
    RelativeSize: Qt.SizeMode = ...  # 0x1
    AscendingOrder: Qt.SortOrder = ...  # 0x0
    DescendingOrder: Qt.SortOrder = ...  # 0x1
    KeepEmptyParts: Qt.SplitBehaviorFlags = ...  # 0x0
    SkipEmptyParts: Qt.SplitBehaviorFlags = ...  # 0x1
    NoTabFocus: Qt.TabFocusBehavior = ...  # 0x0
    TabFocusTextControls: Qt.TabFocusBehavior = ...  # 0x1
    TabFocusListControls: Qt.TabFocusBehavior = ...  # 0x2
    TabFocusAllControls: Qt.TabFocusBehavior = ...  # 0xff
    ElideLeft: Qt.TextElideMode = ...  # 0x0
    ElideRight: Qt.TextElideMode = ...  # 0x1
    ElideMiddle: Qt.TextElideMode = ...  # 0x2
    ElideNone: Qt.TextElideMode = ...  # 0x3
    TextSingleLine: Qt.TextFlag = ...  # 0x100
    TextDontClip: Qt.TextFlag = ...  # 0x200
    TextExpandTabs: Qt.TextFlag = ...  # 0x400
    TextShowMnemonic: Qt.TextFlag = ...  # 0x800
    TextWordWrap: Qt.TextFlag = ...  # 0x1000
    TextWrapAnywhere: Qt.TextFlag = ...  # 0x2000
    TextDontPrint: Qt.TextFlag = ...  # 0x4000
    TextHideMnemonic: Qt.TextFlag = ...  # 0x8000
    TextJustificationForced: Qt.TextFlag = ...  # 0x10000
    TextForceLeftToRight: Qt.TextFlag = ...  # 0x20000
    TextForceRightToLeft: Qt.TextFlag = ...  # 0x40000
    TextLongestVariant: Qt.TextFlag = ...  # 0x80000
    TextIncludeTrailingSpaces: Qt.TextFlag = ...  # 0x8000000
    PlainText: Qt.TextFormat = ...  # 0x0
    RichText: Qt.TextFormat = ...  # 0x1
    AutoText: Qt.TextFormat = ...  # 0x2
    MarkdownText: Qt.TextFormat = ...  # 0x3
    NoTextInteraction: Qt.TextInteractionFlag = ...  # 0x0
    TextSelectableByMouse: Qt.TextInteractionFlag = ...  # 0x1
    TextSelectableByKeyboard: Qt.TextInteractionFlag = ...  # 0x2
    LinksAccessibleByMouse: Qt.TextInteractionFlag = ...  # 0x4
    LinksAccessibleByKeyboard: Qt.TextInteractionFlag = ...  # 0x8
    TextBrowserInteraction: Qt.TextInteractionFlag = ...  # 0xd
    TextEditable: Qt.TextInteractionFlag = ...  # 0x10
    TextEditorInteraction: Qt.TextInteractionFlag = ...  # 0x13
    StretchTile: Qt.TileRule = ...  # 0x0
    RepeatTile: Qt.TileRule = ...  # 0x1
    RoundTile: Qt.TileRule = ...  # 0x2
    LocalTime: Qt.TimeSpec = ...  # 0x0
    UTC: Qt.TimeSpec = ...  # 0x1
    OffsetFromUTC: Qt.TimeSpec = ...  # 0x2
    TimeZone: Qt.TimeSpec = ...  # 0x3
    PreciseTimer: Qt.TimerType = ...  # 0x0
    CoarseTimer: Qt.TimerType = ...  # 0x1
    VeryCoarseTimer: Qt.TimerType = ...  # 0x2
    NoToolBarArea: Qt.ToolBarArea = ...  # 0x0
    LeftToolBarArea: Qt.ToolBarArea = ...  # 0x1
    RightToolBarArea: Qt.ToolBarArea = ...  # 0x2
    TopToolBarArea: Qt.ToolBarArea = ...  # 0x4
    BottomToolBarArea: Qt.ToolBarArea = ...  # 0x8
    AllToolBarAreas: Qt.ToolBarArea = ...  # 0xf
    ToolBarArea_Mask: Qt.ToolBarArea = ...  # 0xf
    NToolBarAreas: Qt.ToolBarAreaSizes = ...  # 0x4
    ToolButtonIconOnly: Qt.ToolButtonStyle = ...  # 0x0
    ToolButtonTextOnly: Qt.ToolButtonStyle = ...  # 0x1
    ToolButtonTextBesideIcon: Qt.ToolButtonStyle = ...  # 0x2
    ToolButtonTextUnderIcon: Qt.ToolButtonStyle = ...  # 0x3
    ToolButtonFollowStyle: Qt.ToolButtonStyle = ...  # 0x4
    TouchPointUnknownState: Qt.TouchPointState = ...  # 0x0
    TouchPointPressed: Qt.TouchPointState = ...  # 0x1
    TouchPointMoved: Qt.TouchPointState = ...  # 0x2
    TouchPointStationary: Qt.TouchPointState = ...  # 0x4
    TouchPointReleased: Qt.TouchPointState = ...  # 0x8
    FastTransformation: Qt.TransformationMode = ...  # 0x0
    SmoothTransformation: Qt.TransformationMode = ...  # 0x1
    UI_General: Qt.UIEffect = ...  # 0x0
    UI_AnimateMenu: Qt.UIEffect = ...  # 0x1
    UI_FadeMenu: Qt.UIEffect = ...  # 0x2
    UI_AnimateCombo: Qt.UIEffect = ...  # 0x3
    UI_AnimateTooltip: Qt.UIEffect = ...  # 0x4
    UI_FadeTooltip: Qt.UIEffect = ...  # 0x5
    UI_AnimateToolBox: Qt.UIEffect = ...  # 0x6
    WhiteSpaceModeUndefined: Qt.WhiteSpaceMode = ...  # -0x1
    WhiteSpaceNormal: Qt.WhiteSpaceMode = ...  # 0x0
    WhiteSpacePre: Qt.WhiteSpaceMode = ...  # 0x1
    WhiteSpaceNoWrap: Qt.WhiteSpaceMode = ...  # 0x2
    WA_Disabled: Qt.WidgetAttribute = ...  # 0x0
    WA_UnderMouse: Qt.WidgetAttribute = ...  # 0x1
    WA_MouseTracking: Qt.WidgetAttribute = ...  # 0x2
    WA_OpaquePaintEvent: Qt.WidgetAttribute = ...  # 0x4
    WA_StaticContents: Qt.WidgetAttribute = ...  # 0x5
    WA_LaidOut: Qt.WidgetAttribute = ...  # 0x7
    WA_PaintOnScreen: Qt.WidgetAttribute = ...  # 0x8
    WA_NoSystemBackground: Qt.WidgetAttribute = ...  # 0x9
    WA_UpdatesDisabled: Qt.WidgetAttribute = ...  # 0xa
    WA_Mapped: Qt.WidgetAttribute = ...  # 0xb
    WA_InputMethodEnabled: Qt.WidgetAttribute = ...  # 0xe
    WA_WState_Visible: Qt.WidgetAttribute = ...  # 0xf
    WA_WState_Hidden: Qt.WidgetAttribute = ...  # 0x10
    WA_ForceDisabled: Qt.WidgetAttribute = ...  # 0x20
    WA_KeyCompression: Qt.WidgetAttribute = ...  # 0x21
    WA_PendingMoveEvent: Qt.WidgetAttribute = ...  # 0x22
    WA_PendingResizeEvent: Qt.WidgetAttribute = ...  # 0x23
    WA_SetPalette: Qt.WidgetAttribute = ...  # 0x24
    WA_SetFont: Qt.WidgetAttribute = ...  # 0x25
    WA_SetCursor: Qt.WidgetAttribute = ...  # 0x26
    WA_NoChildEventsFromChildren: Qt.WidgetAttribute = ...  # 0x27
    WA_WindowModified: Qt.WidgetAttribute = ...  # 0x29
    WA_Resized: Qt.WidgetAttribute = ...  # 0x2a
    WA_Moved: Qt.WidgetAttribute = ...  # 0x2b
    WA_PendingUpdate: Qt.WidgetAttribute = ...  # 0x2c
    WA_InvalidSize: Qt.WidgetAttribute = ...  # 0x2d
    WA_CustomWhatsThis: Qt.WidgetAttribute = ...  # 0x2f
    WA_LayoutOnEntireRect: Qt.WidgetAttribute = ...  # 0x30
    WA_OutsideWSRange: Qt.WidgetAttribute = ...  # 0x31
    WA_GrabbedShortcut: Qt.WidgetAttribute = ...  # 0x32
    WA_TransparentForMouseEvents: Qt.WidgetAttribute = ...  # 0x33
    WA_PaintUnclipped: Qt.WidgetAttribute = ...  # 0x34
    WA_SetWindowIcon: Qt.WidgetAttribute = ...  # 0x35
    WA_NoMouseReplay: Qt.WidgetAttribute = ...  # 0x36
    WA_DeleteOnClose: Qt.WidgetAttribute = ...  # 0x37
    WA_RightToLeft: Qt.WidgetAttribute = ...  # 0x38
    WA_SetLayoutDirection: Qt.WidgetAttribute = ...  # 0x39
    WA_NoChildEventsForParent: Qt.WidgetAttribute = ...  # 0x3a
    WA_ForceUpdatesDisabled: Qt.WidgetAttribute = ...  # 0x3b
    WA_WState_Created: Qt.WidgetAttribute = ...  # 0x3c
    WA_WState_CompressKeys: Qt.WidgetAttribute = ...  # 0x3d
    WA_WState_InPaintEvent: Qt.WidgetAttribute = ...  # 0x3e
    WA_WState_Reparented: Qt.WidgetAttribute = ...  # 0x3f
    WA_WState_ConfigPending: Qt.WidgetAttribute = ...  # 0x40
    WA_WState_Polished: Qt.WidgetAttribute = ...  # 0x42
    WA_WState_OwnSizePolicy: Qt.WidgetAttribute = ...  # 0x44
    WA_WState_ExplicitShowHide: Qt.WidgetAttribute = ...  # 0x45
    WA_ShowModal: Qt.WidgetAttribute = ...  # 0x46
    WA_MouseNoMask: Qt.WidgetAttribute = ...  # 0x47
    WA_NoMousePropagation: Qt.WidgetAttribute = ...  # 0x49
    WA_Hover: Qt.WidgetAttribute = ...  # 0x4a
    WA_InputMethodTransparent: Qt.WidgetAttribute = ...  # 0x4b
    WA_QuitOnClose: Qt.WidgetAttribute = ...  # 0x4c
    WA_KeyboardFocusChange: Qt.WidgetAttribute = ...  # 0x4d
    WA_AcceptDrops: Qt.WidgetAttribute = ...  # 0x4e
    WA_DropSiteRegistered: Qt.WidgetAttribute = ...  # 0x4f
    WA_WindowPropagation: Qt.WidgetAttribute = ...  # 0x50
    WA_NoX11EventCompression: Qt.WidgetAttribute = ...  # 0x51
    WA_TintedBackground: Qt.WidgetAttribute = ...  # 0x52
    WA_X11OpenGLOverlay: Qt.WidgetAttribute = ...  # 0x53
    WA_AlwaysShowToolTips: Qt.WidgetAttribute = ...  # 0x54
    WA_MacOpaqueSizeGrip: Qt.WidgetAttribute = ...  # 0x55
    WA_SetStyle: Qt.WidgetAttribute = ...  # 0x56
    WA_SetLocale: Qt.WidgetAttribute = ...  # 0x57
    WA_MacShowFocusRect: Qt.WidgetAttribute = ...  # 0x58
    WA_MacNormalSize: Qt.WidgetAttribute = ...  # 0x59
    WA_MacSmallSize: Qt.WidgetAttribute = ...  # 0x5a
    WA_MacMiniSize: Qt.WidgetAttribute = ...  # 0x5b
    WA_LayoutUsesWidgetRect: Qt.WidgetAttribute = ...  # 0x5c
    WA_StyledBackground: Qt.WidgetAttribute = ...  # 0x5d
    WA_CanHostQMdiSubWindowTitleBar: Qt.WidgetAttribute = ...  # 0x5f
    WA_MacAlwaysShowToolWindow: Qt.WidgetAttribute = ...  # 0x60
    WA_StyleSheet: Qt.WidgetAttribute = ...  # 0x61
    WA_ShowWithoutActivating: Qt.WidgetAttribute = ...  # 0x62
    WA_X11BypassTransientForHint: Qt.WidgetAttribute = ...  # 0x63
    WA_NativeWindow: Qt.WidgetAttribute = ...  # 0x64
    WA_DontCreateNativeAncestors: Qt.WidgetAttribute = ...  # 0x65
    WA_DontShowOnScreen: Qt.WidgetAttribute = ...  # 0x67
    WA_X11NetWmWindowTypeDesktop: Qt.WidgetAttribute = ...  # 0x68
    WA_X11NetWmWindowTypeDock: Qt.WidgetAttribute = ...  # 0x69
    WA_X11NetWmWindowTypeToolBar: Qt.WidgetAttribute = ...  # 0x6a
    WA_X11NetWmWindowTypeMenu: Qt.WidgetAttribute = ...  # 0x6b
    WA_X11NetWmWindowTypeUtility: Qt.WidgetAttribute = ...  # 0x6c
    WA_X11NetWmWindowTypeSplash: Qt.WidgetAttribute = ...  # 0x6d
    WA_X11NetWmWindowTypeDialog: Qt.WidgetAttribute = ...  # 0x6e
    WA_X11NetWmWindowTypeDropDownMenu: Qt.WidgetAttribute = ...  # 0x6f
    WA_X11NetWmWindowTypePopupMenu: Qt.WidgetAttribute = ...  # 0x70
    WA_X11NetWmWindowTypeToolTip: Qt.WidgetAttribute = ...  # 0x71
    WA_X11NetWmWindowTypeNotification: Qt.WidgetAttribute = ...  # 0x72
    WA_X11NetWmWindowTypeCombo: Qt.WidgetAttribute = ...  # 0x73
    WA_X11NetWmWindowTypeDND: Qt.WidgetAttribute = ...  # 0x74
    WA_SetWindowModality: Qt.WidgetAttribute = ...  # 0x76
    WA_WState_WindowOpacitySet: Qt.WidgetAttribute = ...  # 0x77
    WA_TranslucentBackground: Qt.WidgetAttribute = ...  # 0x78
    WA_AcceptTouchEvents: Qt.WidgetAttribute = ...  # 0x79
    WA_WState_AcceptedTouchBeginEvent: Qt.WidgetAttribute = ...  # 0x7a
    WA_TouchPadAcceptSingleTouchEvents: Qt.WidgetAttribute = ...  # 0x7b
    WA_X11DoNotAcceptFocus: Qt.WidgetAttribute = ...  # 0x7e
    WA_AlwaysStackOnTop: Qt.WidgetAttribute = ...  # 0x80
    WA_TabletTracking: Qt.WidgetAttribute = ...  # 0x81
    WA_ContentsMarginsRespectsSafeArea: Qt.WidgetAttribute = ...  # 0x82
    WA_StyleSheetTarget: Qt.WidgetAttribute = ...  # 0x83
    WA_AttributeCount: Qt.WidgetAttribute = ...  # 0x84
    NoSection: Qt.WindowFrameSection = ...  # 0x0
    LeftSection: Qt.WindowFrameSection = ...  # 0x1
    TopLeftSection: Qt.WindowFrameSection = ...  # 0x2
    TopSection: Qt.WindowFrameSection = ...  # 0x3
    TopRightSection: Qt.WindowFrameSection = ...  # 0x4
    RightSection: Qt.WindowFrameSection = ...  # 0x5
    BottomRightSection: Qt.WindowFrameSection = ...  # 0x6
    BottomSection: Qt.WindowFrameSection = ...  # 0x7
    BottomLeftSection: Qt.WindowFrameSection = ...  # 0x8
    TitleBarArea: Qt.WindowFrameSection = ...  # 0x9
    NonModal: Qt.WindowModality = ...  # 0x0
    WindowModal: Qt.WindowModality = ...  # 0x1
    ApplicationModal: Qt.WindowModality = ...  # 0x2
    WindowNoState: Qt.WindowState = ...  # 0x0
    WindowMinimized: Qt.WindowState = ...  # 0x1
    WindowMaximized: Qt.WindowState = ...  # 0x2
    WindowFullScreen: Qt.WindowState = ...  # 0x4
    WindowActive: Qt.WindowState = ...  # 0x8
    WindowFullscreenButtonHint: Qt.WindowType = ...  # -0x80000000
    Widget: Qt.WindowType = ...  # 0x0
    Window: Qt.WindowType = ...  # 0x1
    Dialog: Qt.WindowType = ...  # 0x3
    Sheet: Qt.WindowType = ...  # 0x5
    Drawer: Qt.WindowType = ...  # 0x7
    Popup: Qt.WindowType = ...  # 0x9
    Tool: Qt.WindowType = ...  # 0xb
    ToolTip: Qt.WindowType = ...  # 0xd
    SplashScreen: Qt.WindowType = ...  # 0xf
    Desktop: Qt.WindowType = ...  # 0x11
    SubWindow: Qt.WindowType = ...  # 0x12
    ForeignWindow: Qt.WindowType = ...  # 0x21
    CoverWindow: Qt.WindowType = ...  # 0x41
    WindowType_Mask: Qt.WindowType = ...  # 0xff
    MSWindowsFixedSizeDialogHint: Qt.WindowType = ...  # 0x100
    MSWindowsOwnDC: Qt.WindowType = ...  # 0x200
    BypassWindowManagerHint: Qt.WindowType = ...  # 0x400
    X11BypassWindowManagerHint: Qt.WindowType = ...  # 0x400
    FramelessWindowHint: Qt.WindowType = ...  # 0x800
    WindowTitleHint: Qt.WindowType = ...  # 0x1000
    WindowSystemMenuHint: Qt.WindowType = ...  # 0x2000
    WindowMinimizeButtonHint: Qt.WindowType = ...  # 0x4000
    WindowMaximizeButtonHint: Qt.WindowType = ...  # 0x8000
    WindowMinMaxButtonsHint: Qt.WindowType = ...  # 0xc000
    WindowContextHelpButtonHint: Qt.WindowType = ...  # 0x10000
    WindowShadeButtonHint: Qt.WindowType = ...  # 0x20000
    WindowStaysOnTopHint: Qt.WindowType = ...  # 0x40000
    WindowTransparentForInput: Qt.WindowType = ...  # 0x80000
    WindowOverridesSystemGestures: Qt.WindowType = ...  # 0x100000
    WindowDoesNotAcceptFocus: Qt.WindowType = ...  # 0x200000
    MaximizeUsingFullscreenGeometryHint: Qt.WindowType = ...  # 0x400000
    CustomizeWindowHint: Qt.WindowType = ...  # 0x2000000
    WindowStaysOnBottomHint: Qt.WindowType = ...  # 0x4000000
    WindowCloseButtonHint: Qt.WindowType = ...  # 0x8000000
    MacWindowToolBarButtonHint: Qt.WindowType = ...  # 0x10000000
    BypassGraphicsProxyWidget: Qt.WindowType = ...  # 0x20000000
    NoDropShadowWindowHint: Qt.WindowType = ...  # 0x40000000
    class Alignment(object): ...
    class AlignmentFlag(Enum):

        AlignLeading: Qt.AlignmentFlag = ...  # 0x1
        AlignLeft: Qt.AlignmentFlag = ...  # 0x1
        AlignRight: Qt.AlignmentFlag = ...  # 0x2
        AlignTrailing: Qt.AlignmentFlag = ...  # 0x2
        AlignHCenter: Qt.AlignmentFlag = ...  # 0x4
        AlignJustify: Qt.AlignmentFlag = ...  # 0x8
        AlignAbsolute: Qt.AlignmentFlag = ...  # 0x10
        AlignHorizontal_Mask: Qt.AlignmentFlag = ...  # 0x1f
        AlignTop: Qt.AlignmentFlag = ...  # 0x20
        AlignBottom: Qt.AlignmentFlag = ...  # 0x40
        AlignVCenter: Qt.AlignmentFlag = ...  # 0x80
        AlignCenter: Qt.AlignmentFlag = ...  # 0x84
        AlignBaseline: Qt.AlignmentFlag = ...  # 0x100
        AlignVertical_Mask: Qt.AlignmentFlag = ...  # 0x1e0
    class AnchorPoint(Enum):

        AnchorLeft: Qt.AnchorPoint = ...  # 0x0
        AnchorHorizontalCenter: Qt.AnchorPoint = ...  # 0x1
        AnchorRight: Qt.AnchorPoint = ...  # 0x2
        AnchorTop: Qt.AnchorPoint = ...  # 0x3
        AnchorVerticalCenter: Qt.AnchorPoint = ...  # 0x4
        AnchorBottom: Qt.AnchorPoint = ...  # 0x5
    class ApplicationAttribute(Enum):

        AA_DontShowIconsInMenus: Qt.ApplicationAttribute = ...  # 0x2
        AA_NativeWindows: Qt.ApplicationAttribute = ...  # 0x3
        AA_DontCreateNativeWidgetSiblings: Qt.ApplicationAttribute = ...  # 0x4
        AA_PluginApplication: Qt.ApplicationAttribute = ...  # 0x5
        AA_DontUseNativeMenuBar: Qt.ApplicationAttribute = ...  # 0x6
        AA_MacDontSwapCtrlAndMeta: Qt.ApplicationAttribute = ...  # 0x7
        AA_Use96Dpi: Qt.ApplicationAttribute = ...  # 0x8
        AA_DisableNativeVirtualKeyboard: Qt.ApplicationAttribute = ...  # 0x9
        AA_SynthesizeTouchForUnhandledMouseEvents: Qt.ApplicationAttribute = ...  # 0xb
        AA_SynthesizeMouseForUnhandledTouchEvents: Qt.ApplicationAttribute = ...  # 0xc
        AA_UseHighDpiPixmaps: Qt.ApplicationAttribute = ...  # 0xd
        AA_ForceRasterWidgets: Qt.ApplicationAttribute = ...  # 0xe
        AA_UseDesktopOpenGL: Qt.ApplicationAttribute = ...  # 0xf
        AA_UseOpenGLES: Qt.ApplicationAttribute = ...  # 0x10
        AA_UseSoftwareOpenGL: Qt.ApplicationAttribute = ...  # 0x11
        AA_ShareOpenGLContexts: Qt.ApplicationAttribute = ...  # 0x12
        AA_SetPalette: Qt.ApplicationAttribute = ...  # 0x13
        AA_EnableHighDpiScaling: Qt.ApplicationAttribute = ...  # 0x14
        AA_DisableHighDpiScaling: Qt.ApplicationAttribute = ...  # 0x15
        AA_UseStyleSheetPropagationInWidgetStyles: Qt.ApplicationAttribute = ...  # 0x16
        AA_DontUseNativeDialogs: Qt.ApplicationAttribute = ...  # 0x17
        AA_SynthesizeMouseForUnhandledTabletEvents: Qt.ApplicationAttribute = ...  # 0x18
        AA_CompressHighFrequencyEvents: Qt.ApplicationAttribute = ...  # 0x19
        AA_DontCheckOpenGLContextThreadAffinity: Qt.ApplicationAttribute = ...  # 0x1a
        AA_DisableShaderDiskCache: Qt.ApplicationAttribute = ...  # 0x1b
        AA_DontShowShortcutsInContextMenus: Qt.ApplicationAttribute = ...  # 0x1c
        AA_CompressTabletEvents: Qt.ApplicationAttribute = ...  # 0x1d
        AA_DisableSessionManager: Qt.ApplicationAttribute = ...  # 0x1f
        AA_AttributeCount: Qt.ApplicationAttribute = ...  # 0x20
    class ApplicationState(Enum):

        ApplicationSuspended: Qt.ApplicationState = ...  # 0x0
        ApplicationHidden: Qt.ApplicationState = ...  # 0x1
        ApplicationInactive: Qt.ApplicationState = ...  # 0x2
        ApplicationActive: Qt.ApplicationState = ...  # 0x4
    class ApplicationStates(object): ...
    class ArrowType(Enum):

        NoArrow: Qt.ArrowType = ...  # 0x0
        UpArrow: Qt.ArrowType = ...  # 0x1
        DownArrow: Qt.ArrowType = ...  # 0x2
        LeftArrow: Qt.ArrowType = ...  # 0x3
        RightArrow: Qt.ArrowType = ...  # 0x4
    class AspectRatioMode(Enum):

        IgnoreAspectRatio: Qt.AspectRatioMode = ...  # 0x0
        KeepAspectRatio: Qt.AspectRatioMode = ...  # 0x1
        KeepAspectRatioByExpanding: Qt.AspectRatioMode = ...  # 0x2
    class Axis(Enum):

        XAxis: Qt.Axis = ...  # 0x0
        YAxis: Qt.Axis = ...  # 0x1
        ZAxis: Qt.Axis = ...  # 0x2
    class BGMode(Enum):

        TransparentMode: Qt.BGMode = ...  # 0x0
        OpaqueMode: Qt.BGMode = ...  # 0x1
    class BrushStyle(Enum):

        NoBrush: Qt.BrushStyle = ...  # 0x0
        SolidPattern: Qt.BrushStyle = ...  # 0x1
        Dense1Pattern: Qt.BrushStyle = ...  # 0x2
        Dense2Pattern: Qt.BrushStyle = ...  # 0x3
        Dense3Pattern: Qt.BrushStyle = ...  # 0x4
        Dense4Pattern: Qt.BrushStyle = ...  # 0x5
        Dense5Pattern: Qt.BrushStyle = ...  # 0x6
        Dense6Pattern: Qt.BrushStyle = ...  # 0x7
        Dense7Pattern: Qt.BrushStyle = ...  # 0x8
        HorPattern: Qt.BrushStyle = ...  # 0x9
        VerPattern: Qt.BrushStyle = ...  # 0xa
        CrossPattern: Qt.BrushStyle = ...  # 0xb
        BDiagPattern: Qt.BrushStyle = ...  # 0xc
        FDiagPattern: Qt.BrushStyle = ...  # 0xd
        DiagCrossPattern: Qt.BrushStyle = ...  # 0xe
        LinearGradientPattern: Qt.BrushStyle = ...  # 0xf
        RadialGradientPattern: Qt.BrushStyle = ...  # 0x10
        ConicalGradientPattern: Qt.BrushStyle = ...  # 0x11
        TexturePattern: Qt.BrushStyle = ...  # 0x18
    class CaseSensitivity(Enum):

        CaseInsensitive: Qt.CaseSensitivity = ...  # 0x0
        CaseSensitive: Qt.CaseSensitivity = ...  # 0x1
    class CheckState(Enum):

        Unchecked: Qt.CheckState = ...  # 0x0
        PartiallyChecked: Qt.CheckState = ...  # 0x1
        Checked: Qt.CheckState = ...  # 0x2
    class ChecksumType(Enum):

        ChecksumIso3309: Qt.ChecksumType = ...  # 0x0
        ChecksumItuV41: Qt.ChecksumType = ...  # 0x1
    class ClipOperation(Enum):

        NoClip: Qt.ClipOperation = ...  # 0x0
        ReplaceClip: Qt.ClipOperation = ...  # 0x1
        IntersectClip: Qt.ClipOperation = ...  # 0x2
    class ConnectionType(Enum):

        AutoConnection: Qt.ConnectionType = ...  # 0x0
        DirectConnection: Qt.ConnectionType = ...  # 0x1
        QueuedConnection: Qt.ConnectionType = ...  # 0x2
        BlockingQueuedConnection: Qt.ConnectionType = ...  # 0x3
        UniqueConnection: Qt.ConnectionType = ...  # 0x80
        SingleShotConnection: Qt.ConnectionType = ...  # 0x100
    class ContextMenuPolicy(Enum):

        NoContextMenu: Qt.ContextMenuPolicy = ...  # 0x0
        DefaultContextMenu: Qt.ContextMenuPolicy = ...  # 0x1
        ActionsContextMenu: Qt.ContextMenuPolicy = ...  # 0x2
        CustomContextMenu: Qt.ContextMenuPolicy = ...  # 0x3
        PreventContextMenu: Qt.ContextMenuPolicy = ...  # 0x4
    class CoordinateSystem(Enum):

        DeviceCoordinates: Qt.CoordinateSystem = ...  # 0x0
        LogicalCoordinates: Qt.CoordinateSystem = ...  # 0x1
    class Corner(Enum):

        TopLeftCorner: Qt.Corner = ...  # 0x0
        TopRightCorner: Qt.Corner = ...  # 0x1
        BottomLeftCorner: Qt.Corner = ...  # 0x2
        BottomRightCorner: Qt.Corner = ...  # 0x3
    class CursorMoveStyle(Enum):

        LogicalMoveStyle: Qt.CursorMoveStyle = ...  # 0x0
        VisualMoveStyle: Qt.CursorMoveStyle = ...  # 0x1
    class CursorShape(Enum):

        ArrowCursor: Qt.CursorShape = ...  # 0x0
        UpArrowCursor: Qt.CursorShape = ...  # 0x1
        CrossCursor: Qt.CursorShape = ...  # 0x2
        WaitCursor: Qt.CursorShape = ...  # 0x3
        IBeamCursor: Qt.CursorShape = ...  # 0x4
        SizeVerCursor: Qt.CursorShape = ...  # 0x5
        SizeHorCursor: Qt.CursorShape = ...  # 0x6
        SizeBDiagCursor: Qt.CursorShape = ...  # 0x7
        SizeFDiagCursor: Qt.CursorShape = ...  # 0x8
        SizeAllCursor: Qt.CursorShape = ...  # 0x9
        BlankCursor: Qt.CursorShape = ...  # 0xa
        SplitVCursor: Qt.CursorShape = ...  # 0xb
        SplitHCursor: Qt.CursorShape = ...  # 0xc
        PointingHandCursor: Qt.CursorShape = ...  # 0xd
        ForbiddenCursor: Qt.CursorShape = ...  # 0xe
        WhatsThisCursor: Qt.CursorShape = ...  # 0xf
        BusyCursor: Qt.CursorShape = ...  # 0x10
        OpenHandCursor: Qt.CursorShape = ...  # 0x11
        ClosedHandCursor: Qt.CursorShape = ...  # 0x12
        DragCopyCursor: Qt.CursorShape = ...  # 0x13
        DragMoveCursor: Qt.CursorShape = ...  # 0x14
        DragLinkCursor: Qt.CursorShape = ...  # 0x15
        LastCursor: Qt.CursorShape = ...  # 0x15
        BitmapCursor: Qt.CursorShape = ...  # 0x18
        CustomCursor: Qt.CursorShape = ...  # 0x19
    class DateFormat(Enum):

        TextDate: Qt.DateFormat = ...  # 0x0
        ISODate: Qt.DateFormat = ...  # 0x1
        RFC2822Date: Qt.DateFormat = ...  # 0x8
        ISODateWithMs: Qt.DateFormat = ...  # 0x9
    class DayOfWeek(Enum):

        Monday: Qt.DayOfWeek = ...  # 0x1
        Tuesday: Qt.DayOfWeek = ...  # 0x2
        Wednesday: Qt.DayOfWeek = ...  # 0x3
        Thursday: Qt.DayOfWeek = ...  # 0x4
        Friday: Qt.DayOfWeek = ...  # 0x5
        Saturday: Qt.DayOfWeek = ...  # 0x6
        Sunday: Qt.DayOfWeek = ...  # 0x7
    class DockWidgetArea(Enum):

        NoDockWidgetArea: Qt.DockWidgetArea = ...  # 0x0
        LeftDockWidgetArea: Qt.DockWidgetArea = ...  # 0x1
        RightDockWidgetArea: Qt.DockWidgetArea = ...  # 0x2
        TopDockWidgetArea: Qt.DockWidgetArea = ...  # 0x4
        BottomDockWidgetArea: Qt.DockWidgetArea = ...  # 0x8
        AllDockWidgetAreas: Qt.DockWidgetArea = ...  # 0xf
        DockWidgetArea_Mask: Qt.DockWidgetArea = ...  # 0xf
    class DockWidgetAreaSizes(Enum):

        NDockWidgetAreas: Qt.DockWidgetAreaSizes = ...  # 0x4
    class DockWidgetAreas(object): ...
    class DropAction(Enum):

        IgnoreAction: Qt.DropAction = ...  # 0x0
        CopyAction: Qt.DropAction = ...  # 0x1
        MoveAction: Qt.DropAction = ...  # 0x2
        LinkAction: Qt.DropAction = ...  # 0x4
        ActionMask: Qt.DropAction = ...  # 0xff
        TargetMoveAction: Qt.DropAction = ...  # 0x8002
    class DropActions(object): ...
    class Edge(Enum):

        TopEdge: Qt.Edge = ...  # 0x1
        LeftEdge: Qt.Edge = ...  # 0x2
        RightEdge: Qt.Edge = ...  # 0x4
        BottomEdge: Qt.Edge = ...  # 0x8
    class Edges(object): ...
    class EnterKeyType(Enum):

        EnterKeyDefault: Qt.EnterKeyType = ...  # 0x0
        EnterKeyReturn: Qt.EnterKeyType = ...  # 0x1
        EnterKeyDone: Qt.EnterKeyType = ...  # 0x2
        EnterKeyGo: Qt.EnterKeyType = ...  # 0x3
        EnterKeySend: Qt.EnterKeyType = ...  # 0x4
        EnterKeySearch: Qt.EnterKeyType = ...  # 0x5
        EnterKeyNext: Qt.EnterKeyType = ...  # 0x6
        EnterKeyPrevious: Qt.EnterKeyType = ...  # 0x7
    class EventPriority(Enum):

        LowEventPriority: Qt.EventPriority = ...  # -0x1
        NormalEventPriority: Qt.EventPriority = ...  # 0x0
        HighEventPriority: Qt.EventPriority = ...  # 0x1
    class FillRule(Enum):

        OddEvenFill: Qt.FillRule = ...  # 0x0
        WindingFill: Qt.FillRule = ...  # 0x1
    class FindChildOption(Enum):

        FindDirectChildrenOnly: Qt.FindChildOption = ...  # 0x0
        FindChildrenRecursively: Qt.FindChildOption = ...  # 0x1
    class FindChildOptions(object): ...
    class FocusPolicy(Enum):

        NoFocus: Qt.FocusPolicy = ...  # 0x0
        TabFocus: Qt.FocusPolicy = ...  # 0x1
        ClickFocus: Qt.FocusPolicy = ...  # 0x2
        StrongFocus: Qt.FocusPolicy = ...  # 0xb
        WheelFocus: Qt.FocusPolicy = ...  # 0xf
    class FocusReason(Enum):

        MouseFocusReason: Qt.FocusReason = ...  # 0x0
        TabFocusReason: Qt.FocusReason = ...  # 0x1
        BacktabFocusReason: Qt.FocusReason = ...  # 0x2
        ActiveWindowFocusReason: Qt.FocusReason = ...  # 0x3
        PopupFocusReason: Qt.FocusReason = ...  # 0x4
        ShortcutFocusReason: Qt.FocusReason = ...  # 0x5
        MenuBarFocusReason: Qt.FocusReason = ...  # 0x6
        OtherFocusReason: Qt.FocusReason = ...  # 0x7
        NoFocusReason: Qt.FocusReason = ...  # 0x8
    class GestureFlag(Enum):

        DontStartGestureOnChildren: Qt.GestureFlag = ...  # 0x1
        ReceivePartialGestures: Qt.GestureFlag = ...  # 0x2
        IgnoredGesturesPropagateToParent: Qt.GestureFlag = ...  # 0x4
    class GestureFlags(object): ...
    class GestureState(Enum):

        NoGesture: Qt.GestureState = ...  # 0x0
        GestureStarted: Qt.GestureState = ...  # 0x1
        GestureUpdated: Qt.GestureState = ...  # 0x2
        GestureFinished: Qt.GestureState = ...  # 0x3
        GestureCanceled: Qt.GestureState = ...  # 0x4
    class GestureType(Enum):

        LastGestureType: Qt.GestureType = ...  # -0x1
        TapGesture: Qt.GestureType = ...  # 0x1
        TapAndHoldGesture: Qt.GestureType = ...  # 0x2
        PanGesture: Qt.GestureType = ...  # 0x3
        PinchGesture: Qt.GestureType = ...  # 0x4
        SwipeGesture: Qt.GestureType = ...  # 0x5
        CustomGesture: Qt.GestureType = ...  # 0x100
    class GlobalColor(Enum):

        color0: Qt.GlobalColor = ...  # 0x0
        color1: Qt.GlobalColor = ...  # 0x1
        black: Qt.GlobalColor = ...  # 0x2
        white: Qt.GlobalColor = ...  # 0x3
        darkGray: Qt.GlobalColor = ...  # 0x4
        gray: Qt.GlobalColor = ...  # 0x5
        lightGray: Qt.GlobalColor = ...  # 0x6
        red: Qt.GlobalColor = ...  # 0x7
        green: Qt.GlobalColor = ...  # 0x8
        blue: Qt.GlobalColor = ...  # 0x9
        cyan: Qt.GlobalColor = ...  # 0xa
        magenta: Qt.GlobalColor = ...  # 0xb
        yellow: Qt.GlobalColor = ...  # 0xc
        darkRed: Qt.GlobalColor = ...  # 0xd
        darkGreen: Qt.GlobalColor = ...  # 0xe
        darkBlue: Qt.GlobalColor = ...  # 0xf
        darkCyan: Qt.GlobalColor = ...  # 0x10
        darkMagenta: Qt.GlobalColor = ...  # 0x11
        darkYellow: Qt.GlobalColor = ...  # 0x12
        transparent: Qt.GlobalColor = ...  # 0x13
    class HighDpiScaleFactorRoundingPolicy(Enum):

        Unset: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x0
        Round: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x1
        Ceil: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x2
        Floor: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x3
        RoundPreferFloor: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x4
        PassThrough: Qt.HighDpiScaleFactorRoundingPolicy = ...  # 0x5
    class HitTestAccuracy(Enum):

        ExactHit: Qt.HitTestAccuracy = ...  # 0x0
        FuzzyHit: Qt.HitTestAccuracy = ...  # 0x1
    class ImageConversionFlag(Enum):

        AutoColor: Qt.ImageConversionFlag = ...  # 0x0
        AutoDither: Qt.ImageConversionFlag = ...  # 0x0
        DiffuseDither: Qt.ImageConversionFlag = ...  # 0x0
        ThresholdAlphaDither: Qt.ImageConversionFlag = ...  # 0x0
        MonoOnly: Qt.ImageConversionFlag = ...  # 0x2
        ColorMode_Mask: Qt.ImageConversionFlag = ...  # 0x3
        ColorOnly: Qt.ImageConversionFlag = ...  # 0x3
        OrderedAlphaDither: Qt.ImageConversionFlag = ...  # 0x4
        DiffuseAlphaDither: Qt.ImageConversionFlag = ...  # 0x8
        AlphaDither_Mask: Qt.ImageConversionFlag = ...  # 0xc
        NoAlpha: Qt.ImageConversionFlag = ...  # 0xc
        OrderedDither: Qt.ImageConversionFlag = ...  # 0x10
        ThresholdDither: Qt.ImageConversionFlag = ...  # 0x20
        Dither_Mask: Qt.ImageConversionFlag = ...  # 0x30
        PreferDither: Qt.ImageConversionFlag = ...  # 0x40
        AvoidDither: Qt.ImageConversionFlag = ...  # 0x80
        DitherMode_Mask: Qt.ImageConversionFlag = ...  # 0xc0
        NoOpaqueDetection: Qt.ImageConversionFlag = ...  # 0x100
        NoFormatConversion: Qt.ImageConversionFlag = ...  # 0x200
    class ImageConversionFlags(object): ...
    class InputMethodHint(Enum):

        ImhExclusiveInputMask: Qt.InputMethodHint = ...  # -0x10000
        ImhNone: Qt.InputMethodHint = ...  # 0x0
        ImhHiddenText: Qt.InputMethodHint = ...  # 0x1
        ImhSensitiveData: Qt.InputMethodHint = ...  # 0x2
        ImhNoAutoUppercase: Qt.InputMethodHint = ...  # 0x4
        ImhPreferNumbers: Qt.InputMethodHint = ...  # 0x8
        ImhPreferUppercase: Qt.InputMethodHint = ...  # 0x10
        ImhPreferLowercase: Qt.InputMethodHint = ...  # 0x20
        ImhNoPredictiveText: Qt.InputMethodHint = ...  # 0x40
        ImhDate: Qt.InputMethodHint = ...  # 0x80
        ImhTime: Qt.InputMethodHint = ...  # 0x100
        ImhPreferLatin: Qt.InputMethodHint = ...  # 0x200
        ImhMultiLine: Qt.InputMethodHint = ...  # 0x400
        ImhNoEditMenu: Qt.InputMethodHint = ...  # 0x800
        ImhNoTextHandles: Qt.InputMethodHint = ...  # 0x1000
        ImhDigitsOnly: Qt.InputMethodHint = ...  # 0x10000
        ImhFormattedNumbersOnly: Qt.InputMethodHint = ...  # 0x20000
        ImhUppercaseOnly: Qt.InputMethodHint = ...  # 0x40000
        ImhLowercaseOnly: Qt.InputMethodHint = ...  # 0x80000
        ImhDialableCharactersOnly: Qt.InputMethodHint = ...  # 0x100000
        ImhEmailCharactersOnly: Qt.InputMethodHint = ...  # 0x200000
        ImhUrlCharactersOnly: Qt.InputMethodHint = ...  # 0x400000
        ImhLatinOnly: Qt.InputMethodHint = ...  # 0x800000
    class InputMethodHints(object): ...
    class InputMethodQueries(object): ...
    class InputMethodQuery(Enum):

        ImPlatformData: Qt.InputMethodQuery = ...  # -0x80000000
        ImQueryAll: Qt.InputMethodQuery = ...  # -0x1
        ImEnabled: Qt.InputMethodQuery = ...  # 0x1
        ImCursorRectangle: Qt.InputMethodQuery = ...  # 0x2
        ImFont: Qt.InputMethodQuery = ...  # 0x4
        ImCursorPosition: Qt.InputMethodQuery = ...  # 0x8
        ImSurroundingText: Qt.InputMethodQuery = ...  # 0x10
        ImCurrentSelection: Qt.InputMethodQuery = ...  # 0x20
        ImMaximumTextLength: Qt.InputMethodQuery = ...  # 0x40
        ImAnchorPosition: Qt.InputMethodQuery = ...  # 0x80
        ImHints: Qt.InputMethodQuery = ...  # 0x100
        ImPreferredLanguage: Qt.InputMethodQuery = ...  # 0x200
        ImAbsolutePosition: Qt.InputMethodQuery = ...  # 0x400
        ImTextBeforeCursor: Qt.InputMethodQuery = ...  # 0x800
        ImTextAfterCursor: Qt.InputMethodQuery = ...  # 0x1000
        ImEnterKeyType: Qt.InputMethodQuery = ...  # 0x2000
        ImAnchorRectangle: Qt.InputMethodQuery = ...  # 0x4000
        ImQueryInput: Qt.InputMethodQuery = ...  # 0x40ba
        ImInputItemClipRectangle: Qt.InputMethodQuery = ...  # 0x8000
        ImReadOnly: Qt.InputMethodQuery = ...  # 0x10000
    class ItemDataRole(Enum):

        DisplayRole: Qt.ItemDataRole = ...  # 0x0
        DecorationRole: Qt.ItemDataRole = ...  # 0x1
        EditRole: Qt.ItemDataRole = ...  # 0x2
        ToolTipRole: Qt.ItemDataRole = ...  # 0x3
        StatusTipRole: Qt.ItemDataRole = ...  # 0x4
        WhatsThisRole: Qt.ItemDataRole = ...  # 0x5
        FontRole: Qt.ItemDataRole = ...  # 0x6
        TextAlignmentRole: Qt.ItemDataRole = ...  # 0x7
        BackgroundRole: Qt.ItemDataRole = ...  # 0x8
        ForegroundRole: Qt.ItemDataRole = ...  # 0x9
        CheckStateRole: Qt.ItemDataRole = ...  # 0xa
        AccessibleTextRole: Qt.ItemDataRole = ...  # 0xb
        AccessibleDescriptionRole: Qt.ItemDataRole = ...  # 0xc
        SizeHintRole: Qt.ItemDataRole = ...  # 0xd
        InitialSortOrderRole: Qt.ItemDataRole = ...  # 0xe
        DisplayPropertyRole: Qt.ItemDataRole = ...  # 0x1b
        DecorationPropertyRole: Qt.ItemDataRole = ...  # 0x1c
        ToolTipPropertyRole: Qt.ItemDataRole = ...  # 0x1d
        StatusTipPropertyRole: Qt.ItemDataRole = ...  # 0x1e
        WhatsThisPropertyRole: Qt.ItemDataRole = ...  # 0x1f
        UserRole: Qt.ItemDataRole = ...  # 0x100
    class ItemFlag(Enum):

        NoItemFlags: Qt.ItemFlag = ...  # 0x0
        ItemIsSelectable: Qt.ItemFlag = ...  # 0x1
        ItemIsEditable: Qt.ItemFlag = ...  # 0x2
        ItemIsDragEnabled: Qt.ItemFlag = ...  # 0x4
        ItemIsDropEnabled: Qt.ItemFlag = ...  # 0x8
        ItemIsUserCheckable: Qt.ItemFlag = ...  # 0x10
        ItemIsEnabled: Qt.ItemFlag = ...  # 0x20
        ItemIsAutoTristate: Qt.ItemFlag = ...  # 0x40
        ItemNeverHasChildren: Qt.ItemFlag = ...  # 0x80
        ItemIsUserTristate: Qt.ItemFlag = ...  # 0x100
        def __or__(self, arg_2: Qt.ItemFlag) -> Qt.ItemFlag: ...
    class ItemFlags(object): ...
    class ItemSelectionMode(Enum):

        ContainsItemShape: Qt.ItemSelectionMode = ...  # 0x0
        IntersectsItemShape: Qt.ItemSelectionMode = ...  # 0x1
        ContainsItemBoundingRect: Qt.ItemSelectionMode = ...  # 0x2
        IntersectsItemBoundingRect: Qt.ItemSelectionMode = ...  # 0x3
    class ItemSelectionOperation(Enum):

        ReplaceSelection: Qt.ItemSelectionOperation = ...  # 0x0
        AddToSelection: Qt.ItemSelectionOperation = ...  # 0x1
    class Key(Enum):

        Key_Any: Qt.Key = ...  # 0x20
        Key_Space: Qt.Key = ...  # 0x20
        Key_Exclam: Qt.Key = ...  # 0x21
        Key_QuoteDbl: Qt.Key = ...  # 0x22
        Key_NumberSign: Qt.Key = ...  # 0x23
        Key_Dollar: Qt.Key = ...  # 0x24
        Key_Percent: Qt.Key = ...  # 0x25
        Key_Ampersand: Qt.Key = ...  # 0x26
        Key_Apostrophe: Qt.Key = ...  # 0x27
        Key_ParenLeft: Qt.Key = ...  # 0x28
        Key_ParenRight: Qt.Key = ...  # 0x29
        Key_Asterisk: Qt.Key = ...  # 0x2a
        Key_Plus: Qt.Key = ...  # 0x2b
        Key_Comma: Qt.Key = ...  # 0x2c
        Key_Minus: Qt.Key = ...  # 0x2d
        Key_Period: Qt.Key = ...  # 0x2e
        Key_Slash: Qt.Key = ...  # 0x2f
        Key_0: Qt.Key = ...  # 0x30
        Key_1: Qt.Key = ...  # 0x31
        Key_2: Qt.Key = ...  # 0x32
        Key_3: Qt.Key = ...  # 0x33
        Key_4: Qt.Key = ...  # 0x34
        Key_5: Qt.Key = ...  # 0x35
        Key_6: Qt.Key = ...  # 0x36
        Key_7: Qt.Key = ...  # 0x37
        Key_8: Qt.Key = ...  # 0x38
        Key_9: Qt.Key = ...  # 0x39
        Key_Colon: Qt.Key = ...  # 0x3a
        Key_Semicolon: Qt.Key = ...  # 0x3b
        Key_Less: Qt.Key = ...  # 0x3c
        Key_Equal: Qt.Key = ...  # 0x3d
        Key_Greater: Qt.Key = ...  # 0x3e
        Key_Question: Qt.Key = ...  # 0x3f
        Key_At: Qt.Key = ...  # 0x40
        Key_A: Qt.Key = ...  # 0x41
        Key_B: Qt.Key = ...  # 0x42
        Key_C: Qt.Key = ...  # 0x43
        Key_D: Qt.Key = ...  # 0x44
        Key_E: Qt.Key = ...  # 0x45
        Key_F: Qt.Key = ...  # 0x46
        Key_G: Qt.Key = ...  # 0x47
        Key_H: Qt.Key = ...  # 0x48
        Key_I: Qt.Key = ...  # 0x49
        Key_J: Qt.Key = ...  # 0x4a
        Key_K: Qt.Key = ...  # 0x4b
        Key_L: Qt.Key = ...  # 0x4c
        Key_M: Qt.Key = ...  # 0x4d
        Key_N: Qt.Key = ...  # 0x4e
        Key_O: Qt.Key = ...  # 0x4f
        Key_P: Qt.Key = ...  # 0x50
        Key_Q: Qt.Key = ...  # 0x51
        Key_R: Qt.Key = ...  # 0x52
        Key_S: Qt.Key = ...  # 0x53
        Key_T: Qt.Key = ...  # 0x54
        Key_U: Qt.Key = ...  # 0x55
        Key_V: Qt.Key = ...  # 0x56
        Key_W: Qt.Key = ...  # 0x57
        Key_X: Qt.Key = ...  # 0x58
        Key_Y: Qt.Key = ...  # 0x59
        Key_Z: Qt.Key = ...  # 0x5a
        Key_BracketLeft: Qt.Key = ...  # 0x5b
        Key_Backslash: Qt.Key = ...  # 0x5c
        Key_BracketRight: Qt.Key = ...  # 0x5d
        Key_AsciiCircum: Qt.Key = ...  # 0x5e
        Key_Underscore: Qt.Key = ...  # 0x5f
        Key_QuoteLeft: Qt.Key = ...  # 0x60
        Key_BraceLeft: Qt.Key = ...  # 0x7b
        Key_Bar: Qt.Key = ...  # 0x7c
        Key_BraceRight: Qt.Key = ...  # 0x7d
        Key_AsciiTilde: Qt.Key = ...  # 0x7e
        Key_nobreakspace: Qt.Key = ...  # 0xa0
        Key_exclamdown: Qt.Key = ...  # 0xa1
        Key_cent: Qt.Key = ...  # 0xa2
        Key_sterling: Qt.Key = ...  # 0xa3
        Key_currency: Qt.Key = ...  # 0xa4
        Key_yen: Qt.Key = ...  # 0xa5
        Key_brokenbar: Qt.Key = ...  # 0xa6
        Key_section: Qt.Key = ...  # 0xa7
        Key_diaeresis: Qt.Key = ...  # 0xa8
        Key_copyright: Qt.Key = ...  # 0xa9
        Key_ordfeminine: Qt.Key = ...  # 0xaa
        Key_guillemotleft: Qt.Key = ...  # 0xab
        Key_notsign: Qt.Key = ...  # 0xac
        Key_hyphen: Qt.Key = ...  # 0xad
        Key_registered: Qt.Key = ...  # 0xae
        Key_macron: Qt.Key = ...  # 0xaf
        Key_degree: Qt.Key = ...  # 0xb0
        Key_plusminus: Qt.Key = ...  # 0xb1
        Key_twosuperior: Qt.Key = ...  # 0xb2
        Key_threesuperior: Qt.Key = ...  # 0xb3
        Key_acute: Qt.Key = ...  # 0xb4
        Key_mu: Qt.Key = ...  # 0xb5
        Key_paragraph: Qt.Key = ...  # 0xb6
        Key_periodcentered: Qt.Key = ...  # 0xb7
        Key_cedilla: Qt.Key = ...  # 0xb8
        Key_onesuperior: Qt.Key = ...  # 0xb9
        Key_masculine: Qt.Key = ...  # 0xba
        Key_guillemotright: Qt.Key = ...  # 0xbb
        Key_onequarter: Qt.Key = ...  # 0xbc
        Key_onehalf: Qt.Key = ...  # 0xbd
        Key_threequarters: Qt.Key = ...  # 0xbe
        Key_questiondown: Qt.Key = ...  # 0xbf
        Key_Agrave: Qt.Key = ...  # 0xc0
        Key_Aacute: Qt.Key = ...  # 0xc1
        Key_Acircumflex: Qt.Key = ...  # 0xc2
        Key_Atilde: Qt.Key = ...  # 0xc3
        Key_Adiaeresis: Qt.Key = ...  # 0xc4
        Key_Aring: Qt.Key = ...  # 0xc5
        Key_AE: Qt.Key = ...  # 0xc6
        Key_Ccedilla: Qt.Key = ...  # 0xc7
        Key_Egrave: Qt.Key = ...  # 0xc8
        Key_Eacute: Qt.Key = ...  # 0xc9
        Key_Ecircumflex: Qt.Key = ...  # 0xca
        Key_Ediaeresis: Qt.Key = ...  # 0xcb
        Key_Igrave: Qt.Key = ...  # 0xcc
        Key_Iacute: Qt.Key = ...  # 0xcd
        Key_Icircumflex: Qt.Key = ...  # 0xce
        Key_Idiaeresis: Qt.Key = ...  # 0xcf
        Key_ETH: Qt.Key = ...  # 0xd0
        Key_Ntilde: Qt.Key = ...  # 0xd1
        Key_Ograve: Qt.Key = ...  # 0xd2
        Key_Oacute: Qt.Key = ...  # 0xd3
        Key_Ocircumflex: Qt.Key = ...  # 0xd4
        Key_Otilde: Qt.Key = ...  # 0xd5
        Key_Odiaeresis: Qt.Key = ...  # 0xd6
        Key_multiply: Qt.Key = ...  # 0xd7
        Key_Ooblique: Qt.Key = ...  # 0xd8
        Key_Ugrave: Qt.Key = ...  # 0xd9
        Key_Uacute: Qt.Key = ...  # 0xda
        Key_Ucircumflex: Qt.Key = ...  # 0xdb
        Key_Udiaeresis: Qt.Key = ...  # 0xdc
        Key_Yacute: Qt.Key = ...  # 0xdd
        Key_THORN: Qt.Key = ...  # 0xde
        Key_ssharp: Qt.Key = ...  # 0xdf
        Key_division: Qt.Key = ...  # 0xf7
        Key_ydiaeresis: Qt.Key = ...  # 0xff
        Key_Escape: Qt.Key = ...  # 0x1000000
        Key_Tab: Qt.Key = ...  # 0x1000001
        Key_Backtab: Qt.Key = ...  # 0x1000002
        Key_Backspace: Qt.Key = ...  # 0x1000003
        Key_Return: Qt.Key = ...  # 0x1000004
        Key_Enter: Qt.Key = ...  # 0x1000005
        Key_Insert: Qt.Key = ...  # 0x1000006
        Key_Delete: Qt.Key = ...  # 0x1000007
        Key_Pause: Qt.Key = ...  # 0x1000008
        Key_Print: Qt.Key = ...  # 0x1000009
        Key_SysReq: Qt.Key = ...  # 0x100000a
        Key_Clear: Qt.Key = ...  # 0x100000b
        Key_Home: Qt.Key = ...  # 0x1000010
        Key_End: Qt.Key = ...  # 0x1000011
        Key_Left: Qt.Key = ...  # 0x1000012
        Key_Up: Qt.Key = ...  # 0x1000013
        Key_Right: Qt.Key = ...  # 0x1000014
        Key_Down: Qt.Key = ...  # 0x1000015
        Key_PageUp: Qt.Key = ...  # 0x1000016
        Key_PageDown: Qt.Key = ...  # 0x1000017
        Key_Shift: Qt.Key = ...  # 0x1000020
        Key_Control: Qt.Key = ...  # 0x1000021
        Key_Meta: Qt.Key = ...  # 0x1000022
        Key_Alt: Qt.Key = ...  # 0x1000023
        Key_CapsLock: Qt.Key = ...  # 0x1000024
        Key_NumLock: Qt.Key = ...  # 0x1000025
        Key_ScrollLock: Qt.Key = ...  # 0x1000026
        Key_F1: Qt.Key = ...  # 0x1000030
        Key_F2: Qt.Key = ...  # 0x1000031
        Key_F3: Qt.Key = ...  # 0x1000032
        Key_F4: Qt.Key = ...  # 0x1000033
        Key_F5: Qt.Key = ...  # 0x1000034
        Key_F6: Qt.Key = ...  # 0x1000035
        Key_F7: Qt.Key = ...  # 0x1000036
        Key_F8: Qt.Key = ...  # 0x1000037
        Key_F9: Qt.Key = ...  # 0x1000038
        Key_F10: Qt.Key = ...  # 0x1000039
        Key_F11: Qt.Key = ...  # 0x100003a
        Key_F12: Qt.Key = ...  # 0x100003b
        Key_F13: Qt.Key = ...  # 0x100003c
        Key_F14: Qt.Key = ...  # 0x100003d
        Key_F15: Qt.Key = ...  # 0x100003e
        Key_F16: Qt.Key = ...  # 0x100003f
        Key_F17: Qt.Key = ...  # 0x1000040
        Key_F18: Qt.Key = ...  # 0x1000041
        Key_F19: Qt.Key = ...  # 0x1000042
        Key_F20: Qt.Key = ...  # 0x1000043
        Key_F21: Qt.Key = ...  # 0x1000044
        Key_F22: Qt.Key = ...  # 0x1000045
        Key_F23: Qt.Key = ...  # 0x1000046
        Key_F24: Qt.Key = ...  # 0x1000047
        Key_F25: Qt.Key = ...  # 0x1000048
        Key_F26: Qt.Key = ...  # 0x1000049
        Key_F27: Qt.Key = ...  # 0x100004a
        Key_F28: Qt.Key = ...  # 0x100004b
        Key_F29: Qt.Key = ...  # 0x100004c
        Key_F30: Qt.Key = ...  # 0x100004d
        Key_F31: Qt.Key = ...  # 0x100004e
        Key_F32: Qt.Key = ...  # 0x100004f
        Key_F33: Qt.Key = ...  # 0x1000050
        Key_F34: Qt.Key = ...  # 0x1000051
        Key_F35: Qt.Key = ...  # 0x1000052
        Key_Super_L: Qt.Key = ...  # 0x1000053
        Key_Super_R: Qt.Key = ...  # 0x1000054
        Key_Menu: Qt.Key = ...  # 0x1000055
        Key_Hyper_L: Qt.Key = ...  # 0x1000056
        Key_Hyper_R: Qt.Key = ...  # 0x1000057
        Key_Help: Qt.Key = ...  # 0x1000058
        Key_Direction_L: Qt.Key = ...  # 0x1000059
        Key_Direction_R: Qt.Key = ...  # 0x1000060
        Key_Back: Qt.Key = ...  # 0x1000061
        Key_Forward: Qt.Key = ...  # 0x1000062
        Key_Stop: Qt.Key = ...  # 0x1000063
        Key_Refresh: Qt.Key = ...  # 0x1000064
        Key_VolumeDown: Qt.Key = ...  # 0x1000070
        Key_VolumeMute: Qt.Key = ...  # 0x1000071
        Key_VolumeUp: Qt.Key = ...  # 0x1000072
        Key_BassBoost: Qt.Key = ...  # 0x1000073
        Key_BassUp: Qt.Key = ...  # 0x1000074
        Key_BassDown: Qt.Key = ...  # 0x1000075
        Key_TrebleUp: Qt.Key = ...  # 0x1000076
        Key_TrebleDown: Qt.Key = ...  # 0x1000077
        Key_MediaPlay: Qt.Key = ...  # 0x1000080
        Key_MediaStop: Qt.Key = ...  # 0x1000081
        Key_MediaPrevious: Qt.Key = ...  # 0x1000082
        Key_MediaNext: Qt.Key = ...  # 0x1000083
        Key_MediaRecord: Qt.Key = ...  # 0x1000084
        Key_MediaPause: Qt.Key = ...  # 0x1000085
        Key_MediaTogglePlayPause: Qt.Key = ...  # 0x1000086
        Key_HomePage: Qt.Key = ...  # 0x1000090
        Key_Favorites: Qt.Key = ...  # 0x1000091
        Key_Search: Qt.Key = ...  # 0x1000092
        Key_Standby: Qt.Key = ...  # 0x1000093
        Key_OpenUrl: Qt.Key = ...  # 0x1000094
        Key_LaunchMail: Qt.Key = ...  # 0x10000a0
        Key_LaunchMedia: Qt.Key = ...  # 0x10000a1
        Key_Launch0: Qt.Key = ...  # 0x10000a2
        Key_Launch1: Qt.Key = ...  # 0x10000a3
        Key_Launch2: Qt.Key = ...  # 0x10000a4
        Key_Launch3: Qt.Key = ...  # 0x10000a5
        Key_Launch4: Qt.Key = ...  # 0x10000a6
        Key_Launch5: Qt.Key = ...  # 0x10000a7
        Key_Launch6: Qt.Key = ...  # 0x10000a8
        Key_Launch7: Qt.Key = ...  # 0x10000a9
        Key_Launch8: Qt.Key = ...  # 0x10000aa
        Key_Launch9: Qt.Key = ...  # 0x10000ab
        Key_LaunchA: Qt.Key = ...  # 0x10000ac
        Key_LaunchB: Qt.Key = ...  # 0x10000ad
        Key_LaunchC: Qt.Key = ...  # 0x10000ae
        Key_LaunchD: Qt.Key = ...  # 0x10000af
        Key_LaunchE: Qt.Key = ...  # 0x10000b0
        Key_LaunchF: Qt.Key = ...  # 0x10000b1
        Key_MonBrightnessUp: Qt.Key = ...  # 0x10000b2
        Key_MonBrightnessDown: Qt.Key = ...  # 0x10000b3
        Key_KeyboardLightOnOff: Qt.Key = ...  # 0x10000b4
        Key_KeyboardBrightnessUp: Qt.Key = ...  # 0x10000b5
        Key_KeyboardBrightnessDown: Qt.Key = ...  # 0x10000b6
        Key_PowerOff: Qt.Key = ...  # 0x10000b7
        Key_WakeUp: Qt.Key = ...  # 0x10000b8
        Key_Eject: Qt.Key = ...  # 0x10000b9
        Key_ScreenSaver: Qt.Key = ...  # 0x10000ba
        Key_WWW: Qt.Key = ...  # 0x10000bb
        Key_Memo: Qt.Key = ...  # 0x10000bc
        Key_LightBulb: Qt.Key = ...  # 0x10000bd
        Key_Shop: Qt.Key = ...  # 0x10000be
        Key_History: Qt.Key = ...  # 0x10000bf
        Key_AddFavorite: Qt.Key = ...  # 0x10000c0
        Key_HotLinks: Qt.Key = ...  # 0x10000c1
        Key_BrightnessAdjust: Qt.Key = ...  # 0x10000c2
        Key_Finance: Qt.Key = ...  # 0x10000c3
        Key_Community: Qt.Key = ...  # 0x10000c4
        Key_AudioRewind: Qt.Key = ...  # 0x10000c5
        Key_BackForward: Qt.Key = ...  # 0x10000c6
        Key_ApplicationLeft: Qt.Key = ...  # 0x10000c7
        Key_ApplicationRight: Qt.Key = ...  # 0x10000c8
        Key_Book: Qt.Key = ...  # 0x10000c9
        Key_CD: Qt.Key = ...  # 0x10000ca
        Key_Calculator: Qt.Key = ...  # 0x10000cb
        Key_ToDoList: Qt.Key = ...  # 0x10000cc
        Key_ClearGrab: Qt.Key = ...  # 0x10000cd
        Key_Close: Qt.Key = ...  # 0x10000ce
        Key_Copy: Qt.Key = ...  # 0x10000cf
        Key_Cut: Qt.Key = ...  # 0x10000d0
        Key_Display: Qt.Key = ...  # 0x10000d1
        Key_DOS: Qt.Key = ...  # 0x10000d2
        Key_Documents: Qt.Key = ...  # 0x10000d3
        Key_Excel: Qt.Key = ...  # 0x10000d4
        Key_Explorer: Qt.Key = ...  # 0x10000d5
        Key_Game: Qt.Key = ...  # 0x10000d6
        Key_Go: Qt.Key = ...  # 0x10000d7
        Key_iTouch: Qt.Key = ...  # 0x10000d8
        Key_LogOff: Qt.Key = ...  # 0x10000d9
        Key_Market: Qt.Key = ...  # 0x10000da
        Key_Meeting: Qt.Key = ...  # 0x10000db
        Key_MenuKB: Qt.Key = ...  # 0x10000dc
        Key_MenuPB: Qt.Key = ...  # 0x10000dd
        Key_MySites: Qt.Key = ...  # 0x10000de
        Key_News: Qt.Key = ...  # 0x10000df
        Key_OfficeHome: Qt.Key = ...  # 0x10000e0
        Key_Option: Qt.Key = ...  # 0x10000e1
        Key_Paste: Qt.Key = ...  # 0x10000e2
        Key_Phone: Qt.Key = ...  # 0x10000e3
        Key_Calendar: Qt.Key = ...  # 0x10000e4
        Key_Reply: Qt.Key = ...  # 0x10000e5
        Key_Reload: Qt.Key = ...  # 0x10000e6
        Key_RotateWindows: Qt.Key = ...  # 0x10000e7
        Key_RotationPB: Qt.Key = ...  # 0x10000e8
        Key_RotationKB: Qt.Key = ...  # 0x10000e9
        Key_Save: Qt.Key = ...  # 0x10000ea
        Key_Send: Qt.Key = ...  # 0x10000eb
        Key_Spell: Qt.Key = ...  # 0x10000ec
        Key_SplitScreen: Qt.Key = ...  # 0x10000ed
        Key_Support: Qt.Key = ...  # 0x10000ee
        Key_TaskPane: Qt.Key = ...  # 0x10000ef
        Key_Terminal: Qt.Key = ...  # 0x10000f0
        Key_Tools: Qt.Key = ...  # 0x10000f1
        Key_Travel: Qt.Key = ...  # 0x10000f2
        Key_Video: Qt.Key = ...  # 0x10000f3
        Key_Word: Qt.Key = ...  # 0x10000f4
        Key_Xfer: Qt.Key = ...  # 0x10000f5
        Key_ZoomIn: Qt.Key = ...  # 0x10000f6
        Key_ZoomOut: Qt.Key = ...  # 0x10000f7
        Key_Away: Qt.Key = ...  # 0x10000f8
        Key_Messenger: Qt.Key = ...  # 0x10000f9
        Key_WebCam: Qt.Key = ...  # 0x10000fa
        Key_MailForward: Qt.Key = ...  # 0x10000fb
        Key_Pictures: Qt.Key = ...  # 0x10000fc
        Key_Music: Qt.Key = ...  # 0x10000fd
        Key_Battery: Qt.Key = ...  # 0x10000fe
        Key_Bluetooth: Qt.Key = ...  # 0x10000ff
        Key_WLAN: Qt.Key = ...  # 0x1000100
        Key_UWB: Qt.Key = ...  # 0x1000101
        Key_AudioForward: Qt.Key = ...  # 0x1000102
        Key_AudioRepeat: Qt.Key = ...  # 0x1000103
        Key_AudioRandomPlay: Qt.Key = ...  # 0x1000104
        Key_Subtitle: Qt.Key = ...  # 0x1000105
        Key_AudioCycleTrack: Qt.Key = ...  # 0x1000106
        Key_Time: Qt.Key = ...  # 0x1000107
        Key_Hibernate: Qt.Key = ...  # 0x1000108
        Key_View: Qt.Key = ...  # 0x1000109
        Key_TopMenu: Qt.Key = ...  # 0x100010a
        Key_PowerDown: Qt.Key = ...  # 0x100010b
        Key_Suspend: Qt.Key = ...  # 0x100010c
        Key_ContrastAdjust: Qt.Key = ...  # 0x100010d
        Key_LaunchG: Qt.Key = ...  # 0x100010e
        Key_LaunchH: Qt.Key = ...  # 0x100010f
        Key_TouchpadToggle: Qt.Key = ...  # 0x1000110
        Key_TouchpadOn: Qt.Key = ...  # 0x1000111
        Key_TouchpadOff: Qt.Key = ...  # 0x1000112
        Key_MicMute: Qt.Key = ...  # 0x1000113
        Key_Red: Qt.Key = ...  # 0x1000114
        Key_Green: Qt.Key = ...  # 0x1000115
        Key_Yellow: Qt.Key = ...  # 0x1000116
        Key_Blue: Qt.Key = ...  # 0x1000117
        Key_ChannelUp: Qt.Key = ...  # 0x1000118
        Key_ChannelDown: Qt.Key = ...  # 0x1000119
        Key_Guide: Qt.Key = ...  # 0x100011a
        Key_Info: Qt.Key = ...  # 0x100011b
        Key_Settings: Qt.Key = ...  # 0x100011c
        Key_MicVolumeUp: Qt.Key = ...  # 0x100011d
        Key_MicVolumeDown: Qt.Key = ...  # 0x100011e
        Key_New: Qt.Key = ...  # 0x1000120
        Key_Open: Qt.Key = ...  # 0x1000121
        Key_Find: Qt.Key = ...  # 0x1000122
        Key_Undo: Qt.Key = ...  # 0x1000123
        Key_Redo: Qt.Key = ...  # 0x1000124
        Key_AltGr: Qt.Key = ...  # 0x1001103
        Key_Multi_key: Qt.Key = ...  # 0x1001120
        Key_Kanji: Qt.Key = ...  # 0x1001121
        Key_Muhenkan: Qt.Key = ...  # 0x1001122
        Key_Henkan: Qt.Key = ...  # 0x1001123
        Key_Romaji: Qt.Key = ...  # 0x1001124
        Key_Hiragana: Qt.Key = ...  # 0x1001125
        Key_Katakana: Qt.Key = ...  # 0x1001126
        Key_Hiragana_Katakana: Qt.Key = ...  # 0x1001127
        Key_Zenkaku: Qt.Key = ...  # 0x1001128
        Key_Hankaku: Qt.Key = ...  # 0x1001129
        Key_Zenkaku_Hankaku: Qt.Key = ...  # 0x100112a
        Key_Touroku: Qt.Key = ...  # 0x100112b
        Key_Massyo: Qt.Key = ...  # 0x100112c
        Key_Kana_Lock: Qt.Key = ...  # 0x100112d
        Key_Kana_Shift: Qt.Key = ...  # 0x100112e
        Key_Eisu_Shift: Qt.Key = ...  # 0x100112f
        Key_Eisu_toggle: Qt.Key = ...  # 0x1001130
        Key_Hangul: Qt.Key = ...  # 0x1001131
        Key_Hangul_Start: Qt.Key = ...  # 0x1001132
        Key_Hangul_End: Qt.Key = ...  # 0x1001133
        Key_Hangul_Hanja: Qt.Key = ...  # 0x1001134
        Key_Hangul_Jamo: Qt.Key = ...  # 0x1001135
        Key_Hangul_Romaja: Qt.Key = ...  # 0x1001136
        Key_Codeinput: Qt.Key = ...  # 0x1001137
        Key_Hangul_Jeonja: Qt.Key = ...  # 0x1001138
        Key_Hangul_Banja: Qt.Key = ...  # 0x1001139
        Key_Hangul_PreHanja: Qt.Key = ...  # 0x100113a
        Key_Hangul_PostHanja: Qt.Key = ...  # 0x100113b
        Key_SingleCandidate: Qt.Key = ...  # 0x100113c
        Key_MultipleCandidate: Qt.Key = ...  # 0x100113d
        Key_PreviousCandidate: Qt.Key = ...  # 0x100113e
        Key_Hangul_Special: Qt.Key = ...  # 0x100113f
        Key_Mode_switch: Qt.Key = ...  # 0x100117e
        Key_Dead_Grave: Qt.Key = ...  # 0x1001250
        Key_Dead_Acute: Qt.Key = ...  # 0x1001251
        Key_Dead_Circumflex: Qt.Key = ...  # 0x1001252
        Key_Dead_Tilde: Qt.Key = ...  # 0x1001253
        Key_Dead_Macron: Qt.Key = ...  # 0x1001254
        Key_Dead_Breve: Qt.Key = ...  # 0x1001255
        Key_Dead_Abovedot: Qt.Key = ...  # 0x1001256
        Key_Dead_Diaeresis: Qt.Key = ...  # 0x1001257
        Key_Dead_Abovering: Qt.Key = ...  # 0x1001258
        Key_Dead_Doubleacute: Qt.Key = ...  # 0x1001259
        Key_Dead_Caron: Qt.Key = ...  # 0x100125a
        Key_Dead_Cedilla: Qt.Key = ...  # 0x100125b
        Key_Dead_Ogonek: Qt.Key = ...  # 0x100125c
        Key_Dead_Iota: Qt.Key = ...  # 0x100125d
        Key_Dead_Voiced_Sound: Qt.Key = ...  # 0x100125e
        Key_Dead_Semivoiced_Sound: Qt.Key = ...  # 0x100125f
        Key_Dead_Belowdot: Qt.Key = ...  # 0x1001260
        Key_Dead_Hook: Qt.Key = ...  # 0x1001261
        Key_Dead_Horn: Qt.Key = ...  # 0x1001262
        Key_Dead_Stroke: Qt.Key = ...  # 0x1001263
        Key_Dead_Abovecomma: Qt.Key = ...  # 0x1001264
        Key_Dead_Abovereversedcomma: Qt.Key = ...  # 0x1001265
        Key_Dead_Doublegrave: Qt.Key = ...  # 0x1001266
        Key_Dead_Belowring: Qt.Key = ...  # 0x1001267
        Key_Dead_Belowmacron: Qt.Key = ...  # 0x1001268
        Key_Dead_Belowcircumflex: Qt.Key = ...  # 0x1001269
        Key_Dead_Belowtilde: Qt.Key = ...  # 0x100126a
        Key_Dead_Belowbreve: Qt.Key = ...  # 0x100126b
        Key_Dead_Belowdiaeresis: Qt.Key = ...  # 0x100126c
        Key_Dead_Invertedbreve: Qt.Key = ...  # 0x100126d
        Key_Dead_Belowcomma: Qt.Key = ...  # 0x100126e
        Key_Dead_Currency: Qt.Key = ...  # 0x100126f
        Key_Dead_a: Qt.Key = ...  # 0x1001280
        Key_Dead_A: Qt.Key = ...  # 0x1001281
        Key_Dead_e: Qt.Key = ...  # 0x1001282
        Key_Dead_E: Qt.Key = ...  # 0x1001283
        Key_Dead_i: Qt.Key = ...  # 0x1001284
        Key_Dead_I: Qt.Key = ...  # 0x1001285
        Key_Dead_o: Qt.Key = ...  # 0x1001286
        Key_Dead_O: Qt.Key = ...  # 0x1001287
        Key_Dead_u: Qt.Key = ...  # 0x1001288
        Key_Dead_U: Qt.Key = ...  # 0x1001289
        Key_Dead_Small_Schwa: Qt.Key = ...  # 0x100128a
        Key_Dead_Capital_Schwa: Qt.Key = ...  # 0x100128b
        Key_Dead_Greek: Qt.Key = ...  # 0x100128c
        Key_Dead_Lowline: Qt.Key = ...  # 0x1001290
        Key_Dead_Aboveverticalline: Qt.Key = ...  # 0x1001291
        Key_Dead_Belowverticalline: Qt.Key = ...  # 0x1001292
        Key_Dead_Longsolidusoverlay: Qt.Key = ...  # 0x1001293
        Key_MediaLast: Qt.Key = ...  # 0x100ffff
        Key_Select: Qt.Key = ...  # 0x1010000
        Key_Yes: Qt.Key = ...  # 0x1010001
        Key_No: Qt.Key = ...  # 0x1010002
        Key_Cancel: Qt.Key = ...  # 0x1020001
        Key_Printer: Qt.Key = ...  # 0x1020002
        Key_Execute: Qt.Key = ...  # 0x1020003
        Key_Sleep: Qt.Key = ...  # 0x1020004
        Key_Play: Qt.Key = ...  # 0x1020005
        Key_Zoom: Qt.Key = ...  # 0x1020006
        Key_Exit: Qt.Key = ...  # 0x102000a
        Key_Context1: Qt.Key = ...  # 0x1100000
        Key_Context2: Qt.Key = ...  # 0x1100001
        Key_Context3: Qt.Key = ...  # 0x1100002
        Key_Context4: Qt.Key = ...  # 0x1100003
        Key_Call: Qt.Key = ...  # 0x1100004
        Key_Hangup: Qt.Key = ...  # 0x1100005
        Key_Flip: Qt.Key = ...  # 0x1100006
        Key_ToggleCallHangup: Qt.Key = ...  # 0x1100007
        Key_VoiceDial: Qt.Key = ...  # 0x1100008
        Key_LastNumberRedial: Qt.Key = ...  # 0x1100009
        Key_Camera: Qt.Key = ...  # 0x1100020
        Key_CameraFocus: Qt.Key = ...  # 0x1100021
        Key_unknown: Qt.Key = ...  # 0x1ffffff
    class KeyboardModifier(Enum):

        KeyboardModifierMask: Qt.KeyboardModifier = ...  # -0x2000000
        NoModifier: Qt.KeyboardModifier = ...  # 0x0
        ShiftModifier: Qt.KeyboardModifier = ...  # 0x2000000
        ControlModifier: Qt.KeyboardModifier = ...  # 0x4000000
        AltModifier: Qt.KeyboardModifier = ...  # 0x8000000
        MetaModifier: Qt.KeyboardModifier = ...  # 0x10000000
        KeypadModifier: Qt.KeyboardModifier = ...  # 0x20000000
        GroupSwitchModifier: Qt.KeyboardModifier = ...  # 0x40000000
    class KeyboardModifiers(object): ...
    class LayoutDirection(Enum):

        LeftToRight: Qt.LayoutDirection = ...  # 0x0
        RightToLeft: Qt.LayoutDirection = ...  # 0x1
        LayoutDirectionAuto: Qt.LayoutDirection = ...  # 0x2
    class MaskMode(Enum):

        MaskInColor: Qt.MaskMode = ...  # 0x0
        MaskOutColor: Qt.MaskMode = ...  # 0x1
    class MatchFlag(Enum):

        MatchExactly: Qt.MatchFlag = ...  # 0x0
        MatchContains: Qt.MatchFlag = ...  # 0x1
        MatchStartsWith: Qt.MatchFlag = ...  # 0x2
        MatchEndsWith: Qt.MatchFlag = ...  # 0x3
        MatchRegularExpression: Qt.MatchFlag = ...  # 0x4
        MatchWildcard: Qt.MatchFlag = ...  # 0x5
        MatchFixedString: Qt.MatchFlag = ...  # 0x8
        MatchTypeMask: Qt.MatchFlag = ...  # 0xf
        MatchCaseSensitive: Qt.MatchFlag = ...  # 0x10
        MatchWrap: Qt.MatchFlag = ...  # 0x20
        MatchRecursive: Qt.MatchFlag = ...  # 0x40
    class MatchFlags(object): ...
    class Modifier(Enum):

        MODIFIER_MASK: Qt.Modifier = ...  # -0x2000000
        SHIFT: Qt.Modifier = ...  # 0x2000000
        CTRL: Qt.Modifier = ...  # 0x4000000
        ALT: Qt.Modifier = ...  # 0x8000000
        META: Qt.Modifier = ...  # 0x10000000
    class MouseButton(Enum):

        MouseButtonMask: Qt.MouseButton = ...  # -0x1
        NoButton: Qt.MouseButton = ...  # 0x0
        LeftButton: Qt.MouseButton = ...  # 0x1
        RightButton: Qt.MouseButton = ...  # 0x2
        MiddleButton: Qt.MouseButton = ...  # 0x4
        BackButton: Qt.MouseButton = ...  # 0x8
        ExtraButton1: Qt.MouseButton = ...  # 0x8
        XButton1: Qt.MouseButton = ...  # 0x8
        ExtraButton2: Qt.MouseButton = ...  # 0x10
        ForwardButton: Qt.MouseButton = ...  # 0x10
        XButton2: Qt.MouseButton = ...  # 0x10
        ExtraButton3: Qt.MouseButton = ...  # 0x20
        TaskButton: Qt.MouseButton = ...  # 0x20
        ExtraButton4: Qt.MouseButton = ...  # 0x40
        ExtraButton5: Qt.MouseButton = ...  # 0x80
        ExtraButton6: Qt.MouseButton = ...  # 0x100
        ExtraButton7: Qt.MouseButton = ...  # 0x200
        ExtraButton8: Qt.MouseButton = ...  # 0x400
        ExtraButton9: Qt.MouseButton = ...  # 0x800
        ExtraButton10: Qt.MouseButton = ...  # 0x1000
        ExtraButton11: Qt.MouseButton = ...  # 0x2000
        ExtraButton12: Qt.MouseButton = ...  # 0x4000
        ExtraButton13: Qt.MouseButton = ...  # 0x8000
        ExtraButton14: Qt.MouseButton = ...  # 0x10000
        ExtraButton15: Qt.MouseButton = ...  # 0x20000
        ExtraButton16: Qt.MouseButton = ...  # 0x40000
        ExtraButton17: Qt.MouseButton = ...  # 0x80000
        ExtraButton18: Qt.MouseButton = ...  # 0x100000
        ExtraButton19: Qt.MouseButton = ...  # 0x200000
        ExtraButton20: Qt.MouseButton = ...  # 0x400000
        ExtraButton21: Qt.MouseButton = ...  # 0x800000
        ExtraButton22: Qt.MouseButton = ...  # 0x1000000
        ExtraButton23: Qt.MouseButton = ...  # 0x2000000
        ExtraButton24: Qt.MouseButton = ...  # 0x4000000
        MaxMouseButton: Qt.MouseButton = ...  # 0x4000000
        AllButtons: Qt.MouseButton = ...  # 0x7ffffff
    class MouseButtons(object): ...
    class MouseEventFlag(Enum):

        NoMouseEventFlag: Qt.MouseEventFlag = ...  # 0x0
        MouseEventCreatedDoubleClick: Qt.MouseEventFlag = ...  # 0x1
        MouseEventFlagMask: Qt.MouseEventFlag = ...  # 0xff
    class MouseEventFlags(object): ...
    class MouseEventSource(Enum):

        MouseEventNotSynthesized: Qt.MouseEventSource = ...  # 0x0
        MouseEventSynthesizedBySystem: Qt.MouseEventSource = ...  # 0x1
        MouseEventSynthesizedByQt: Qt.MouseEventSource = ...  # 0x2
        MouseEventSynthesizedByApplication: Qt.MouseEventSource = ...  # 0x3
    class NativeGestureType(Enum):

        BeginNativeGesture: Qt.NativeGestureType = ...  # 0x0
        EndNativeGesture: Qt.NativeGestureType = ...  # 0x1
        PanNativeGesture: Qt.NativeGestureType = ...  # 0x2
        ZoomNativeGesture: Qt.NativeGestureType = ...  # 0x3
        SmartZoomNativeGesture: Qt.NativeGestureType = ...  # 0x4
        RotateNativeGesture: Qt.NativeGestureType = ...  # 0x5
        SwipeNativeGesture: Qt.NativeGestureType = ...  # 0x6
    class NavigationMode(Enum):

        NavigationModeNone: Qt.NavigationMode = ...  # 0x0
        NavigationModeKeypadTabOrder: Qt.NavigationMode = ...  # 0x1
        NavigationModeKeypadDirectional: Qt.NavigationMode = ...  # 0x2
        NavigationModeCursorAuto: Qt.NavigationMode = ...  # 0x3
        NavigationModeCursorForceVisible: Qt.NavigationMode = ...  # 0x4
    class Orientation(Enum):

        Horizontal: Qt.Orientation = ...  # 0x1
        Vertical: Qt.Orientation = ...  # 0x2
    class Orientations(object): ...
    class PenCapStyle(Enum):

        FlatCap: Qt.PenCapStyle = ...  # 0x0
        SquareCap: Qt.PenCapStyle = ...  # 0x10
        RoundCap: Qt.PenCapStyle = ...  # 0x20
        MPenCapStyle: Qt.PenCapStyle = ...  # 0x30
    class PenJoinStyle(Enum):

        MiterJoin: Qt.PenJoinStyle = ...  # 0x0
        BevelJoin: Qt.PenJoinStyle = ...  # 0x40
        RoundJoin: Qt.PenJoinStyle = ...  # 0x80
        SvgMiterJoin: Qt.PenJoinStyle = ...  # 0x100
        MPenJoinStyle: Qt.PenJoinStyle = ...  # 0x1c0
    class PenStyle(Enum):

        NoPen: Qt.PenStyle = ...  # 0x0
        SolidLine: Qt.PenStyle = ...  # 0x1
        DashLine: Qt.PenStyle = ...  # 0x2
        DotLine: Qt.PenStyle = ...  # 0x3
        DashDotLine: Qt.PenStyle = ...  # 0x4
        DashDotDotLine: Qt.PenStyle = ...  # 0x5
        CustomDashLine: Qt.PenStyle = ...  # 0x6
        MPenStyle: Qt.PenStyle = ...  # 0xf
    class ReturnByValueConstant(Enum):

        ReturnByValue: Qt.ReturnByValueConstant = ...  # 0x0
    class ScreenOrientation(Enum):

        PrimaryOrientation: Qt.ScreenOrientation = ...  # 0x0
        PortraitOrientation: Qt.ScreenOrientation = ...  # 0x1
        LandscapeOrientation: Qt.ScreenOrientation = ...  # 0x2
        InvertedPortraitOrientation: Qt.ScreenOrientation = ...  # 0x4
        InvertedLandscapeOrientation: Qt.ScreenOrientation = ...  # 0x8
    class ScreenOrientations(object): ...
    class ScrollBarPolicy(Enum):

        ScrollBarAsNeeded: Qt.ScrollBarPolicy = ...  # 0x0
        ScrollBarAlwaysOff: Qt.ScrollBarPolicy = ...  # 0x1
        ScrollBarAlwaysOn: Qt.ScrollBarPolicy = ...  # 0x2
    class ScrollPhase(Enum):

        NoScrollPhase: Qt.ScrollPhase = ...  # 0x0
        ScrollBegin: Qt.ScrollPhase = ...  # 0x1
        ScrollUpdate: Qt.ScrollPhase = ...  # 0x2
        ScrollEnd: Qt.ScrollPhase = ...  # 0x3
        ScrollMomentum: Qt.ScrollPhase = ...  # 0x4
    class ShortcutContext(Enum):

        WidgetShortcut: Qt.ShortcutContext = ...  # 0x0
        WindowShortcut: Qt.ShortcutContext = ...  # 0x1
        ApplicationShortcut: Qt.ShortcutContext = ...  # 0x2
        WidgetWithChildrenShortcut: Qt.ShortcutContext = ...  # 0x3
    class SizeHint(Enum):

        MinimumSize: Qt.SizeHint = ...  # 0x0
        PreferredSize: Qt.SizeHint = ...  # 0x1
        MaximumSize: Qt.SizeHint = ...  # 0x2
        MinimumDescent: Qt.SizeHint = ...  # 0x3
        NSizeHints: Qt.SizeHint = ...  # 0x4
    class SizeMode(Enum):

        AbsoluteSize: Qt.SizeMode = ...  # 0x0
        RelativeSize: Qt.SizeMode = ...  # 0x1
    class SortOrder(Enum):

        AscendingOrder: Qt.SortOrder = ...  # 0x0
        DescendingOrder: Qt.SortOrder = ...  # 0x1
    class SplitBehavior(object): ...
    class SplitBehaviorFlags(Enum):

        KeepEmptyParts: Qt.SplitBehaviorFlags = ...  # 0x0
        SkipEmptyParts: Qt.SplitBehaviorFlags = ...  # 0x1
    class TabFocusBehavior(Enum):

        NoTabFocus: Qt.TabFocusBehavior = ...  # 0x0
        TabFocusTextControls: Qt.TabFocusBehavior = ...  # 0x1
        TabFocusListControls: Qt.TabFocusBehavior = ...  # 0x2
        TabFocusAllControls: Qt.TabFocusBehavior = ...  # 0xff
    class TextElideMode(Enum):

        ElideLeft: Qt.TextElideMode = ...  # 0x0
        ElideRight: Qt.TextElideMode = ...  # 0x1
        ElideMiddle: Qt.TextElideMode = ...  # 0x2
        ElideNone: Qt.TextElideMode = ...  # 0x3
    class TextFlag(Enum):

        TextSingleLine: Qt.TextFlag = ...  # 0x100
        TextDontClip: Qt.TextFlag = ...  # 0x200
        TextExpandTabs: Qt.TextFlag = ...  # 0x400
        TextShowMnemonic: Qt.TextFlag = ...  # 0x800
        TextWordWrap: Qt.TextFlag = ...  # 0x1000
        TextWrapAnywhere: Qt.TextFlag = ...  # 0x2000
        TextDontPrint: Qt.TextFlag = ...  # 0x4000
        TextHideMnemonic: Qt.TextFlag = ...  # 0x8000
        TextJustificationForced: Qt.TextFlag = ...  # 0x10000
        TextForceLeftToRight: Qt.TextFlag = ...  # 0x20000
        TextForceRightToLeft: Qt.TextFlag = ...  # 0x40000
        TextLongestVariant: Qt.TextFlag = ...  # 0x80000
        TextIncludeTrailingSpaces: Qt.TextFlag = ...  # 0x8000000
    class TextFormat(Enum):

        PlainText: Qt.TextFormat = ...  # 0x0
        RichText: Qt.TextFormat = ...  # 0x1
        AutoText: Qt.TextFormat = ...  # 0x2
        MarkdownText: Qt.TextFormat = ...  # 0x3
    class TextInteractionFlag(Enum):

        NoTextInteraction: Qt.TextInteractionFlag = ...  # 0x0
        TextSelectableByMouse: Qt.TextInteractionFlag = ...  # 0x1
        TextSelectableByKeyboard: Qt.TextInteractionFlag = ...  # 0x2
        LinksAccessibleByMouse: Qt.TextInteractionFlag = ...  # 0x4
        LinksAccessibleByKeyboard: Qt.TextInteractionFlag = ...  # 0x8
        TextBrowserInteraction: Qt.TextInteractionFlag = ...  # 0xd
        TextEditable: Qt.TextInteractionFlag = ...  # 0x10
        TextEditorInteraction: Qt.TextInteractionFlag = ...  # 0x13
    class TextInteractionFlags(object): ...
    class TileRule(Enum):

        StretchTile: Qt.TileRule = ...  # 0x0
        RepeatTile: Qt.TileRule = ...  # 0x1
        RoundTile: Qt.TileRule = ...  # 0x2
    class TimeSpec(Enum):

        LocalTime: Qt.TimeSpec = ...  # 0x0
        UTC: Qt.TimeSpec = ...  # 0x1
        OffsetFromUTC: Qt.TimeSpec = ...  # 0x2
        TimeZone: Qt.TimeSpec = ...  # 0x3
    class TimerType(Enum):

        PreciseTimer: Qt.TimerType = ...  # 0x0
        CoarseTimer: Qt.TimerType = ...  # 0x1
        VeryCoarseTimer: Qt.TimerType = ...  # 0x2
    class ToolBarArea(Enum):

        NoToolBarArea: Qt.ToolBarArea = ...  # 0x0
        LeftToolBarArea: Qt.ToolBarArea = ...  # 0x1
        RightToolBarArea: Qt.ToolBarArea = ...  # 0x2
        TopToolBarArea: Qt.ToolBarArea = ...  # 0x4
        BottomToolBarArea: Qt.ToolBarArea = ...  # 0x8
        AllToolBarAreas: Qt.ToolBarArea = ...  # 0xf
        ToolBarArea_Mask: Qt.ToolBarArea = ...  # 0xf
    class ToolBarAreaSizes(Enum):

        NToolBarAreas: Qt.ToolBarAreaSizes = ...  # 0x4
    class ToolBarAreas(object): ...
    class ToolButtonStyle(Enum):

        ToolButtonIconOnly: Qt.ToolButtonStyle = ...  # 0x0
        ToolButtonTextOnly: Qt.ToolButtonStyle = ...  # 0x1
        ToolButtonTextBesideIcon: Qt.ToolButtonStyle = ...  # 0x2
        ToolButtonTextUnderIcon: Qt.ToolButtonStyle = ...  # 0x3
        ToolButtonFollowStyle: Qt.ToolButtonStyle = ...  # 0x4
    class TouchPointState(Enum):

        TouchPointUnknownState: Qt.TouchPointState = ...  # 0x0
        TouchPointPressed: Qt.TouchPointState = ...  # 0x1
        TouchPointMoved: Qt.TouchPointState = ...  # 0x2
        TouchPointStationary: Qt.TouchPointState = ...  # 0x4
        TouchPointReleased: Qt.TouchPointState = ...  # 0x8
    class TouchPointStates(object): ...
    class TransformationMode(Enum):

        FastTransformation: Qt.TransformationMode = ...  # 0x0
        SmoothTransformation: Qt.TransformationMode = ...  # 0x1
    class UIEffect(Enum):

        UI_General: Qt.UIEffect = ...  # 0x0
        UI_AnimateMenu: Qt.UIEffect = ...  # 0x1
        UI_FadeMenu: Qt.UIEffect = ...  # 0x2
        UI_AnimateCombo: Qt.UIEffect = ...  # 0x3
        UI_AnimateTooltip: Qt.UIEffect = ...  # 0x4
        UI_FadeTooltip: Qt.UIEffect = ...  # 0x5
        UI_AnimateToolBox: Qt.UIEffect = ...  # 0x6
    class WhiteSpaceMode(Enum):

        WhiteSpaceModeUndefined: Qt.WhiteSpaceMode = ...  # -0x1
        WhiteSpaceNormal: Qt.WhiteSpaceMode = ...  # 0x0
        WhiteSpacePre: Qt.WhiteSpaceMode = ...  # 0x1
        WhiteSpaceNoWrap: Qt.WhiteSpaceMode = ...  # 0x2
    class WidgetAttribute(Enum):

        WA_Disabled: Qt.WidgetAttribute = ...  # 0x0
        WA_UnderMouse: Qt.WidgetAttribute = ...  # 0x1
        WA_MouseTracking: Qt.WidgetAttribute = ...  # 0x2
        WA_OpaquePaintEvent: Qt.WidgetAttribute = ...  # 0x4
        WA_StaticContents: Qt.WidgetAttribute = ...  # 0x5
        WA_LaidOut: Qt.WidgetAttribute = ...  # 0x7
        WA_PaintOnScreen: Qt.WidgetAttribute = ...  # 0x8
        WA_NoSystemBackground: Qt.WidgetAttribute = ...  # 0x9
        WA_UpdatesDisabled: Qt.WidgetAttribute = ...  # 0xa
        WA_Mapped: Qt.WidgetAttribute = ...  # 0xb
        WA_InputMethodEnabled: Qt.WidgetAttribute = ...  # 0xe
        WA_WState_Visible: Qt.WidgetAttribute = ...  # 0xf
        WA_WState_Hidden: Qt.WidgetAttribute = ...  # 0x10
        WA_ForceDisabled: Qt.WidgetAttribute = ...  # 0x20
        WA_KeyCompression: Qt.WidgetAttribute = ...  # 0x21
        WA_PendingMoveEvent: Qt.WidgetAttribute = ...  # 0x22
        WA_PendingResizeEvent: Qt.WidgetAttribute = ...  # 0x23
        WA_SetPalette: Qt.WidgetAttribute = ...  # 0x24
        WA_SetFont: Qt.WidgetAttribute = ...  # 0x25
        WA_SetCursor: Qt.WidgetAttribute = ...  # 0x26
        WA_NoChildEventsFromChildren: Qt.WidgetAttribute = ...  # 0x27
        WA_WindowModified: Qt.WidgetAttribute = ...  # 0x29
        WA_Resized: Qt.WidgetAttribute = ...  # 0x2a
        WA_Moved: Qt.WidgetAttribute = ...  # 0x2b
        WA_PendingUpdate: Qt.WidgetAttribute = ...  # 0x2c
        WA_InvalidSize: Qt.WidgetAttribute = ...  # 0x2d
        WA_CustomWhatsThis: Qt.WidgetAttribute = ...  # 0x2f
        WA_LayoutOnEntireRect: Qt.WidgetAttribute = ...  # 0x30
        WA_OutsideWSRange: Qt.WidgetAttribute = ...  # 0x31
        WA_GrabbedShortcut: Qt.WidgetAttribute = ...  # 0x32
        WA_TransparentForMouseEvents: Qt.WidgetAttribute = ...  # 0x33
        WA_PaintUnclipped: Qt.WidgetAttribute = ...  # 0x34
        WA_SetWindowIcon: Qt.WidgetAttribute = ...  # 0x35
        WA_NoMouseReplay: Qt.WidgetAttribute = ...  # 0x36
        WA_DeleteOnClose: Qt.WidgetAttribute = ...  # 0x37
        WA_RightToLeft: Qt.WidgetAttribute = ...  # 0x38
        WA_SetLayoutDirection: Qt.WidgetAttribute = ...  # 0x39
        WA_NoChildEventsForParent: Qt.WidgetAttribute = ...  # 0x3a
        WA_ForceUpdatesDisabled: Qt.WidgetAttribute = ...  # 0x3b
        WA_WState_Created: Qt.WidgetAttribute = ...  # 0x3c
        WA_WState_CompressKeys: Qt.WidgetAttribute = ...  # 0x3d
        WA_WState_InPaintEvent: Qt.WidgetAttribute = ...  # 0x3e
        WA_WState_Reparented: Qt.WidgetAttribute = ...  # 0x3f
        WA_WState_ConfigPending: Qt.WidgetAttribute = ...  # 0x40
        WA_WState_Polished: Qt.WidgetAttribute = ...  # 0x42
        WA_WState_OwnSizePolicy: Qt.WidgetAttribute = ...  # 0x44
        WA_WState_ExplicitShowHide: Qt.WidgetAttribute = ...  # 0x45
        WA_ShowModal: Qt.WidgetAttribute = ...  # 0x46
        WA_MouseNoMask: Qt.WidgetAttribute = ...  # 0x47
        WA_NoMousePropagation: Qt.WidgetAttribute = ...  # 0x49
        WA_Hover: Qt.WidgetAttribute = ...  # 0x4a
        WA_InputMethodTransparent: Qt.WidgetAttribute = ...  # 0x4b
        WA_QuitOnClose: Qt.WidgetAttribute = ...  # 0x4c
        WA_KeyboardFocusChange: Qt.WidgetAttribute = ...  # 0x4d
        WA_AcceptDrops: Qt.WidgetAttribute = ...  # 0x4e
        WA_DropSiteRegistered: Qt.WidgetAttribute = ...  # 0x4f
        WA_WindowPropagation: Qt.WidgetAttribute = ...  # 0x50
        WA_NoX11EventCompression: Qt.WidgetAttribute = ...  # 0x51
        WA_TintedBackground: Qt.WidgetAttribute = ...  # 0x52
        WA_X11OpenGLOverlay: Qt.WidgetAttribute = ...  # 0x53
        WA_AlwaysShowToolTips: Qt.WidgetAttribute = ...  # 0x54
        WA_MacOpaqueSizeGrip: Qt.WidgetAttribute = ...  # 0x55
        WA_SetStyle: Qt.WidgetAttribute = ...  # 0x56
        WA_SetLocale: Qt.WidgetAttribute = ...  # 0x57
        WA_MacShowFocusRect: Qt.WidgetAttribute = ...  # 0x58
        WA_MacNormalSize: Qt.WidgetAttribute = ...  # 0x59
        WA_MacSmallSize: Qt.WidgetAttribute = ...  # 0x5a
        WA_MacMiniSize: Qt.WidgetAttribute = ...  # 0x5b
        WA_LayoutUsesWidgetRect: Qt.WidgetAttribute = ...  # 0x5c
        WA_StyledBackground: Qt.WidgetAttribute = ...  # 0x5d
        WA_CanHostQMdiSubWindowTitleBar: Qt.WidgetAttribute = ...  # 0x5f
        WA_MacAlwaysShowToolWindow: Qt.WidgetAttribute = ...  # 0x60
        WA_StyleSheet: Qt.WidgetAttribute = ...  # 0x61
        WA_ShowWithoutActivating: Qt.WidgetAttribute = ...  # 0x62
        WA_X11BypassTransientForHint: Qt.WidgetAttribute = ...  # 0x63
        WA_NativeWindow: Qt.WidgetAttribute = ...  # 0x64
        WA_DontCreateNativeAncestors: Qt.WidgetAttribute = ...  # 0x65
        WA_DontShowOnScreen: Qt.WidgetAttribute = ...  # 0x67
        WA_X11NetWmWindowTypeDesktop: Qt.WidgetAttribute = ...  # 0x68
        WA_X11NetWmWindowTypeDock: Qt.WidgetAttribute = ...  # 0x69
        WA_X11NetWmWindowTypeToolBar: Qt.WidgetAttribute = ...  # 0x6a
        WA_X11NetWmWindowTypeMenu: Qt.WidgetAttribute = ...  # 0x6b
        WA_X11NetWmWindowTypeUtility: Qt.WidgetAttribute = ...  # 0x6c
        WA_X11NetWmWindowTypeSplash: Qt.WidgetAttribute = ...  # 0x6d
        WA_X11NetWmWindowTypeDialog: Qt.WidgetAttribute = ...  # 0x6e
        WA_X11NetWmWindowTypeDropDownMenu: Qt.WidgetAttribute = ...  # 0x6f
        WA_X11NetWmWindowTypePopupMenu: Qt.WidgetAttribute = ...  # 0x70
        WA_X11NetWmWindowTypeToolTip: Qt.WidgetAttribute = ...  # 0x71
        WA_X11NetWmWindowTypeNotification: Qt.WidgetAttribute = ...  # 0x72
        WA_X11NetWmWindowTypeCombo: Qt.WidgetAttribute = ...  # 0x73
        WA_X11NetWmWindowTypeDND: Qt.WidgetAttribute = ...  # 0x74
        WA_SetWindowModality: Qt.WidgetAttribute = ...  # 0x76
        WA_WState_WindowOpacitySet: Qt.WidgetAttribute = ...  # 0x77
        WA_TranslucentBackground: Qt.WidgetAttribute = ...  # 0x78
        WA_AcceptTouchEvents: Qt.WidgetAttribute = ...  # 0x79
        WA_WState_AcceptedTouchBeginEvent: Qt.WidgetAttribute = ...  # 0x7a
        WA_TouchPadAcceptSingleTouchEvents: Qt.WidgetAttribute = ...  # 0x7b
        WA_X11DoNotAcceptFocus: Qt.WidgetAttribute = ...  # 0x7e
        WA_AlwaysStackOnTop: Qt.WidgetAttribute = ...  # 0x80
        WA_TabletTracking: Qt.WidgetAttribute = ...  # 0x81
        WA_ContentsMarginsRespectsSafeArea: Qt.WidgetAttribute = ...  # 0x82
        WA_StyleSheetTarget: Qt.WidgetAttribute = ...  # 0x83
        WA_AttributeCount: Qt.WidgetAttribute = ...  # 0x84
    class WindowFlags(object): ...
    class WindowFrameSection(Enum):

        NoSection: Qt.WindowFrameSection = ...  # 0x0
        LeftSection: Qt.WindowFrameSection = ...  # 0x1
        TopLeftSection: Qt.WindowFrameSection = ...  # 0x2
        TopSection: Qt.WindowFrameSection = ...  # 0x3
        TopRightSection: Qt.WindowFrameSection = ...  # 0x4
        RightSection: Qt.WindowFrameSection = ...  # 0x5
        BottomRightSection: Qt.WindowFrameSection = ...  # 0x6
        BottomSection: Qt.WindowFrameSection = ...  # 0x7
        BottomLeftSection: Qt.WindowFrameSection = ...  # 0x8
        TitleBarArea: Qt.WindowFrameSection = ...  # 0x9
    class WindowModality(Enum):

        NonModal: Qt.WindowModality = ...  # 0x0
        WindowModal: Qt.WindowModality = ...  # 0x1
        ApplicationModal: Qt.WindowModality = ...  # 0x2
    class WindowState(Enum):

        WindowNoState: Qt.WindowState = ...  # 0x0
        WindowMinimized: Qt.WindowState = ...  # 0x1
        WindowMaximized: Qt.WindowState = ...  # 0x2
        WindowFullScreen: Qt.WindowState = ...  # 0x4
        WindowActive: Qt.WindowState = ...  # 0x8
    class WindowStates(object): ...
    class WindowType(Enum):

        WindowFullscreenButtonHint: Qt.WindowType = ...  # -0x80000000
        Widget: Qt.WindowType = ...  # 0x0
        Window: Qt.WindowType = ...  # 0x1
        Dialog: Qt.WindowType = ...  # 0x3
        Sheet: Qt.WindowType = ...  # 0x5
        Drawer: Qt.WindowType = ...  # 0x7
        Popup: Qt.WindowType = ...  # 0x9
        Tool: Qt.WindowType = ...  # 0xb
        ToolTip: Qt.WindowType = ...  # 0xd
        SplashScreen: Qt.WindowType = ...  # 0xf
        Desktop: Qt.WindowType = ...  # 0x11
        SubWindow: Qt.WindowType = ...  # 0x12
        ForeignWindow: Qt.WindowType = ...  # 0x21
        CoverWindow: Qt.WindowType = ...  # 0x41
        WindowType_Mask: Qt.WindowType = ...  # 0xff
        MSWindowsFixedSizeDialogHint: Qt.WindowType = ...  # 0x100
        MSWindowsOwnDC: Qt.WindowType = ...  # 0x200
        BypassWindowManagerHint: Qt.WindowType = ...  # 0x400
        X11BypassWindowManagerHint: Qt.WindowType = ...  # 0x400
        FramelessWindowHint: Qt.WindowType = ...  # 0x800
        WindowTitleHint: Qt.WindowType = ...  # 0x1000
        WindowSystemMenuHint: Qt.WindowType = ...  # 0x2000
        WindowMinimizeButtonHint: Qt.WindowType = ...  # 0x4000
        WindowMaximizeButtonHint: Qt.WindowType = ...  # 0x8000
        WindowMinMaxButtonsHint: Qt.WindowType = ...  # 0xc000
        WindowContextHelpButtonHint: Qt.WindowType = ...  # 0x10000
        WindowShadeButtonHint: Qt.WindowType = ...  # 0x20000
        WindowStaysOnTopHint: Qt.WindowType = ...  # 0x40000
        WindowTransparentForInput: Qt.WindowType = ...  # 0x80000
        WindowOverridesSystemGestures: Qt.WindowType = ...  # 0x100000
        WindowDoesNotAcceptFocus: Qt.WindowType = ...  # 0x200000
        MaximizeUsingFullscreenGeometryHint: Qt.WindowType = ...  # 0x400000
        CustomizeWindowHint: Qt.WindowType = ...  # 0x2000000
        WindowStaysOnBottomHint: Qt.WindowType = ...  # 0x4000000
        WindowCloseButtonHint: Qt.WindowType = ...  # 0x8000000
        MacWindowToolBarButtonHint: Qt.WindowType = ...  # 0x10000000
        BypassGraphicsProxyWidget: Qt.WindowType = ...  # 0x20000000
        NoDropShadowWindowHint: Qt.WindowType = ...  # 0x40000000
        def __or__(self, arg_2: Qt.WindowType) -> Qt.WindowType: ...
        def __ior__(self, arg_2: Qt.WindowType) -> Qt.WindowType: ...

    @staticmethod
    def beginPropertyUpdateGroup() -> None: ...
    @staticmethod
    def bin(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def bom(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def center(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def dec(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def endPropertyUpdateGroup() -> None: ...
    @staticmethod
    def endl(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def fixed(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def flush(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def forcepoint(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def forcesign(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def hex(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def left(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def lowercasebase(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def lowercasedigits(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def noforcepoint(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def noforcesign(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def noshowbase(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def oct(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def reset(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def right(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def scientific(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def showbase(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def uppercasebase(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def uppercasedigits(s: QTextStream) -> QTextStream: ...
    @staticmethod
    def ws(s: QTextStream) -> QTextStream: ...

class QtMsgType(Enum):

    QtDebugMsg: QtMsgType = ...  # 0x0
    QtWarningMsg: QtMsgType = ...  # 0x1
    QtCriticalMsg: QtMsgType = ...  # 0x2
    QtSystemMsg: QtMsgType = ...  # 0x2
    QtFatalMsg: QtMsgType = ...  # 0x3
    QtInfoMsg: QtMsgType = ...  # 0x4

class Signal(object):
    def connect(self, slot: object, type: Optional[type] = ...) -> None: ...
    def disconnect(self, slot: object = ...) -> None: ...
    def emit(self, *args: Any) -> None: ...
    def __init__(
        self, *types: type, name: Optional[str] = ..., arguments: Optional[str] = ...
    ) -> None: ...

class SignalInstance(object):
    def connect(self, slot: object, type: Optional[type] = ...) -> None: ...
    def disconnect(self, slot: object = ...) -> None: ...
    def emit(self, *args: Any) -> None: ...

class Slot(object):
    def __init__(
        self, *types: type, name: Optional[str] = ..., result: Optional[str] = ...
    ) -> None: ...
    def __call__(self, function: Callable) -> Any: ...

def QEnum(arg__1: object) -> object: ...
def QFlag(arg__1: object) -> object: ...
def QT_TRANSLATE_NOOP(arg__1: object, arg__2: object) -> object: ...
def QT_TRANSLATE_NOOP3(arg__1: object, arg__2: object, arg__3: object) -> object: ...
def QT_TRANSLATE_NOOP_UTF8(arg__1: object) -> object: ...
def QT_TR_NOOP(arg__1: object) -> object: ...
def QT_TR_NOOP_UTF8(arg__1: object) -> object: ...
def SIGNAL(arg__1: bytes) -> str: ...
def SLOT(arg__1: bytes) -> str: ...
def __init_feature__() -> None: ...
def __moduleShutdown() -> None: ...
def qAbs(arg__1: float) -> float: ...
def qAddPostRoutine(arg__1: object) -> None: ...
@overload
def qCompress(data: Union[QByteArray, bytes], compressionLevel: int = ...) -> QByteArray: ...
@overload
def qCompress(data: bytes, nbytes: int, compressionLevel: int = ...) -> QByteArray: ...
def qCritical(arg__1: bytes) -> None: ...
def qDebug(arg__1: bytes) -> None: ...
def qFastCos(x: float) -> float: ...
def qFastSin(x: float) -> float: ...
def qFatal(arg__1: bytes) -> None: ...
def qFormatLogMessage(type: QtMsgType, context: QMessageLogContext, buf: str) -> str: ...
def qFuzzyCompare(p1: float, p2: float) -> bool: ...
def qFuzzyIsNull(d: float) -> bool: ...
def qInstallMessageHandler(arg__1: object) -> object: ...
def qIsFinite(d: float) -> bool: ...
def qIsInf(d: float) -> bool: ...
def qIsNaN(d: float) -> bool: ...
def qIsNull(d: float) -> bool: ...
def qRegisterResourceData(arg__1: int, arg__2: bytes, arg__3: bytes, arg__4: bytes) -> bool: ...
def qSetMessagePattern(messagePattern: str) -> None: ...
@overload
def qUncompress(data: Union[QByteArray, bytes]) -> QByteArray: ...
@overload
def qUncompress(data: bytes, nbytes: int) -> QByteArray: ...
def qUnregisterResourceData(arg__1: int, arg__2: bytes, arg__3: bytes, arg__4: bytes) -> bool: ...
def qVersion() -> bytes: ...
def qWarning(arg__1: bytes) -> None: ...
def qtTrId(id: bytes, n: int = ...) -> str: ...

# eof
