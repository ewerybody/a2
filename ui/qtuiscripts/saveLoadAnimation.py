import os
import sys
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import sip
import CryAnimation as ca
import CryCore as cc
import CryRigging as cr


def getMayaWindow():
	#'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

uiFile = (os.path.dirname(str(__file__)) + '/saveLoadAnimation.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class SaveLoadAnimation(base_class, form_class):
	def __init__(self,parent=getMayaWindow()):
	
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		self.user = os.environ['USERNAME']
		self.__setUserName()
		
		self.setObjectName('SaveLoadAnimationWindow')
		
		self.connect(self.btnLoad, QtCore.SIGNAL("clicked()"), self.__loadAnimationFn)
		self.connect(self.btnSave, QtCore.SIGNAL("clicked()"), self.__saveAnimationFn)
		self.connect(self.btnNamespace, QtCore.SIGNAL("clicked()"), self.__getNameSpaceFromSelectionFn)
		self.connect(self.cbMultiChar, QtCore.SIGNAL("clicked()"), self.__toggleCutNameSpacesFn)
		
	def __loadAnimationFn(self, iOffset=0, replace=1):
		print ("loading animation...")
		iOffset = self.fOffset.value()
		replaceKeys = self.rbReplaceKeys.isChecked()
		forceNameSpace = self.cbForceNameSpace.isChecked()
		
		nameSpace = None
		
		if (self.rbNameSpaceOverride.isChecked()):
			nameSpace = str(self.tbNamespace.text())
		
		shortNames = self.cbShortNames.isChecked()
		
		basicFilter = "Crytek Animation Save (*.aff)(*.aff)"
		loadFile = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=1)
		if not (loadFile == None):
			loadFile = loadFile[0]
			cmds.undoInfo(openChunk=True)
			try:
				data = ca.loadCurvesFromFile(loadFile)
				for obj in data[0]:
					print obj, data[0][obj]
				ca.setCurvesOnNodes(data[1], replace=replaceKeys, offset=iOffset, namespace=nameSpace, shortNames=shortNames, forceNameSpace=forceNameSpace)
			finally:
				cmds.undoInfo(closeChunk=True)
		
	def __setUserName(self):
		self.tbUserName.setText(self.user)
	
	def __saveAnimationFn(self, selection=1, filter=""):
		doit = True
		cutNamespace = None
		multiChar = self.cbMultiChar.isChecked()
		if multiChar:
			cutNamespace = False
		else:
			cutNamespace = self.cbNamespace.isChecked()
		print "Cut Namespace:",cutNamespace
		nodes = cmds.ls(sl=1)
		selectedNode = None
		if not (self.rbSelection.isChecked()):
			if (nodes):
				selectedNode = nodes[0]
			if (self.rbMethod0.isChecked()):
				nodes = self.__getCharacterControllers(method=0, node=selectedNode, multiChar=multiChar)
			if (self.rbMethod1.isChecked()):
				nodes = self.__getCharacterControllers(method=1, node=selectedNode)
		rigVersion = str(self.tbRigVersion.text())
		metadata = ca.createMetaData(rigVersion=rigVersion,user=self.user)
		
		if (len(nodes) < 1):
			doit = False
			cmds.warning("Nothing select or no selection filter defined.")
		if (doit):
			print ("saving animation...")
			basicFilter = "Crytek Animation Save (*.aff)(*.aff)"
			saveFile = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=0)
			if not saveFile == None:
				saveFile = saveFile[0]
				if not (saveFile == None):
					ca.saveCurvesIntoFile(saveFile, ca.getCurvesFromNodes(nodes=nodes, debug=False, showProgress=True, excludeAttributes=['visibility'], cutNamespace=cutNamespace), metadata=metadata)
			else:
				cmds.warning("Cancelled by user")
			
	def __toggleCutNameSpacesFn(self):
		exportMultiChar = self.cbMultiChar.isChecked()
		if (exportMultiChar):
			self.cbNamespace.setCheckState(0)
	
	def __getCharacterControllers(self,method=None, node=None, multiChar=False):
		nodes = []
		if (method == 0):
			# method with SETS
			nodes = cr.getCharacterControllers(method=0,node=node,multiChar=multiChar)
		elif (method == 1):
			# method with rig node network
			print 'Not implemented yet - returning zero nodes'
		return nodes
		
	def __getNameSpaceFromSelectionFn(self):
		self.rbNameSpaceFromAnim.setChecked(0)
		self.rbNameSpaceOverride.setChecked(1)
		self.tbNamespace.setEnabled(1)
		nodes = cmds.ls(sl=1)
		if nodes:
			if ':' in nodes[0]:
				nameSpace = ''
				tokens = nodes[0].split('|')[0].split(':')
				for i in range(0,len(tokens)-1):
					nameSpace = nameSpace + tokens[i] + ':'
				if nameSpace:
					self.tbNamespace.setText(nameSpace)
			else:
				self.tbNamespace.setText('')

def show():
	window = SaveLoadAnimation()
	window.show()
	return window
