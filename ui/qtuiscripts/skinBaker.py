import os
import sip

from PyQt4 import QtGui, QtCore, uic

import maya.OpenMayaUI as openMayaUI
import maya.OpenMaya as openMaya
import maya.mel as mel
import maya.cmds as cmds

import skinMapper as sm

def getMayaWindow():
	ptr = openMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

selfDirectory = os.path.dirname(__file__)
uiFile = selfDirectory + '/skinBaker.ui'

form_class, base_class = uic.loadUiType(uiFile)

def open():
	global skiBakerWindow
	try:
		skiBakerWindow.close()
	except:
		pass

	skiBakerWindow = skinBakerUI()
	skiBakerWindow.show()
	
class skinBakerUI(base_class, form_class):
	title = 'crySkinBaker'
	
	def __init__(self, parent=getMayaWindow()):
		super(skinBakerUI, self).__init__(parent)

		self.setupUi(self)
		self.setWindowTitle(self.title)
		
		if not cmds.pluginInfo('crySkinData_2013_64', q=1, l=1):    
			cmds.loadPlugin('crySkinData_2013_64')

		windowUIName = openMayaUI.MQtUtil.fullName(long(sip.unwrapinstance(self)))
		if cmds.window('SkinBakerWindow', q=1, ex=1):
			cmds.deleteUI('SkinBakerWindow')

		cmds.window('SkinBakerWindow', widthHeight=(380, 600), resizeToFitChildren=1)
		
		# save
		self.connect(self.sfDirectoryButton, QtCore.SIGNAL("clicked()"), self.fnSaveDirectoryButtonClicked)
		self.connect(self.sfSaveButton, QtCore.SIGNAL("clicked()"), self.fnSaveSaveButtonClicked)
		self.connect(self.sfRefreshButton, QtCore.SIGNAL("clicked()"), self.fnSaveRefreshButtonClicked)
		
		# load
		self.connect(self.lfLoadButton, QtCore.SIGNAL("clicked()"), self.fnLoadLoadButtonClicked)
		self.connect(self.lfRemapperButton, QtCore.SIGNAL("clicked()"), self.fnLoadRemapperButtonClicked)
		
		# baking
		self.connect(self.bButton, QtCore.SIGNAL("clicked()"), self.fnBakeButtonClicked)
		self.connect(self.bSelectVertsButton, QtCore.SIGNAL("clicked()"), self.fnbSelectVertsButtonClicked)
		self.connect(self.bDeleteButton, QtCore.SIGNAL("clicked()"), self.fnbDeleteButtonClicked)
		self.connect(self.ubButton, QtCore.SIGNAL("clicked()"), self.fnUnbakeButtonClicked)
				
		# tools
		self.connect(self.tDeleteHistoryButton, QtCore.SIGNAL("clicked()"), self.fnToolsDeleteHistoryButtonClicked)
		
		# initialize UI
		self.fnInitializeUI()
		
	def fnToolsDeleteHistoryButtonClicked(self):
		nodes = cmds.ls(sl=1, l=1)
		for node in nodes:
			cmds.delete(node, ch=1)
		
	def fnSaveRefreshButtonClicked(self):
		currentFile = cmds.file(sn=True, q=True)
		dirName = os.path.dirname(currentFile)
		self.sfDirectoryEdit.setText(dirName)
		
	def fnSaveSaveButtonClicked(self):
		selection = openMaya.MSelectionList()
		openMaya.MGlobal.getActiveSelectionList(selection)
		iterSel = openMaya.MItSelectionList(selection)

		while not iterSel.isDone():
			dagPath = openMaya.MDagPath()
			iterSel.getDagPath(dagPath)
			
			partialName = dagPath.partialPathName()
			partialName = partialName.split('|')[-1].split(':')[-1]

			try:
				if dagPath.node().hasFn(openMaya.MFn.kTransform) and dagPath.hasFn(openMaya.MFn.kMesh):
					if not self.sfUseObjectsNamesCheckbox.isChecked():
						fileSaveDialog = QtGui.QFileDialog(self, "Save weight files", self.sfDirectoryEdit.text(), "Weights (*.weights)")
						fileSaveDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
						fileSaveDialog.selectFile(partialName + ".weights")
						if fileSaveDialog.exec_() == 1:
							fullFilePath = (str(fileSaveDialog.selectedFiles()[0]))
					else:
						fullFilePath = self.sfDirectoryEdit.text() + "\\" + partialName + ".weights"
						
	    			cmds.crySkinData(s=str(fullFilePath), o=str(dagPath.partialPathName()))
			except:
				pass
			iterSel.next()
		
	def fnSaveDirectoryButtonClicked(self):
		dirPathDialog = QtGui.QFileDialog(self,"Select Directory", self.sfDirectoryEdit.text())
		dirPathDialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		if dirPathDialog.exec_() == 1:
			self.sfDirectoryEdit.setText(str(dirPathDialog.selectedFiles()[0]))
			
	def fnLoadRemapperButtonClicked(self):
		filePathDialog = QtGui.QFileDialog(self, "Select weight files", self.sfDirectoryEdit.text(), "Weights (*.weights)")
		if filePathDialog.exec_() != 1:
			return
		
		sourceBoneList = []
		targetBoneList = []
		
		weightFile = filePathDialog.selectedFiles()[0]
		if not weightFile:
			return

		sourceBoneList = cmds.crySkinData(gfj = str(weightFile))
		self.currentWeightFile = weightFile
			
		sel = cmds.ls(sl=True)[0]
		if sel:
			sc = mel.eval('findRelatedSkinCluster ' + sel)
			if sc:
				targetBoneList = cmds.skinCluster(sc, query = True, influence = True)
			try:
				sm.open(skinBaker = self, sourceList = sourceBoneList, targetList = targetBoneList)
			except:
				pass

	def fnLoadLoadButtonClicked(self):
		filePathDialog = QtGui.QFileDialog(self, "Select weight files", self.sfDirectoryEdit.text(), "Weights (*.weights)")
		filePathDialog.setFileMode(QtGui.QFileDialog.ExistingFiles);
		if filePathDialog.exec_() != 1:
			return

		for weightFile in filePathDialog.selectedFiles():
			cmds.crySkinData(n=self.cbNormalizeWeights.currentIndex(), l=[str(weightFile), self.lfIgnoreSceneNamespaceCheckbox.isChecked(), self.lfDeleteSkinClusterCheckbox.isChecked(), self.lfUseWorldspacePosCheckbox.isChecked()])
		
	def fnBakeButtonClicked(self):
		cmds.crySkinData(b=True)
		
	def fnbSelectVertsButtonClicked(self):
		selection = openMaya.MSelectionList()
		openMaya.MGlobal.getActiveSelectionList(selection)
		iterSel = openMaya.MItSelectionList(selection)

		while not iterSel.isDone():
			dagPath = openMaya.MDagPath()
			iterSel.getDagPath(dagPath)
			
			try:
				if dagPath.node().hasFn(openMaya.MFn.kTransform) and dagPath.hasFn(openMaya.MFn.kMesh):	
					cmds.crySkinData(o=str(dagPath.partialPathName()), sbv=True)
			except:
				pass
			iterSel.next()
		
	def fnbDeleteButtonClicked(self):
		cmds.crySkinData(db=True)
		
	def fnUnbakeButtonClicked(self):
		cmds.crySkinData(n=self.cbNormalizeWeights.currentIndex(), ub=[self.ubIgnoreSceneNamespacesCheckbox.isChecked(), self.ubDeleteSkinclusterCheckbox.isChecked(), self.ubSmoothWeightsCheckbox.isChecked()])
		
	def fnInitializeUI(self):
		self.fnSaveRefreshButtonClicked()
