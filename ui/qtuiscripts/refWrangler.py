import os

import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic

def show():
	return refWrangler()

class refWrangler(QtGui.QMainWindow):
	iconLib = {}
	iconPath = os.environ.get('MAYA_LOCATION', None) + '/icons/'
	iconLib['file'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'render_mib_geo_cube.png'))

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		#pathing: home, local office, network
		uiPath = None
		try: uiPath = (os.path.dirname(str(__file__)) + '/refWrangler.ui').replace('/','\\')
		except: uiPath = 'X:\\projects\\2011\\crytek\\Tools\\CryMayaTools\\CryCore\\refWrangler\\refWrangler.ui'

		self.ui = uic.loadUi(uiPath)
		self.ui.show()
		self.cache = {}
		
		self.refreshTree()
		self.connect(self.ui.refreshBTN, QtCore.SIGNAL("clicked()"), self.refreshTree)
		self.connect(self.ui.filterBTN, QtCore.SIGNAL("clicked()"), self.filterTree)
		self.connect(self.ui.expandBTN, QtCore.SIGNAL("clicked()"), self.expandTree)
		
		#set the context menu policy, add context menu
		self.ui.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.tree.customContextMenuRequested.connect(self.openMenu)

	def updateDictList(self, key, value, dict):
		filterText = self.ui.filterLINE.text()
		if filterText != '':
			if filterText in value:
				if key in dict: dict[key].append(value)
				else: dict[key] = [value]
		else:
			if key in dict: dict[key].append(value)
			else: dict[key] = [value]
	
	
	def getRefs(self, rFile):
		edits = cmds.referenceQuery(rFile, es=1, successfulEdits=1, dagPath=0)
		fails = cmds.referenceQuery(rFile, es=1, failedEdits=1, successfulEdits=0)
		print 'successful edits:', len(edits)
		print 'failed edits:', len(fails)
		editTypes = {}
		for edit in edits:
			type = str(edit.split(' ')[0])
			if type in editTypes: editTypes[type].append(edit)
			else: editTypes[type] = [edit]
				
		failTypes = {}
		for fail in fails:
			type = str(fail.split(' ')[0])
			if type in failTypes: failTypes[type].append(fail)
			else: failTypes[type] = [fail]
			
		return [editTypes, failTypes]
	
	def divideUpLines(self, lines, node=1):
		if node:
			nodeDict = {}
			for line in lines:
				split = line.split(' ')
				if split[0] == 'addAttr':
					name = split[-1]
					self.updateDictList(name, line, nodeDict)
				if split[0] == 'setAttr':
					name = split[1].split('.')[0]
					self.updateDictList(name, line, nodeDict)
				if split[0] == 'connectAttr':
					name1 = split[1].split('.')[0].replace('"','')
					name2 = split[2].split('.')[0].replace('"','')
					self.updateDictList(name1, line, nodeDict)
					self.updateDictList(name2, line, nodeDict)
			return nodeDict
	
	def formatName(self, name):
		if self.ui.showDagCHK.isChecked() == True: pass
		else: name = name.split('|')[-1]
		return name
	
	def formatLine(self, line):
		split = line.split(' ')
		if split[0] == 'addAttr':
			if self.ui.showDagCHK.isChecked() == True: pass
			else: line = line.replace(split[-1],split[-1].split('|')[-1])
		if split[0] == 'setAttr':
			if self.ui.showDagCHK.isChecked() == True: pass
			else: line = line.replace(split[1],split[1].split('|')[-1])
		return line


## UI RELATED
####################
	def filterTree(self):
		self.refreshTree(full=0)
		
	def expandTree(self):
		self.ui.tree.expandAll()
	
	def openMenu(self, position):
		menu = QtGui.QMenu()
		delete = menu.addAction("Delete Selected Edits")
		action = menu.exec_(self.ui.tree.mapToGlobal(position))
		self.timeRange = [0,0]
		if action == delete:
			#currently passes single, needs to query selection
			item = self.ui.tree.itemAt(position)
			print 'deleting',item
	
	def refreshTree(self, full=1):
		self.ui.tree.clear()
		
		refs = cmds.file(q=1,r=1)
		
		for ref in refs:
			
			refFile = ref.split('/')[-1]
			
			#ADD TOP LEVEL ITEMS (NODES)
			wid1 = QtGui.QTreeWidgetItem()
			nameSpace = cmds.file(ref, q=1, namespace=1)
			self.ui.tree.setColumnCount(1)
			wid1.setText(0,('[' + nameSpace + '] ' + refFile))
			
			wid1.setData(0,32,str(ref))
			wid1.setIcon(0, self.iconLib['file'])
			self.ui.tree.addTopLevelItem(wid1)
			
			data = None
			if full == 0 and self.cache[ref]:
				data = self.cache[ref]
			else:
				data = self.getRefs(ref)
				self.cache[ref] = data
			
			#successful edits
			successColor = QtGui.QColor(120,175,255,200)
			font = wid1.font(0)
			font.setPointSize(10)
			wid2 = QtGui.QTreeWidgetItem()
			wid2.setTextColor(0,successColor)
			wid2.setText(0, 'Reference Edits')
			wid2.setFont(0,font)
			wid1.addChild(wid2)
			for type in data[0]:
				font = wid1.font(0)
				font.setPointSize(9)
				wid3 = QtGui.QTreeWidgetItem()
				typeColor = QtGui.QColor(210,210,210,200)
				wid3.setTextColor(0,typeColor)
				wid3.setText(0, type)
				wid3.setFont(0,font)
				wid2.addChild(wid3)
				
				parsed = self.divideUpLines(data[0][type])
				for item in sorted(parsed.keys()):
					font = wid1.font(0)
					font.setPointSize(8)
					#force no bold, since bold is inheritted
					font.setWeight(QtGui.QFont.Normal)
					wid4 = QtGui.QTreeWidgetItem()
					wid4.setText(0, self.formatName(item))
					wid4.setFont(0,font)
					wid3.addChild(wid4)
					for line in parsed[item]:
						font = wid1.font(0)
						#force no bold, since bold is inheritted
						font.setWeight(QtGui.QFont.Normal)
						font.setPointSize(8)
						wid5 = QtGui.QTreeWidgetItem()
						wid5.setText(0, self.formatLine(line))
						wid5.setFont(0,font)
						wid4.addChild(wid5)
					
				
			#failed edits
			failedColor = QtGui.QColor(255,80,80,150)
			font = wid1.font(0)
			font.setPointSize(10)
			wid2 = QtGui.QTreeWidgetItem()
			wid2.setTextColor(0,failedColor)
			wid2.setText(0, 'Failed Edits')
			wid2.setFont(0,font)
			wid1.addChild(wid2)
			for type in data[1]:
				font = wid1.font(0)
				font.setPointSize(9)
				wid3 = QtGui.QTreeWidgetItem()
				typeColor = QtGui.QColor(210,210,210,200)
				wid3.setTextColor(0,typeColor)
				wid3.setText(0, type)
				wid3.setFont(0,font)
				wid2.addChild(wid3)
				
				parsed = self.divideUpLines(data[1][type])
				for item in sorted(parsed.keys()):
					font = wid1.font(0)
					font.setPointSize(8)
					#force no bold, since bold is inheritted
					font.setWeight(QtGui.QFont.Normal)
					wid4 = QtGui.QTreeWidgetItem()
					wid4.setText(0, self.formatName(item))
					wid4.setFont(0,font)
					wid3.addChild(wid4)
					for line in parsed[item]:
						font = wid1.font(0)
						#force no bold, since bold is inheritted
						font.setWeight(QtGui.QFont.Normal)
						font.setPointSize(8)
						wid5 = QtGui.QTreeWidgetItem()
						wid5.setText(0, self.formatLine(line))
						wid5.setFont(0,font)
						wid4.addChild(wid5)