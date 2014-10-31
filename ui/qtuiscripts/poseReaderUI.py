__author__ = 'Judd Simantov'


import sip
import os

from PyQt4 import uic
from PyQt4 import QtCore
from PyQt4 import QtGui


import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import maya.cmds as cmds

from CryRigging import rigParts as rp

import poseReader as pr
reload(pr)

#The UI file must live in the same place as this file
uiPath = os.path.dirname(__file__) + "/poseReaderUI.ui"
form_class, base_class = uic.loadUiType(uiPath)

"""
import poseReaderUI
reload(poseReaderUI)
poseReaderUI.showUI()
"""

#get maya's window so we can parent to it
def getMayaWindow():
	ptr = apiUI.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)


class Window(form_class, base_class):

	def __init__(self, parent=getMayaWindow()):
		super(Window, self).__init__(parent)
		self.setupUi(self)

		self.setWindowTitle("Pose Reader UI")


		self.searchString = ""


		#setup all signal and slot connections
		self.createPoseReader_button.clicked.connect(self.createNode)
		self.refresh_button.clicked.connect(self.listNodes)

		self.poseReader_treeWidget.itemPressed.connect(self.selectNode)

		self.radius_spinBox.valueChanged.connect(self.updateRadius)
		self.coneSize_spinBox.valueChanged.connect(self.updateConeSize)
		self.globalConeSize_spinBox.valueChanged.connect(self.updateGlobalConeSize)
		self.minAngle_spinBox.valueChanged.connect(self.updateConeMinAngle)
		self.maxAngle_spinBox.valueChanged.connect(self.updateConeMaxAngle)

		self.minTwistAngle_spinBox.valueChanged.connect(self.updateMinTwistAngle)
		self.maxTwistAngle_spinBox.valueChanged.connect(self.updateMaxTwistAngle)

		self.aimAxis_comboBox.currentIndexChanged.connect(self.updateAimAxis)
		self.useTwist_comboBox.currentIndexChanged.connect(self.updateUseTwist)
		self.drawOption_comboBox.currentIndexChanged.connect(self.updateDrawOption)
		self.interpType_comboBox.currentIndexChanged.connect(self.updateInterpType)

		self.drawEachWeight_checkbox.stateChanged.connect(self.updateDrawEachWeight)

		self.rotation_checkbox.stateChanged.connect(self.updateCalculationType)
		self.translation_checkbox.stateChanged.connect(self.updateCalculationType)

		self.search_lineEdit.textChanged.connect(self.searchPoseReaders)


		#whent the UI opens find all poseReaders in the scene
		self.listNodes()

		import __main__
		if hasattr(__main__, "gPoseReaderScale"):
			self.globalConeSize_spinBox.setValue(__main__.gPoseReaderScale)

	def createNode(self):
		"""will create the node, requires the UI to present for initial options to be set"""


		if not self.checkPlugin():
			return
		
		radius = self.radius_spinBox.value()
		minAngle = self.minAngle_spinBox.value()
		maxAngle = self.maxAngle_spinBox.value()
		minTwistAngle = self.minTwistAngle_spinBox.value()
		maxTwistAngle = self.maxTwistAngle_spinBox.value()
		aimAxis = self.aimAxis_comboBox.currentIndex()
		drawOption= self.drawOption_comboBox.currentIndex()
		interpType = self.interpType_comboBox.currentIndex()
		drawEachWeight = self.drawEachWeight_checkbox.isChecked()
		
		name = str(self.poseReaderName_label.text())
		rotation = self.rotation_checkbox.isChecked()
		translation = self.translation_checkbox.isChecked()
		
		transRot = None
		if (rotation and translation):
			transRot = 0
		elif (rotation):
			transRot = 1
		elif (translation):
			transRot = 2

		rp.poseReader(name=name , volumeSize=radius, aimAxis=aimAxis, drawOption=drawOption, drawEachWeight=drawEachWeight, interpType=interpType, maxAngle=maxAngle, minAngle=minAngle, minTwistAngle=minTwistAngle, maxTwistAngle=maxTwistAngle, transRot=0)
		self.listNodes()


	def listNodes(self):
		"""get all pose readers in the scene and list them in the tree widget"""

		if not self.checkPlugin():
			return False
		
		self.poseReader_treeWidget.clear()
		nodes = cmds.ls(type="cryPoseReader")

		#loop nodes and do filter check 
		for node in nodes:
			if self.searchString:
				if not self.searchString in node:
					continue


			#create the tree item
			item = QtGui.QTreeWidgetItem()
			item.setText(0, node)

			insertIndex = self.poseReader_treeWidget.topLevelItemCount()
			self.poseReader_treeWidget.insertTopLevelItem(insertIndex, item)

			inputs = cmds.listConnections(node + ".inputMatrix")
			#add children items
			for input in inputs:
				childItem = QtGui.QTreeWidgetItem()
				childItem.setText(0, input)
				index = item.childCount()
				item.insertChild(index, childItem)

	def checkPlugin(self):
		"""function will try and load the plugin and if it cant find it, it will error
		and return false"""

		if not cmds.pluginInfo( "cryPoseReaderPlugin", query=True, loaded=True ):
			try:
				cmds.loadPlugin("cryPoseReaderPlugin.py")
			except:
				api.MGlobal.displayError("Cant find the cryPoseReaderPlugin.py to load!")
				return False

			return True
		else:
			return True

			
	def selectNode(self, item, index):
		"""gets called when the node is selected in the treeWidget"""
		
		poseReader, selIndex = self.__getItemData(item)
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".selectedIndex", selIndex)


		#load all general settings first
		useTwist= cmds.getAttr(poseReader + ".useTwist")
		self.useTwist_comboBox.setCurrentIndex(useTwist)

		aimAxis= cmds.getAttr(poseReader + ".aimAxis")
		self.aimAxis_comboBox.setCurrentIndex(aimAxis)
		drawOption = cmds.getAttr(poseReader + ".drawOption")
		self.drawOption_comboBox.setCurrentIndex(drawOption)

		interpType = cmds.getAttr(poseReader + ".interpType")
		self.interpType_comboBox.setCurrentIndex(interpType)

		drawEachWeight = cmds.getAttr(poseReader + ".drawEachWeight")
		self.drawEachWeight_checkbox.setCheckState(drawEachWeight)

		calculateType = cmds.getAttr(poseReader + ".calculate")
		if (calculateType == 0):
			self.rotation_checkbox.setCheckState(True)
			self.translation_checkbox.setCheckState(True)
		elif (calculateType == 1):
			self.rotation_checkbox.setCheckState(True)
			self.translation_checkbox.setCheckState(False)
		elif (calculateType == 2):
			self.rotation_checkbox.setCheckState(False)
			self.translation_checkbox.setCheckState(True)


		#load node specific settings
		if (selIndex == -1):
			cmds.select(poseReader, r=1)
			volumeSize = cmds.getAttr(poseReader + ".volumeSize")
			self.radius_spinBox.setValue(volumeSize)
			
			minAngle = cmds.getAttr(poseReader + ".minAngle[0]")
			self.minAngle_spinBox.setValue(minAngle)
			maxAngle = cmds.getAttr(poseReader + ".maxAngle[0]")
			self.maxAngle_spinBox.setValue(maxAngle)

			minTwistAngle = cmds.getAttr(poseReader + ".minTwistAngle[0]")
			self.minTwistAngle_spinBox.setValue(minTwistAngle)
			maxTwistAngle = cmds.getAttr(poseReader + ".maxTwistAngle[0]")
			self.maxTwistAngle_spinBox.setValue(maxTwistAngle)

			sl = cmds.ls(sl=1)[0]
			self.poseReaderName_label.setText(sl)

		#load index specfic settings
		else:

			self.poseReaderName_label.setText(item.parent().text(0))
			
			radius = cmds.getAttr(poseReader + ".volumeRadius[" + str(selIndex) + "]")
			self.radius_spinBox.setValue(radius)
			minAngle = cmds.getAttr(poseReader + ".minAngle[" + str(selIndex) + "]")
			self.minAngle_spinBox.setValue(minAngle)
			maxAngle = cmds.getAttr(poseReader + ".maxAngle[" + str(selIndex) + "]")
			self.maxAngle_spinBox.setValue(maxAngle)

			minTwistAngle = cmds.getAttr(poseReader + ".minTwistAngle[" + str(selIndex) + "]")
			self.minTwistAngle_spinBox.setValue(minTwistAngle)
			maxTwistAngle = cmds.getAttr(poseReader + ".maxTwistAngle[" + str(selIndex) + "]")
			self.maxTwistAngle_spinBox.setValue(maxTwistAngle)
			


	def searchPoseReaders(self, searchText):
		"""search/filter function for poseReaders in the treeWidget"""
		self.searchString = searchText
		self.listNodes()

	def updateName(self, name):

		if not len(self.poseReader_treeWidget.selectedItems()):
			return
		
		selectedItem = self.poseReader_treeWidget.selectedItems()[0]
		poseReader, selIndex = self.__getItemData(selectedItem)
		if poseReader == None:
			return
		poseReader = str(poseReader)
		if (selIndex == -1):
			selectedItem.setText(0, name)
		else:
			selectedItem.parent().setText(0, name)

		transform = cmds.listRelatives(poseReader, p=1)[0]
		cmds.rename(poseReader, name)
		cmds.rename(transform, name + "_transform")


	def updateRadius(self):

		value = self.radius_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		if (selIndex > -1):
			cmds.setAttr(transform + ".volumeRadius" + str(selIndex), value)
		else:
			cmds.setAttr(poseReader + ".volumeSize", value)

	def updateConeSize(self):

		value = self.coneSize_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		cmds.setAttr(poseReader + ".coneSize", value)

	def updateConeMinAngle(self):

		value = self.minAngle_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		if (selIndex > -1):
			cmds.setAttr(transform + ".minAngle" + str(selIndex), value)
		else:
			size = cmds.getAttr(poseReader + ".minAngle", s=1)
			for i in range(size):
				cmds.setAttr(transform + ".minAngle" + str(i), value)

	def updateConeMaxAngle(self):

		value = self.maxAngle_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		if (selIndex > -1):
			cmds.setAttr(transform + ".maxAngle" + str(selIndex), value)
		else:
			size = cmds.getAttr(poseReader + ".maxAngle", s=1)
			for i in range(size):
				cmds.setAttr(transform + ".maxAngle" + str(i), value)

	def updateMinTwistAngle(self):

		value = self.minTwistAngle_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		if (selIndex > -1):
			cmds.setAttr(transform + ".minTwistAngle" + str(selIndex), value)
		else:
			size = cmds.getAttr(poseReader + ".minTwistAngle", s=1)
			for i in range(size):
				cmds.setAttr(transform + ".minTwistAngle" + str(i), value)

	def updateMaxTwistAngle(self):

		value = self.maxTwistAngle_spinBox.value()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		transform = cmds.listRelatives(poseReader, p=1)[0]
		if (selIndex > -1):
			cmds.setAttr(transform + ".maxTwistAngle" + str(selIndex), value)
		else:
			size = cmds.getAttr(poseReader + ".maxTwistAngle", s=1)
			for i in range(size):
				cmds.setAttr(transform + ".maxTwistAngle" + str(i), value)

	def updateUseTwist(self):

		index = self.useTwist_comboBox.currentIndex()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".useTwist", index)

	def updateAimAxis(self):

		index = self.aimAxis_comboBox.currentIndex()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".aimAxis", index)

	def updateDrawOption(self):

		index = self.drawOption_comboBox.currentIndex()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".drawOption", index)


	def updateCalculationType(self):

		rotation = self.rotation_checkbox.isChecked()
		translation = self.translation_checkbox.isChecked()

		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		if (rotation and translation):
			cmds.setAttr(poseReader + ".calculate", 0)
		elif (rotation):
			cmds.setAttr(poseReader + ".calculate", 1)
		elif (translation):
			cmds.setAttr(poseReader + ".calculate", 2)

	def updateInterpType(self):

		index = self.interpType_comboBox.currentIndex()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".interpType", index)


	def updateDrawEachWeight(self):

		value = self.drawEachWeight_checkbox.isChecked()
		poseReader, selIndex = self.__getSelectedItemData()
		if poseReader == None:
			return
		poseReader = str(poseReader)
		cmds.setAttr(poseReader + ".drawEachWeight", value)

	def updateGlobalConeSize(self):

		value = self.globalConeSize_spinBox.value()

		import __main__

		if hasattr(__main__, "gPoseReaderScale"):
			__main__.gPoseReaderScale = value
			view = apiUI.M3dView.active3dView()
			view.refresh(True, True)


	def __getSelectedItemData(self):
		"""will get the selected pose reader and selected index from the tree widget"""

		if not len(self.poseReader_treeWidget.selectedItems()):
			return (None, None)
		
		selectedItem = self.poseReader_treeWidget.selectedItems()[0]
		return self.__getItemData(selectedItem)

	def __getItemData(self, item):
		"""will get the pose reader and selected index from the tree widget item passed in"""
		poseReader = ""
		selIndex = -1
		if not item.childCount():
			parent = item.parent()
			selIndex = parent.indexOfChild(item)
			poseReader = parent.text(0)
		else:
			poseReader = item.text(0)

		return (poseReader, selIndex)





def showUI():

	#import main to make sure we can store the UI there
	import __main__

	if hasattr(__main__, "poseReaderWindow"):
		__main__.poseReaderWindow.close()
	__main__.poseReaderWindow = Window()
	__main__.poseReaderWindow.show()

	return __main__.poseReaderWindow





