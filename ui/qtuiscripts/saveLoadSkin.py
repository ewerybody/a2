import os
import sys
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import sip
import CryRigging
import CryCore


def getMayaWindow():
	#'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

uiFile = (os.path.dirname(str(__file__)) + '/saveLoadSkin.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class SaveLoadSkin(base_class, form_class):
	def __init__(self,parent=getMayaWindow()):
	
		super(base_class, self).__init__(parent)

		self.setupUi(self)
		
		self.connect(self.btnLoad, QtCore.SIGNAL("clicked()"), self.__loadSkinFn)
		self.connect(self.btnSave, QtCore.SIGNAL("clicked()"), self.__saveSkinFn)
		
	def __loadSkinFn(self):
		doit = False
		nodes = cmds.ls(sl=1)
		deleteHistory = self.cbDeleteHistory.isChecked()
		worldSpace = self.cbWorldSpace.isChecked()
		threshold = self.nThreshold.value()
		vertexDistance = self.nVertexDistance.value()
		if len(nodes) == 1:
			basicFilter = "Crytek Skin Save (*.weights)(*.weights)"
			loadFile = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=1)
			if loadFile:
				loadFile = loadFile[0]
				print ("loading Skin...")
				if (deleteHistory):
					print ("deleting history on mesh")
					cmds.delete(ch=1)
				if (worldSpace):
					cmds.crySkinData(f=loadFile, ws=1, p=1, th=threshold, vd=vertexDistance)
				else:
					cmds.crySkinData(f=loadFile)
			else:
				cmds.warning('Cancelled by user')
		else:
			cmds.warning('Please select a mesh to load skin onto')

	def __saveSkinFn(self):
		doit = True
		nodes = cmds.ls(sl=1)
		if (len(nodes) == 1):
			basicFilter = "Crytek Skin Save (*.weights)(*.weights)"
			saveFile = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=0)
			if saveFile:
				saveFile = saveFile[0]
				if saveFile:
					print ("saving Skin...")
					cmds.crySkinData(s=1,f=saveFile,p=1)
			else:
				cmds.warning("Cancelled by user")
		else:
			cmds.warning('Please select a skinned mesh')
		
def show():
	window = SaveLoadSkin()
	window.show()
	return window
