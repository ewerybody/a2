import maya.cmds as cmds
import os
import maya.OpenMaya as om
from PyQt4 import QtGui, QtCore, uic

def show():
	return rigTools()

class rigTools(QtGui.QMainWindow):
	#not working when i place in the __init__, no one knows why
	iconLib = {}
	iconPath = os.environ.get('MAYA_LOCATION', None) + '/icons/'
	iconLib['joint'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'kinJoint.png'))
	iconLib['ikHandle'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'kinHandle.png'))
	iconLib['transform'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'orientJoint.png'))
	nameColumn = None
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		#pathing: home, local office, network
		uiPath = None
		try: uiPath = (os.path.dirname(str(__file__)) + '/rigTools.ui').replace('/','\\')
		except: uiPath = 'X:\\projects\\2011\\crytek\\Tools\\CryMayaTools\\CryRigging\\rigTools\\rigTools.ui'
		#except: uiPath = 'J:\\data\\Production\\TechArt\\Builds\\Latest\\Tools\\CryMayaTools\\CryRigging\\rigTools\\rigTools.ui'

		self.ui = uic.loadUi(uiPath)
		self.ui.show()
		
		self.refreshTree()
		self.connect(self.ui.loadSelBTN, QtCore.SIGNAL("clicked()"), self.refreshTree)
		self.connect(self.ui.makeIkChainBTN, QtCore.SIGNAL("clicked()"), self.makeIkChain)
		self.connect(self.ui.orientBTN, QtCore.SIGNAL("clicked()"), self.makeOrient)
		self.connect(self.ui.pointBTN, QtCore.SIGNAL("clicked()"), self.makePoint)
		self.connect(self.ui.linkJointsBTN, QtCore.SIGNAL("clicked()"), self.linkJoints)


## GENERAL
####################
	def getSelection(self):
		nodes = []
		sel = om.MSelectionList()
		om.MGlobal.getActiveSelectionList(sel)

		for i in range(0,sel.length()):
			path = om.MDagPath()
			sel.getDagPath(i, path)
			nodes.append(path)
		return nodes


## TAGGING
####################
	def addTag(self, widget, node, name, textColor, nameColumn, extraTxt='>>  ', debug=1):
		color = None
		if textColor == 'red': color = QtGui.QColor(255,0,0,200)
		if textColor == 'yellow': color = QtGui.QColor(255,255,17,200)
		if textColor == 'blue': color = QtGui.QColor(0,140,255,200)
		font = widget.font(0)
		#force no bold, since bold is inheritted
		font.setWeight(QtGui.QFont.Normal)
		font.setPointSize(8)
		if debug == 1: print '>>--DEBUG-->> listConnections Return:', cmds.listConnections((node.fullPathName() + '.' + name), type='transform'), 'Node:', node.fullPathName().split('|')[-1]
		wid2 = QtGui.QTreeWidgetItem()
		val = None
		if not cmds.listConnections((node.fullPathName() + '.' + name), type='transform'): val = 'EMPTY'
		else: val = cmds.listConnections((node.fullPathName() + '.' + name), type='transform')[0]
		wid2.setText(self.nameColumn, (extraTxt + name + ': ' + val))
		wid2.setFont(self.nameColumn,font)
		if color: wid2.setTextColor(self.nameColumn,color)
		widget.addChild(wid2)
	
	def attrExists(self, node, attr):
		return cmds.attributeQuery(attr, n=node, ex=1)
	
	def linkJoints(self):
		from skeleTools import skelLink
		oldSel = cmds.ls(sl=1)
		nodes = self.longNamesFromTree()
		if len(nodes) == 2:
			skelLink(nodes[0], nodes[1], conn='msg', debug=1)
		else: cmds.warning('Requires two joints selected.')
		#RELOAD TREE
		cmds.select(oldSel)
		self.refreshTree()


## UI RELATED
####################
	def refreshTree(self):
		self.ui.tree.clear()
		
		n = 1
		for node in self.getSelection():
			name = None
			if self.ui.shortNamesCHK.isChecked() == True: name = node.fullPathName().split('|')[-1]
			if self.ui.shortNamesCHK.isChecked() == False: name = node.fullPathName()
			
			#ADD TOP LEVEL ITEMS (NODES)
			wid1 = QtGui.QTreeWidgetItem()
			light_blue = QtGui.QColor(80,100,115,128)
			
			if self.ui.selOrderCHK.isChecked() == True:
				self.ui.tree.setColumnCount(3)
				self.ui.tree.setColumnWidth(1, 15)
				wid1.setBackgroundColor(1,light_blue)
				wid1.setText(1,str(n))
				wid1.setText(2,name)
				self.nameColumn = 2
				n += 1
			else:
				self.ui.tree.setColumnCount(2)
				wid1.setText(1,name)
				self.nameColumn = 1
			
			wid1.setData(0,32,str(node.fullPathName()))
			self.setIcon(node.fullPathName(), wid1)
			self.ui.tree.addTopLevelItem(wid1)
			
			#ADD CHILDREN (MARKED ATTRS)
			#---------------------------
			
			#SKEL LINK
			if cmds.attributeQuery('skelLink', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'skelLink', 'yellow', self.nameColumn, extraTxt='>> SKEL LINK >>  ')
			
			#IK CHAIN
			if cmds.attributeQuery('tagIkEnd', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagIkEnd', 'red', self.nameColumn, extraTxt='>> IK START >>  ')
			if cmds.attributeQuery('tagIkStart', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagIkStart', 'red', self.nameColumn, extraTxt='>> IK END >>  ')
			if cmds.attributeQuery('tagIkPv', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagIkPv', 'blue', self.nameColumn, extraTxt='>> IK PV >>  ')
				
			#CONSTRAINTS
			if cmds.attributeQuery('tagOrientDriven', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagOrientDriven', 'red', self.nameColumn, extraTxt='>> ORIENT CONST >>  ')
			if cmds.attributeQuery('tagOrientDriver', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagOrientDriver', 'red', self.nameColumn, extraTxt='>> ORIENT CONST >>  ')
			if cmds.attributeQuery('tagPointDriven', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagPointDriven', 'red', self.nameColumn, extraTxt='>> POINT CONST >>  ')
			if cmds.attributeQuery('tagPointDriver', n=node.fullPathName(), ex=1) == True:
				self.addTag(wid1, node, 'tagPointDriver', 'red', self.nameColumn, extraTxt='>> POINT CONST >>  ')
				
		self.ui.tree.expandAll()
	
	def setIcon(self, node, widget):
		type = cmds.nodeType(node)
		icon = None
		if type in self.iconLib.keys(): icon = self.iconLib[type]
		if icon: widget.setIcon(0, icon)
	
	def longNamesFromTree(self):
		longs = []
		#casting the QVariant back to a long path
		for i in range(0,self.ui.tree.topLevelItemCount()): longs.append(str(self.ui.tree.topLevelItem(i).data(0,32).toString()))
		return longs


## RIGGING
####################
	def makeIkChain(self):
		oldSel = cmds.ls(sl=1)
		parts = self.longNamesFromTree()
		
		solver = None
		solCMB = self.ui.solverCMB.currentIndex()
		if solCMB == 0: solver = 'ikRPsolver'
		if solCMB == 1: solver = 'ikSCsolver'
		if solCMB == 2: solver = 'ikSplineSolver'
		print('Building IK chain from ' + parts[0] + ' to ' + parts[1] + ' (' + solver + ')')
		
		#BUILD IK CHAIN
		handleName = parts[0].split('|')[-1] + '_ikHandle'
		#create chain
		chain = None
		if solCMB == 0: chain = cmds.ikHandle(n=handleName, sj=parts[0], ee=parts[1], sol=solver, jl=1)
		if solCMB == 2: chain = cmds.ikHandle(n=handleName, sj=parts[0], ee=parts[1], sol=solver, jl=1, roc=0, ccv=0)
		
		#Create rigPart node
		rigPart = cmds.createNode("cryRigPart", name='rigPart_ikChain')
		
		if not self.attrExists(parts[1],'rigPart'): cmds.addAttr(parts[1], longName='rigPart', attributeType='message', s=1)
		if not self.attrExists(parts[0],'rigPart'): cmds.addAttr(parts[0], longName='rigPart', attributeType='message', s=1)
		cmds.connectAttr((parts[0] + '.rigPart'), (rigPart + '.startJoint'), f=1)
		cmds.connectAttr((parts[1] + '.rigPart'), (rigPart + '.endJoint'), f=1)
		if self.ui.pvCHK.isChecked():
			pv = cmds.poleVectorConstraint(parts[2], handleName)[0]
			if not self.attrExists(parts[2],'rigPart'): cmds.addAttr(pv, longName='rigPart', attributeType='message', s=1)
			cmds.connectAttr((parts[2] + '.rigPart'), (rigPart + '.poleVector'), f=1)
		
		cmds.addAttr(chain, longName='rigPart', attributeType='message', s=1)
		cmds.connectAttr((chain + '.rigPart'), (rigPart + '.poleVector'), f=1)
			
		#RELOAD TREE
		cmds.select(oldSel)
		self.refreshTree()
	
	def makeOrient(self):
		oldSel = cmds.ls(sl=1)
		
		parts = self.longNamesFromTree()
		
		driver = parts[0]
		parts.pop(0)
		moCHK = self.ui.moCHK.isChecked()
		
		for part in parts:
			orient = cmds.orientConstraint(driver, part, mo=moCHK, name=(part.split('|')[-1] + '_orient'))[0]
			if not self.attrExists(orient,'rigParts'): cmds.addAttr(orient, longName='rigParts', attributeType='message', s=1)
			if not self.attrExists(driver, 'tagOrientDriven'): cmds.addAttr(driver, longName='tagOrientDriven', attributeType='message', s=1)
			if not self.attrExists(part,'tagOrientDriver'): cmds.addAttr(part, longName='tagOrientDriver', attributeType='message', s=1)
			cmds.connectAttr((part + '.tagOrientDriver'), (driver + '.tagOrientDriven'), f=1)
		
		#RELOAD TREE
		cmds.select(oldSel)
		self.refreshTree()
	
	def makePoint(self):
		oldSel = cmds.ls(sl=1)
		
		parts = self.longNamesFromTree()
		
		driver = parts[0]
		parts.pop(0)
		moCHK = self.ui.moCHK.isChecked()
		
		for part in parts:
			point = cmds.pointConstraint(driver, part, mo=moCHK, name=(part.split('|')[-1] + '_point'))[0]
			if not self.attrExists(point,'rigParts'): cmds.addAttr(point, longName='rigParts', attributeType='message', s=1)
			if not self.attrExists(driver, 'tagPointDriven'): cmds.addAttr(driver, longName='tagPointDriven', attributeType='message', s=1)
			if not self.attrExists(part,'tagPointDriver'): cmds.addAttr(part, longName='tagPointDriver', attributeType='message', s=1)
			cmds.connectAttr((part + '.tagPointDriver'), (driver + '.tagPointDriven'), f=1)
		
		#RELOAD TREE
		cmds.select(oldSel)
		self.refreshTree()