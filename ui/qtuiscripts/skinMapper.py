import os
import sip
import copy

from PyQt4 import QtGui, QtCore, uic

import maya.OpenMayaUI as openMayaUI
import maya.OpenMaya as openMaya
import maya.mel as mel
import maya.cmds as cmds

from skinBaker import *

def getMayaWindow():
	ptr = openMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

selfDirectory = os.path.dirname(__file__)
uiFile = selfDirectory + '/skinMapper.ui'

form_class, base_class = uic.loadUiType(uiFile)

def open(skinBaker = None, sourceList=[], targetList=[]):
	global skiMapperWindow
	try:
		skiMapperWindow.close()
	except:
		pass

	skiMapperWindow = skinMapperUI(skinBaker = skinBaker, sourceList = sourceList, targetList = targetList)
	skiMapperWindow.show()

class skinMapperUI(base_class, form_class):
	title = 'crySkinMapper'
	
	def __init__(self, parent=getMayaWindow(), skinBaker = None, sourceList=[], targetList=[]):
		super(skinMapperUI, self).__init__(parent)

		self.resSource = []
		self.resTarget = []
		
		self.setupUi(self)
		self.setWindowTitle(self.title)
		
		self.skinBaker = skinBaker

		self.connect(self.btnOK, QtCore.SIGNAL("clicked()"), self.fnBtnOK)
		self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.fnBtnCancel)
		self.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.fnAddFromSceneClicked)
		self.connect(self.btnCleanMapping, QtCore.SIGNAL("clicked()"), self.fnClearMappingClicked)
		self.connect(self.btnAutomap, QtCore.SIGNAL("clicked()"), self.fnAutomapClicked)

		self.fnUpdateGridFromData(fileJointsList = sourceList, sceneJointsFullNamesList = targetList)
		self.fnUpdateSceneListFromData(newList = targetList)

	def fnCalculateResult(self):
		for x in range(0, self.tableMapper.rowCount()):
			sceneCellItem = self.tableMapper.item(x, 1)
			if not sceneCellItem:
				continue

			fileCellItem = self.tableMapper.item(x, 0)
			fileCellText = str(fileCellItem.text())
			sceneCellText = str(sceneCellItem.text())
			
			if len(sceneCellText) > 0:
				self.resSource.append(fileCellText)
				for y in range(0, self.lwSceneJoints.count()):
					sceneListItem = self.lwSceneJoints.item(y)
					if str(sceneListItem.text()).lower() == fileCellText.lower():
						self.resTarget.append(str(sceneListItem.toolTip()))
						break

	def fnAutomapClicked(self):
		for x in range(0, self.tableMapper.rowCount()):
			fileCellItem = self.tableMapper.item(x, 0)
			sceneCellItem = self.tableMapper.item(x, 1)
			if not sceneCellItem:
				sceneCellItem = QtGui.QTableWidgetItem("")
				self.tableMapper.setItem(x, 1, sceneCellItem)
			
			sceneCellItem.setText("")
			fileCellText = str(fileCellItem.text())

			for y in range(0, self.lwSceneJoints.count()):
				sceneListItem = self.lwSceneJoints.item(y)
				if str(sceneListItem.text()).lower() == fileCellText.lower():
					sceneCellItem.setText(str(sceneListItem.text()))
					break
		
	def fnUpdateSceneListFromData(self, newList = []):
		shortJointsSceneNamesList = self.fnGetFinalName(newList)
		for x in range(0, len(shortJointsSceneNamesList)):
			itm = QtGui.QListWidgetItem(shortJointsSceneNamesList[x])
			itm.setToolTip(newList[x])
			self.lwSceneJoints.addItem(itm)
	
	def fnClearMappingClicked(self):
		for x in range(0, self.tableMapper.rowCount()):
			cellItem = self.tableMapper.item(x, 1)
			if cellItem:
				cellItem.setText("")
	
	def fnUpdateGridFromData(self, fileJointsList = [], sceneJointsFullNamesList = []):

		self.tableMapper.setColumnWidth(0, 180)
		self.tableMapper.setColumnWidth(1, 180)
	
		# add file joints
		numFileJoints = len(fileJointsList)
		self.tableMapper.setRowCount(numFileJoints)
		for x in range(0, numFileJoints):
			cellItem = QtGui.QTableWidgetItem(fileJointsList[x])
			self.tableMapper.setItem(x, 0, cellItem)
			
		# add scene joints (if any)
		shortJointsSceneNamesList = self.fnGetFinalName(sceneJointsFullNamesList)
		for x in range(0, numFileJoints):
			cellText = str(self.tableMapper.item(x, 0).text())
			try:
				sceneIdx = shortJointsSceneNamesList.index(cellText)
			except ValueError:
				pass
			else:
				cellItem = QtGui.QTableWidgetItem(shortJointsSceneNamesList[sceneIdx])
				cellItem.setToolTip(sceneJointsFullNamesList[sceneIdx])
				self.tableMapper.setItem(x, 1, cellItem)

#		self.tableMapper.resizeColumnsToContents()
		
	def fnAddFromSceneClicked(self):
		prevSel = cmds.ls(sl=1, l=1, type='joint')
		if self.cbSelectHierarchy.isChecked():
			cmds.select(hi=True)
		nodes = cmds.ls(sl=1, l=1, type='joint')
		nodes = [str(n) for n in nodes]

		self.fnUpdateSceneListFromData(nodes)
		
		if len(prevSel):
			cmds.select(prevSel, r=True)

	def fnBtnOK(self):
		selection = openMaya.MSelectionList()
		openMaya.MGlobal.getActiveSelectionList(selection)
		iterSel = openMaya.MItSelectionList(selection)

		while not iterSel.isDone():
			dagPath = openMaya.MDagPath()
			iterSel.getDagPath(dagPath)
			
			try:
				if dagPath.node().hasFn(openMaya.MFn.kTransform) and dagPath.hasFn(openMaya.MFn.kMesh):	
					self.fnCalculateResult()
					cmds.crySkinData(rs = self.resSource, rt = self.resTarget, n=self.skinBaker.cbNormalizeWeights.currentIndex(), l=[str(self.skinBaker.currentWeightFile), self.skinBaker.lfIgnoreSceneNamespaceCheckbox.isChecked(), self.skinBaker.lfDeleteSkinClusterCheckbox.isChecked(), self.skinBaker.lfUseWorldspacePosCheckbox.isChecked()])
					self.done(0)
				else:
					openMaya.MGlobal.displayError("Select a mesh to apply weights to ...")
			except:
				pass

			break

	def fnBtnCancel(self):
		self.done(0)
		
	def fnGetFinalName(self, list=[]):
		cutNameSpaces = True #self.cbCutNamespaces.isChecked()
		shortNames = True #self.cbShortNames.isChecked()
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
