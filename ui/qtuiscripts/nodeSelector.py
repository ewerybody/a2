'''
Prompts the user to select a node in the scene, only works with transforms now, need to make it work with any nodes, I guess.
@creation=2012.02.04
@version=1.0
@author=chrise
'''

from os import path
import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic

uiFile = (path.dirname(str(__file__)) + '/nodeSelector.ui').replace('/','\\')
#uiFile = 'X:\\projects\\2011\\crytek\\Tools\\CryMayaTools\\CryCore\\nodeSelector\\nodeSelector.ui'
form_class, base_class = uic.loadUiType(uiFile)

class nodeSelect(base_class, form_class):
	def __init__(self):
		super(base_class, self).__init__(None)
		self.setupUi(self)
		self.connect(self.getNodesBTN, QtCore.SIGNAL("clicked()"), self.getNodesFn)
		self.result = None
		self.rebuildTree()

	def traverse(self, node, wid):
		children = cmds.listRelatives(node, children=True, fullPath=True)
		if children:
			for child in children:
				nodeShort = child.split('|')[-1]
				wid1 = None
				existing = None
				for c in range(0, wid.childCount()):
					if wid.child(c).text(0) == nodeShort: existing = wid.child(c)
				if existing: wid1 = existing
				else:
					wid1 = QtGui.QTreeWidgetItem()
				wid1.setText(0,nodeShort)
				wid1.setData(0,QtCore.Qt.UserRole,str(child))
				wid.addChild(wid1)
				self.traverse(child, wid1)

	def getTopLevelNodes(self):
		allNodes = cmds.ls(transforms=1, l=1)
		topNodes = []
		for node in allNodes:
			split = node.split('|')[1]
			if split not in topNodes: topNodes.append(split)
		return topNodes

	def rebuildTree(self):
		self.nodeTree.clear()
		self.nodeTree.setColumnCount(0)
		self.nodeTree.setStyle(QtGui.QStyleFactory.create('motif'))
		topNodes = self.getTopLevelNodes()
		for node in topNodes:
			nodeShort = node.split('|')[-1]
			wid1 = QtGui.QTreeWidgetItem()
			self.nodeTree.setColumnCount(1)
			wid1.setText(0,nodeShort)
			wid1.setData(0,32,str(node))
			self.nodeTree.addTopLevelItem(wid1)
				
			self.traverse(node, wid1)
			self.nodeTree.expandAll()
	
	def getNodesFn(self):
		self.result = []
		for item in self.nodeTree.selectedItems():
			self.result.append(str(item.data(0,QtCore.Qt.UserRole).toString()))
		self.close()

def show():
	nodes = nodeSelect()
	nodes.exec_()
	return nodes.result