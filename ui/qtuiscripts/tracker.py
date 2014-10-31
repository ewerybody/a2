'''
tracker
@author = chrise
version = 0.1

TODO:
- charpart should ask what character to connect to, rigpart what charpart
'''

import maya.cmds as cmds
import os
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as mui
import maya.OpenMaya as om
import sip
import CryRigging as cr

__author__ = 'chrise'

def show():
	return NodeTracker().ui.show()

class NodeTracker(QtGui.QDialog):
	
	def __init__(self):
		ptr = mui.MQtUtil.mainWindow()
		mayaMainWindow = sip.wrapinstance(long(ptr), QtCore.QObject)
		QtGui.QDialog.__init__(self, parent=mayaMainWindow)
		
		uiPath = (os.path.dirname(str(__file__)) + '/tracker.ui').replace('/','\\')
		self.ui = uic.loadUi(uiPath, self)
		wName = mui.MQtUtil.fullName(long(sip.unwrapinstance(self)))
	
		self.connect(self.ui.trackBTN, QtCore.SIGNAL("clicked()"), self.trackFn)
		
		self.newNodeHandles = []
		self.newNodeCallBackMsgId = None
		self.inputName = None
		self.nodeNum = 0
		
	
	def closeEvent(self, e):
		print '[Tracker] Killing scriptJob (' + str(self.newNodeCallBackMsgId) + ')'
		try:
			om.MMessage.removeCallback(self.newNodeCallBackMsgId)
		except:
			pass
	
	def newNodeCallBack(self, node, data):
			self.newNodeHandles.append(om.MObjectHandle(node))
			self.nodeNum += 1
			self.ui.trackBTN.setText('\'' + self.itemName + '\' TRACKING ' + str(self.nodeNum) + ' NODES')
			
	def convertTagged(self, debug=1):
		items = self.findTrackerParts()
		if debug:
			print items
			print self.inputName
		convertTo = self.ui.convertCMB.currentText()
		
		if str(self.inputName) in items.keys():
			if convertTo == 'NameSpace':
				print 'Creating NameSpace', 
				if not cmds.namespace(ex=self.inputName):
					cmds.namespace(add=self.inputName)
				for node in items[self.inputName]:
					newName = self.inputName + ':' + node
					cmds.rename(node, newName)
			if convertTo == 'CryCharacterPart':
				if not cmds.objExists(self.inputName):
					cryCharPart = cmds.createNode('cryCharPart', name=str(self.inputName))
					
					#scan for rigParts
					rigParts = []
					other = []
					for node in items[self.inputName]:
						if not cr.attrExists(node, 'constructor_fn'):
							if cmds.nodeType(node) == 'cryRigPart':
								rigParts.append(node)
							else:
								other.append(node)
					else:
						print 'Skipping node with constructor_fn attr:', node
					if rigParts:
						cr.connectMsgAttrs(cryCharPart + '.rigParts', rigParts, 'rigPart', rebuild=0)
					if other:
						cr.connectMsgAttrs(cryCharPart + '.rigging', other, 'rigging', rebuild=0)
				else:
					#if exists I should later hook up to the existing and check all connections
					cmds.error('Node already exists with name: ' + self.inputName)
			if convertTo == 'CryRigPart':
				if not cmds.objExists(self.inputName):
					cryRigPart = cmds.createNode('cryRigPart', name=self.inputName)

					if items[self.inputName]:
						cr.connectMsgAttrs(cryRigPart + '.rigging', items[self.inputName], 'rigging', rebuild=0)
				else:
					#if exists I should later hook up to the existing and check all connections
					cmds.error('Node already exists with name: ' + self.inputName)
	
	def findTrackerParts(self):
		dangleDict = {}
		for node in cmds.ls('*.trackerTag'):
			nodeName = node.split('.')[0]
			constructor = cmds.getAttr(node)
			if constructor not in dangleDict.keys():
				dangleDict[constructor] = [nodeName]
			else:
				dangleDict[constructor].append(nodeName)
		return dangleDict
	
	def trackFn(self):
		if self.trackBTN.isChecked():
			self.inputName, ok = QtGui.QInputDialog.getText(None, 'Enter Name for Capture Container', 'Enter name:', text='replaceme')
			if ok:
				#reset node info if the tool hasn't closed
				self.newNodeHandles = []
				self.nodeNum = 0
				
				self.inputName = str(self.inputName)
				self.itemName = str(self.inputName)
				self.ui.trackBTN.setText('\'' + self.itemName + '\' TRACKING ' + str(self.nodeNum) + ' NODES')
				self.newNodeCallBackMsgId = om.MDGMessage.addNodeAddedCallback(self.newNodeCallBack)
		else:
			om.MMessage.removeCallback(self.newNodeCallBackMsgId)
			for n in self.newNodeHandles:
				try:
					node = om.MFnDependencyNode(n.object()).name()
					if not cr.attrExists(node, 'trackerTag'):
						cmds.addAttr(node, ln='trackerTag', dt='string')
						cmds.setAttr(node + '.trackerTag', self.inputName, type='string')
				except Exception as e:
					print e
			self.convertTagged()
			self.ui.trackBTN.setText('TRACK NODE CREATION')
		