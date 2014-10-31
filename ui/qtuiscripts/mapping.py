import os
import sys
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import sip
import CryRigging
import CryCore
'''
Independent mapping for two lists
returning a list containing 2 lists

if mapper is closed, latest list update will be sent
'''

def getMayaWindow():
	#'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

uiFile = (os.path.dirname(str(__file__)) + '/mapping.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class Mapping(base_class, form_class):
	def __init__(self,parent=getMayaWindow(), sourceList=[], targetList=[], isChild=False, shortNames=True, cutNamespaces=True, checkNodesExistence=False):
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		self.setEnabled(1)
		self.lists = [sourceList,targetList]
		self.aSrcSel = []
		self.aTgtSel = []
		self.listWidgets = [self.lwSource, self.lwTarget]
		
		self.cbShortNames.setCheckState = shortNames
		self.cbCutNamespaces.setCheckState = cutNamespaces
		
		self.__makeListsSameSize()
		self.__fillList(side=0)
		self.__fillList(side=1)
		
		self.result = None
		
		self.connect(self.btnOK, QtCore.SIGNAL("clicked()"), self.__clickedOK)
		self.connect(self.btnSourceAdd, QtCore.SIGNAL("clicked()"), self.__addNode_src)
		self.connect(self.btnSourceRemove, QtCore.SIGNAL("clicked()"), self.__removeNode_src)
		self.connect(self.btnTargetAdd, QtCore.SIGNAL("clicked()"), self.__addNode_tgt)
		self.connect(self.btnTargetRemove, QtCore.SIGNAL("clicked()"), self.__removeNode_tgt)
		self.connect(self.cbCutNamespaces, QtCore.SIGNAL("clicked()"), self.__cutNameSpacesToggled)
		self.connect(self.cbShortNames, QtCore.SIGNAL("clicked()"), self.__shortNamesToggled)
		
		self.connect(self.btnTEST, QtCore.SIGNAL("clicked()"), self.__testme)
		
	def __makeListsSameSize(self):
		
		lenA = len(self.lists[0])
		lenB = len(self.lists[1])
		
		
		if (lenA < lenB):
			diff = lenB - lenA
			for i in range(0,diff):
				self.lists[0].append('')
		else:
			diff = lenA - lenB
			for i in range(0,diff):
				self.lists[1].append('')

	def __cutNameSpacesToggled(self):
		self.__updateData()
		self.__fillList(side=0)
		self.__fillList(side=1)
		
	def __shortNamesToggled(self):
		self.__updateData()
		self.__fillList(side=0)
		self.__fillList(side=1)
		
	def __getFinalName(self,list=[]):
		cutNameSpaces = self.cbCutNamespaces.isChecked()
		shortNames = self.cbShortNames.isChecked()
		listShort = []
		tokens = []
		finalName = ''
		for obj in list:
			finalName = ''
			if (cutNameSpaces):
				if (shortNames):
					finalName = obj.split('|')[-1].split(':')[-1]
				else:
					tokens = obj.split('|')
					if (len(tokens) > 1):
						for x in tokens:
							if (x != ''):
								finalName =  finalName + ('|'+x.split(':')[-1])
					else:
						finalName = obj.split(':')[-1]
			else:
				if (shortNames):
					finalName = obj.split('|')[-1]
				else:
					finalName = obj
			listShort.append(finalName)
		return listShort
	
	def __fillList(self,side=None,clear=True,list=None):
		lw = None
		listShort = []
		lw = self.listWidgets[side]
		if (list == None):
			list = self.lists[side]
		else:
			self.lists[side] = list
		listShort = self.__getFinalName(list=list)
		
		if (lw!=None):
			if clear:
				lw.clear()
			for x in range(0,len(listShort)):
				lw.addItem(listShort[x])
				lw.item(x).setToolTip(list[x])
				
	def __testme(self):
		print "this button is just temporary to test functions"
	
	def __addNode_tgt(self):
		self.__updateData()
		self.__addNode(side=1)
		
	def __removeNode_tgt(self):
		self.__removeNode(side=1)
		
	def __addNode_src(self):
		self.__updateData()
		self.__addNode(side=0)
		
	def __removeNode_src(self):
		self.__removeNode(side=0)
		
	def __addNode(self,side=None):
		nodes = cmds.ls(sl=1,l=1)
		nodes = [str(n) for n in nodes]
		list = self.lists[side].extend(nodes)
		self.__fillList(side=side,list=list)
		
	def __removeNode(self,side=None):
		lw = None
		self.__updateData()
		
		lw = self.listWidgets[side]
		list = self.lists[side]
		
		currentItem = None
		for i in reversed(range(0,lw.count())):
			currentItem = lw.item(i)
			if lw.isItemSelected(currentItem):
				list.pop(i)
		
		self.__fillList(side=side,list=list)
	
	def __createResult(self):
		#finalMapping = dict(zip(self.lists[0],self.lists[1]))
		self.result = self.lists
		
	def __clickedOK(self):
		self.__updateData()
		self.__createResult()
		self.done(0)
		
	def __updateData(self):
		# updating the lists according to the QListWidget entries
		self.lists[0] = self.__getListEntries(side=0)
		self.lists[1] = self.__getListEntries(side=1)
		self.__makeListsSameSize()
		
	def __getListEntries(self,side=None):
		theList = []
		lw = None
		lw = self.listWidgets[side]
		
		if lw:
			for i in range(0,lw.count()):
				theList.append(str(lw.item(i).toolTip()))
		return theList
	
	'''
	# old method when NOT using exec_()
	def sendDataToParent(self,data=[]):
		self.parentWidget().doneMapping(data)
	'''
		
def show(parent=None, sourceList=[], targetList=[], mappingFile=None):
	isChild = False
	if parent:
		isChild = True
	newMapping = Mapping(parent=parent, sourceList=sourceList, targetList=targetList, isChild=isChild)
	newMapping.setWindowModality(0)
	newMapping.setModal (False)
	newMapping.exec_()
	return newMapping.result