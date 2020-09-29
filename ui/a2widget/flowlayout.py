"""
So far just the bugged flow layout example from the PySide2 demos.
"""

from PySide2 import QtCore, QtWidgets


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        self.item_list = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.do_layout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(self.contentsMargins().top() + self.contentsMargins().bottom(),
                             self.contentsMargins().left() + self.contentsMargins().right())
        return size

    def do_layout(self, rect=None, test_only=False):
        if rect is None:
            rect = self.geometry()
            print('rect: %s' % rect)

        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        lineHeight = 0

        for item in self.item_list:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() - self.contentsMargins().right() and lineHeight > 0:
                x = rect.x() + self.contentsMargins().left()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not test_only:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + self.contentsMargins().bottom()

    def set_marging(self, this):
        self.setContentsMargins(this, this, this, this)

    def set_spacing(self, this):
        self.setSpacing(this)


if __name__ == '__main__':
    from a2widget.demo import flowlayout_demo
    flowlayout_demo.show()
