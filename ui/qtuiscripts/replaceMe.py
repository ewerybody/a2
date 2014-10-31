import maya.cmds as cmds
import os, sip
import maya.OpenMaya as om
import maya.OpenMayaUI as mui
from PyQt4 import QtGui, QtCore, uic

def getMayaWindow():
	#'Get the maya main window as a QMainWindow instance'	
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

uiPath = (os.path.dirname(str(__file__)) + '/replaceMe.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiPath)

class ReplaceMe(base_class, form_class):
	def __init__(self, parent= getMayaWindow()):
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		
		self.connect(self.renameBTN, QtCore.SIGNAL("clicked()"), self.renameFn)
		self.connect(self.testBTN, QtCore.SIGNAL("clicked()"), self.testFn)
		self.connect(self.getNameBTN, QtCore.SIGNAL("clicked()"), self.getNameFn)
		
	def renameFn(self, test=False):
		nodes = self.getSelection()
		n = 0
		try:
			cmds.undoInfo(openChunk=True)
			for obj in nodes:
				if obj.hasFn(om.MFn.kDagNode):
					dag = om.MFnDagNode(obj)
					obj = dag.fullPathName()
				else:
					dg = om.MFnDependencyNode(obj)
					obj = dg.name()
				name = obj.split('|')[-1]
				#replace
				if self.replaceTXT.text() == '*': name = self.withTXT.text()
				elif self.replaceTXT.text() != '': name = name.replace(self.replaceTXT.text(), self.withTXT.text())
				#delete first
				if self.deleteFirstSPN.value() != 0: name = name[self.deleteFirstSPN.value():-1]
				#delete last
				if self.deleteLastSPN.value() != 0: name = name[0:(len(name) - self.deleteLastSPN.value())]
				#pre/suffix
				if self.prefixTXT != '': name = (self.prefixTXT.text() + name)
				if self.suffixTXT != '': name = (name + self.suffixTXT.text())
				#numbering
				if self.numCHK.isChecked() == True:
						name += '0' + str(int(self.numEDT.text()) + n)
						n += 1
				
				if name != obj.split('|')[-1]:
					#rename or print
					if test == True: print(name)
					else:
						cmds.rename(obj, str(name))
						print(obj.split('|')[-1] + ' renamed to ' + name.split('|')[-1])
		finally:
			cmds.undoInfo(closeChunk=True)
	
	def testFn(self):
		self.renameFn(test=True)
	
	def getSelection(self):
		nodes = []
		sel = om.MSelectionList()
		om.MGlobal.getActiveSelectionList(sel)

		for i in range(0,sel.length()):
			obj = om.MObject()
			sel.getDependNode(i, obj)
			nodes.append(obj)
		return nodes
	
	def getNameFn(self):
		self.replaceTXT.setText(self.getSelection()[0])

def show():
	global ReplaceMe_win
	try:
		ReplaceMe_win.close()
	except:pass
	ReplaceMe_win = ReplaceMe()
	ReplaceMe_win.show()
	return ReplaceMe_win