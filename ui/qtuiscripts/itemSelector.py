
from os import path
from PyQt4 import QtGui, QtCore, uic

uiFile = (path.dirname(str(__file__)) + '/itemSelector.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class itemSelect(base_class, form_class):
	def __init__(self, list):
		super(base_class, self).__init__(None)
		self.list = list
		self.setupUi(self)
		self.connect(self.getItemsBTN, QtCore.SIGNAL("clicked()"), self.getItemsFn)
		self.connect(self.filterEDT, QtCore.SIGNAL("textChanged(QString)"), self.rebuildList)
		self.result = None
		self.rebuildList()

	def rebuildList(self):
		self.itemList.clear()
		for item in self.list:
			filterTxt = str(self.filterEDT.text())
			if filterTxt == '':
				self.itemList.addItem(str(item))
			else:
				if filterTxt in str(item):
					self.itemList.addItem(str(item))
	
	def getItemsFn(self):
		self.result = []
		for index in xrange(self.itemList.count()):
			widItem = self.itemList.item(index)
			if widItem.isSelected(): self.result.append(str(widItem.text()))
		self.close()

def show(list):
	items = itemSelect(list)
	items.exec_()
	return items.result