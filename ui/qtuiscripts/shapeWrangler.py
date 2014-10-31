import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as mui
import sip
from PyQt4 import QtGui, QtCore, uic
from CryRigging import shapeTools
import CryRigging as cr
import os

def show():
	return shapeWrangler()

class shapeWrangler(QtGui.QDialog):
	def __init__(self):
		self.sculptMode = 0
		self.skinMsh = None
		self.sculptMsh = None
		self.meshes = []
		self.addShape = None
		
		ptr = mui.MQtUtil.mainWindow()
		mayaMainWindow = sip.wrapinstance(long(ptr), QtCore.QObject)
		QtGui.QDialog.__init__(self, parent=mayaMainWindow)
		
		#pathing: home, local office, network
		uiPath = None
		try: uiPath = (os.path.dirname(str(__file__)) + '/shapeWrangler.ui').replace('/','\\')
		#except: uiPath = 'D:\\crytek\\tools\\pcap_shoot_tools_dir\\Tools\\CryMayaTools\\CryRigging\\shapeWrangler\\shapeWrangler.ui'
		except: uiPath = 'J:\\data\\Production\\TechArt\\Builds\\Latest\\Tools\\CryMayaTools\\CryRigging\\shapeWrangler\\shapeWrangler.ui'

		self.ui = uic.loadUi(uiPath)
		self.ui.show()

		self.connect(self.ui.createBTN, QtCore.SIGNAL("clicked()"), self.createFn)
		self.connect(self.ui.refreshPoseReaderCmbBTN, QtCore.SIGNAL("clicked()"), self.poseReaderChkFn)
		self.connect(self.ui.poseReaderCHK, QtCore.SIGNAL("stateChanged(int)"), self.poseReaderChkFn)
		
		self.refreshTree()
	
	def connectShape(self, mesh, shape):
		if not self.attrExists(mesh,'additiveShapes'):
			cmds.addAttr(mesh, longName='additiveShapes', attributeType='message', s=1)
		cmds.addAttr(shape, longName='additiveShape', attributeType='message', s=1)
		cmds.connectAttr((mesh + '.additiveShapes'), (shape + '.additiveShape'), f=1)
	
	def saveDagPose(self, name):
		infs = cmds.skinCluster(self.skinMsh, inf=1, q=1)
		dp = cmds.dagPose(infs, n=name, save=1)
		self.addToSet(dp, 'shapeWrangler_additivePoses')
		if not self.attrExists(self.skinMsh,'additivePoses'):
			cmds.addAttr(self.skinMsh, longName='additivePoses', attributeType='message', s=1)
		cmds.addAttr(dp, longName='additivePose', attributeType='message', s=1)
		cmds.connectAttr((self.skinMsh + '.additivePoses'), (dp + '.additivePose'), f=1)
		
	
	def attrExists(self, node, attr):
		return cmds.attributeQuery(attr, n=node, ex=1)
	
	def getPoseReaders(self):
		return cmds.ls(type='cryPoseReader')
	
	def poseReaderChkFn(self):
		if self.ui.poseReaderCHK.isChecked():
			self.ui.poseReaderCMB.clear()
			for reader in self.getPoseReaders():
				self.ui.poseReaderCMB.addItem(reader)
		else:
			pass
	
	def setSculptMode(self, mode):
		if mode:
			pal = QtGui.QPalette(self.ui.palette())
			self.ui.setAutoFillBackground(True)
			self.ui.createBTN.setAutoFillBackground(True)
			#pal.setColor(QtGui.QPalette.Button, QtGui.QColor('darkRed'))
			pal.setColor(QtGui.QPalette.Window,QtGui.QColor('darkRed'))
			self.ui.setPalette(pal)
			self.ui.createBTN.setPalette(pal)
			self.sculptMode = 1
		else:
			pal = QtGui.QPalette(self.ui.palette())
			self.ui.setAutoFillBackground(True)
			pal.setColor(QtGui.QPalette.Window,QtGui.QColor(68,68,68,255))
			self.ui.setPalette(pal)
			self.sculptMode = 0
	
	def addToSet(self, nodes, name):
		for node in nodes:
			if not cmds.objExists(name):
				cmds.sets(nodes, n=name)
		else:
			cmds.sets(nodes, add=name)
	
	def refreshTree(self):
		self.ui.shapeTree.clear()
		
		if self.meshes == []:
			if cmds.objExists('shapeWrangler_skinMeshes'):
				for dpose in cmds.sets('shapeWrangler_skinMeshes', q=1): self.meshes.append(dpose)
		for mesh in self.meshes:
			wid = QtGui.QTreeWidgetItem()
			wid.setText(0, mesh)
			self.ui.shapeTree.addTopLevelItem(wid)
			for shape in cmds.listConnections((mesh + '.additiveShapes'), d=1):
				wid2 = QtGui.QTreeWidgetItem()
				wid2.setText(0, shape)
				wid.addChild(wid2)
		self.ui.shapeTree.expandAll()
	
	def createFn(self):
		cmds.undoInfo(openChunk=True)
		if self.ui.createBTN.isChecked():
			sel = cmds.ls(sl=1)
			if len(sel) == 0:
				cmds.warning('[shapeWrangler] Nothing selected!')
			self.skinMsh = cmds.ls(sl=1)[0]
			if cmds.nodeType(shapeTools.getShape(self.skinMsh)) == 'mesh':
				
				if cr.findRelatedSkinCluster(self.skinMsh):
					buttonTxt = 'SCULPT MODE: ' + self.skinMsh
					self.ui.createBTN.setText(buttonTxt)
					sculptMshName = self.skinMsh + '_sculptMsh'
					self.sculptMsh = cmds.duplicate(self.skinMsh, n=sculptMshName)[0]
					cmds.hide(self.skinMsh)
					self.setSculptMode(True)
					
					
				else:
					warn = '[shapeWrangler WARNING] Node \'' + self.skinMsh + '\' does not have a skin modifier.'
					cmds.warning(warn)
					self.ui.createBTN.setChecked(False)
					self.ui.createBTN.setText('CREATE ADDITIVE')
					return False
			else:
				warn = '[shapeWrangler WARNING] Node \'' + self.skinMsh + '\' is not a mesh.'
				cmds.warning(warn)
				self.ui.createBTN.setChecked(False)
				self.ui.createBTN.setText('CREATE ADDITIVE')
				return False
		else:
			if self.sculptMode:	
				if self.sculptMsh:
					#generate shape
					shapeName = self.skinMsh + '_ADD'
					addShape = shapeTools.getAdditiveShape(self.skinMsh, self.sculptMsh, name=shapeName)
					self.addShape = addShape
					
					self.connectShape(self.skinMsh, addShape)
					if self.skinMsh not in self.meshes: self.meshes.append(self.skinMsh)						
					
					dagName = self.skinMsh + '_POSE'
					self.saveDagPose(dagName)
					
					#connect to poseReader, add the blendshape
					if self.ui.poseReaderCHK.isChecked():
						selectedPR = str(self.ui.poseReaderCMB.currentText())
						
						#add blendshape
						bshape = cmds.blendShape(addShape, self.skinMsh, name=(addShape + '_BSHAPE'))[0]
						cmds.reorderDeformers(cr.findRelatedSkinCluster(self.skinMsh), bshape, [self.skinMsh])
						cmds.connectAttr((selectedPR + '.weight'), (bshape + '.weight[0]'))
					
					#cmds.delete(self.sculptMsh)
					cmds.hide(self.sculptMsh)
					self.addToSet(self.sculptMsh, 'shapeWrangler_sculptMeshes')
					self.addToSet(self.skinMsh, 'shapeWrangler_skinMeshes')
					cmds.showHidden(self.skinMsh)
					cmds.select(self.skinMsh)
				else:
					cmds.warning(('[shapeWrangler] sculptMesh ' + self.sculptMsh + 'not found'))
			self.ui.createBTN.setChecked(False)
			self.setSculptMode(False)
			self.ui.createBTN.setText('CREATE ADDITIVE')
		self.refreshTree()
		cmds.undoInfo(closeChunk=True)