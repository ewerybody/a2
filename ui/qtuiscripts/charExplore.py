import os, sip

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as mui
from PyQt4 import QtGui, QtCore, uic

from CryRigging import charParts as cp
from CryRigging import rigParts as rp
import CryRigging as cr
import CryCore as cc

def getMayaWindow():
	#'Get the maya main window as a QMainWindow instance'	
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

#pathing: home, local office, network
uiPath = None
try: uiPath = (os.path.dirname(str(__file__)) + '/charExplore.ui').replace('/','\\')
except: uiPath = 'X:\\projects\\2011\\crytek\\Tools\\CryMayaTools\\CryRigging\\charExplore\\charExplore.ui'
#except: uiPath = 'J:\\data\\Production\\TechArt\\Builds\\Latest\\Tools\\CryMayaTools\\CryRigging\\rigTools\\rigTools.ui'
form_class, base_class = uic.loadUiType(uiPath)

class rigTools(base_class, form_class):
	#not working when i place in the __init__, no one knows why
	iconLib = {}
	iconPath = (os.environ.get('MAYA_LOCATION', None) + '/icons/')
	filePath = os.path.realpath(__file__)
	localIconPath = (filePath.replace(filePath.split('\\')[-1], '') + 'icons\\')
	classCache = {}
	
	iconLib['joint'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'joint.png'))
	iconLib['ikHandle'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'kinHandle.png'))
	iconLib['transform'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'transform.png'))
	iconLib['pv'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'pointlight.png'))
	iconLib['constraint'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'constraint.png'))
	#iconLib['character'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'mayaHIK/HIKCharacterToolSkeleton.png'))
	iconLib['rigging'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'smallTrash.png'))
	iconLib['cryped'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'cryped.png'))
	iconLib['skeleton'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'skeleton.png'))
	iconLib['SKIN'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'SKIN.png'))
	iconLib['SKEL'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'SKEL.png'))
	iconLib['charPart'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'charPart.png'))
	iconLib['character'] = QtGui.QIcon(QtGui.QPixmap(localIconPath + 'character.png'))
	
	red = QtGui.QColor(255,0,0,200)
	softRed = QtGui.QColor(235,70,70,240)
	yellow = QtGui.QColor(255,255,17,200)
	blue = QtGui.QColor(75,136,211,255)
	green = QtGui.QColor(70,240,104,255)
	
	p4Cache = {}
	meshDict = {}
	
	def __init__(self, parent= getMayaWindow()):
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		
		self.refreshUI()
		self.connect(self.refreshBTN, QtCore.SIGNAL("clicked()"), self.refreshTree)
		#refresh on tab changed
		self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.refreshUI)
		self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.tree, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.openMenu)
		#self.tree.customContextMenuRequested.connect(self.openMenu)
		
		#explore tree
		self.connect(self.showEmptyCHK, QtCore.SIGNAL("stateChanged(int)"), self.refreshUI)
		
		#toolbox functions
		self.connect(self.refreshCharNodesBTN, QtCore.SIGNAL("clicked()"), self.refreshUI)
		self.connect(self.createClassBTN, QtCore.SIGNAL("clicked()"), self.createClass)
		self.classTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.classTree, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.openClassMenu)
		self.connect(self.deleteClassBTN, QtCore.SIGNAL("clicked()"), self.deleteClass)
		self.connect(self.addMeshesToClassBTN, QtCore.SIGNAL("clicked()"), self.addMeshesToClassFn)
		self.connect(self.updateControllerDefaultsBTN, QtCore.SIGNAL("clicked()"), self.updateControllerDefaultsFn)
		self.connect(self.findTexturesP4BTN, QtCore.SIGNAL("clicked()"), self.findTexturesP4Fn)
		self.connect(self.validateBTN, QtCore.SIGNAL("clicked()"), self.validateFn)
		self.connect(self.connectSelectedItemAsBTN, QtCore.SIGNAL("clicked()"), self.connectSelectedItemAsFn)
		
		#batch export
		self.connect(self.checkoutBTN, QtCore.SIGNAL("clicked()"), self.checkoutFn)
		
		#rig update and scene validation
		self.connect(self.updateRigBTN, QtCore.SIGNAL("clicked()"), self.updateRigFn)
		
		self.generateMeshDict()


	def getConnections(self, attr):
		try:
			return cmds.listConnections(attr, d=1)
		except ValueError:
			return None
			
	def getLatestVersion(self, module, fn):
		'''
		Takes two strings, of module and function, returns the float version of the function if it has this as a last default
		'''
		execLine = module + '.' + fn + '.func_defaults[-1]'
		try:
			ver = eval(execLine)
			if type(ver) == float: return ver
			else:
				print 'getLatestVersion>>>', fn, 'has no version info.'
				return False
		except AttributeError:
			print 'getLatestVersion>>>', 'No function named:', fn
			return False

	def getMeshExportProperties(self, mesh, debug=1):
		'''
		Returns a dict of the mesh's export properties
		'''
		dict = {}
		if not cc.isMesh(mesh):
			return cmds.error(mesh + ' is not a render mesh!')
		exportNode = cmds.listRelatives(cmds.listRelatives(mesh, p=1), p=1)
		if exportNode:
			exportNode = exportNode[0]
			if 'cryExportNode' in exportNode:
				dict['exportNode'] = exportNode
				
				type = cmds.getAttr(exportNode + '.fileType')
				if type == 0: dict['fileType'] = 'cgf'
				if type == 1: dict['fileType'] = 'chr'
				if type == 2: dict['fileType'] = 'cga'
				if type == 3: dict['fileType'] = 'skin'
				
				if cr.attrExists(exportNode, 'DoNotMerge'): dict['DoNotMerge'] = cmds.getAttr(exportNode + '.DoNotMerge')
				if cr.attrExists(exportNode, 'WriteVertexColours'): dict['WriteVertexColours'] = cmds.getAttr(exportNode + '.WriteVertexColours')
				if cr.attrExists(exportNode, 'WriteAsSubdivisionMesh'): dict['WriteAsSubdivisionMesh'] = cmds.getAttr(exportNode + '.WriteAsSubdivisionMesh')
				if cr.attrExists(exportNode, 'UseF32VertexFormat'): dict['UseF32VertexFormat'] = cmds.getAttr(exportNode + '.UseF32VertexFormat')
				
				return dict
			else:
				if debug: print '>>>charExplorer: TOP NODE NOT EXPORT NODE:', exportNode, 'mesh:',mesh
				return False
		else:
			if debug: print '>>>charExplorer: NO EXPORT NODE:', exportNode, 'mesh:',mesh
			return False

	def generateMeshDict(self, debug=0):
		chars = cmds.ls(type='cryCharacter')
		for char in chars:
			if cr.attrExists(char, 'classes'):
				for cls in cmds.attributeQuery('classes', n=char, lc=1):
					for lod in cmds.attributeQuery(cls, n=char, lc=1):
						attr = char + '.' + 'classes' + '.' + cls + '.' + lod
						if lod:
							conns = self.getConnections(attr)
							if conns:
								for mesh in conns:
									self.meshDict[mesh] = self.getMeshExportProperties(mesh)
							else:
								if debug: print '>>>charExplorer: Meshes not found for:', char, cls, lod, attr
								#if debug: print locals()
			else: return False
			
	
	def p4FileInfo(self, asset, root='//data/Games/Freedom/dev/GameRyse', debug=0):
		from P4 import P4, P4Exception
		p4 = P4()
		try: p4.connect()
		except:
			print 'Cannot connect!'
			return False
		try:
			file =  p4.run_files(root + '...' + asset)
			depotLoc = file[0]['depotFile']
			describe = p4.run_describe(file[0]['change'])
			return [describe[0]['user'], depotLoc, describe[0]['desc'], file[0]['change']]
		except Exception as e:
			print "Cannot find file.", asset
			if debug: print e
			return False
		finally:
			p4.disconnect()
			
	def generateClassCache(self):
		for char in cmds.ls(type='cryCharacter'):
			lodDict = {}
			if cr.attrExists(char, 'classes'):
				for c in cmds.attributeQuery('classes', node=char, lc=1):
					lods = {}
					for lod in cmds.attributeQuery(c, node=char, lc=1):
						attr = char + '.' + 'classes' + '.' + c + '.' + lod
						conns = self.getConnections(attr)
						if conns:
							lods[lod] = conns
					lodDict[c] = lods
					
			self.classCache[char] = lodDict
				
		

## UI RELATED
####################
	
	def refreshUI(self, index=None, debug=0):
		if not index: index = self.tabWidget.currentIndex()
		
		if index == 0:
			self.refreshTree()
			if debug: print '>>>charExplorer: Refreshing character view'
		if index == 1:
			self.generateMeshDict()
			self.refreshExportTree()
			if debug: print '>>>charExplorer: Refreshing export view'
		if index == 2:
			self.refreshToolbox()
			if debug: print '>>>charExplorer: Refreshing toolbox view'
		if index == 3:
			self.refreshRigUpdate()
			if debug: print '>>>charExplorer: Refreshing rig update view'
	
	def openMenu(self, position):
		menu = QtGui.QMenu()
		select = menu.addAction("Select")
		pos = self.tree.mapToGlobal(position)
		action = menu.exec_(pos)
		if action == select:
			selectMe = []
			for index in self.tree.selectedIndexes():
				selectMe.append(self.tree.itemFromIndex(index).text(0))
			cmds.select(selectMe)
			
			#No longer select item
			'''
			item = self.tree.itemAt(position)
			if item:
				name = str(item.text(0))
				if ': ' in name: name = name.split(': ')[-1]
				if cmds.objExists(name): cmds.select(name)
				else:
					cmds.warning(('>>>charExplorer: No node in scene matches: ' + name))
			'''
	
	def refreshToolbox(self, debug=0):
		self.charactersCMB.clear()
		self.generateClassCache()
		self.classTree.setColumnCount(2)
		
		#TODO: don't blow away item selection on refreshing
		#selectedTreeItem = self.classTree.selectedItems()
		self.classTree.clear()
		
		for char in self.classCache.keys():
			self.charactersCMB.addItem(char)
			
			#classTree
			if cr.attrExists(char, 'classes'):
				for cls in cmds.attributeQuery('classes', n=char, lc=1):
					wid1 = QtGui.QTreeWidgetItem()
					wid1.setText(0, cls)
					self.classTree.addTopLevelItem(wid1)
					for lod in cmds.attributeQuery(cls, n=char, lc=1):
						wid2 = QtGui.QTreeWidgetItem()
						wid2.setText(0, lod)
						if debug:
							print char, cls, lod
							print self.classCache
							print self.classCache[char]
							print self.classCache[char][cls]
							print self.classCache[char][cls].keys()
						if lod in self.classCache[char][cls].keys():
							wid2.setText(1, ('Meshes: ' + str(len(self.classCache[char][cls][lod]))))
						else:
							wid2.setText(1, 'Meshes: 0')
						wid1.addChild(wid2)
		self.classTree.expandAll()
		self.classTree.header().resizeSections(QtGui.QHeaderView.ResizeToContents)
		
	
	def refreshExportTree(self, debug=1):
		self.exportTree.clear()
		
		chars = cmds.ls(type='cryCharacter')
		
		for char in chars:
			#ADD TOP LEVEL ITEMS (NODES)
			wid1 = QtGui.QTreeWidgetItem()
			
			name = char
			
			self.exportTree.setColumnCount(3)
			wid1.setText(0, name)
			
			font = wid1.font(0)
			font.setPointSize(10)
			wid1.setFont(0,font)
			
			wid1.setData(0,32,str(char))
			wid1.setIcon(0, self.iconLib['skeleton'])
			self.exportTree.addTopLevelItem(wid1)
			
			if cr.attrExists(char, 'classes'):
				for cls in cmds.attributeQuery('classes', n=char, lc=1):
					font = wid1.font(0)
					#force no bold, since bold is inheritted
					font.setPointSize(10)
					wid2 = QtGui.QTreeWidgetItem()
					wid2.setText(0, cls)
					wid2.setFont(0,font)
					wid1.addChild(wid2)
					
					for lod in cmds.attributeQuery(cls, n=char, lc=1):
						font.setWeight(QtGui.QFont.Normal)
						font.setPointSize(8)
						wid3 = QtGui.QTreeWidgetItem()
						wid3.setText(0, lod.split('_')[-1])
						wid3.setFont(0,font)
						wid2.addChild(wid3)
						
						attr = char + '.' + 'classes' + '.' + cls + '.' + lod
						connections = self.getConnections(attr)
						if connections:
							for mesh in connections:
								font.setWeight(QtGui.QFont.Normal)
								font.setPointSize(8)
								wid4 = QtGui.QTreeWidgetItem()
								wid4.setText(0, mesh)
								wid4.setFont(0,font)
								wid3.addChild(wid4)
								
								#check if somehow non-mesh was connected
								if not cc.isMesh(mesh):
									wid4.setText(0, mesh) 
									wid4.setText(1, ('ERROR: ' + mesh + ' IS NOT A MESH!'))
									wid4.setTextColor(0,self.red)
									wid4.setTextColor(1,self.red)
									continue
								
								assetName = 'NONE'
								if mesh in self.meshDict.keys():
									if debug: print  self.meshDict[mesh], mesh, '\n' + str(self.meshDict.keys())
									if self.meshDict[mesh]:
										assetName = (mesh + '.' + self.meshDict[mesh]['fileType'])
									else:
										cmds.warning(mesh + ' has no fileType, possibly does not exist on disk.')
								if mesh not in self.p4Cache.keys():
									#TODO dump this info in the temp folder, use it later
									self.p4Cache[mesh] = self.p4FileInfo(assetName)
									
								p4Info = self.p4Cache[mesh]
								if p4Info:
									wid4.setText(2, p4Info[0])
									wid4.setToolTip(1, p4Info[2])
									asset = p4Info[1]
									wid4.setText(1, p4Info[1])
									if asset.split('.')[-1].lower() == 'skin':
										#wid4.setIcon(0, self.iconLib['SKIN'])
										wid4.setTextColor(0,self.blue)
										wid4.setTextColor(1,self.blue)
									if asset.split('.')[-1].lower() == 'chr':
										#wid4.setIcon(0, self.iconLib['SKEL'])
										wid4.setTextColor(0,self.green)
										wid4.setTextColor(1,self.green)
								else:
									print '>>>charExplorer: Type returned is not string', p4Info
									wid4.setText(0, mesh) 
									wid4.setText(1, (assetName + ' cannot be found in Perforce!'))
									wid4.setTextColor(0,self.red)
									wid4.setTextColor(1,self.red)
						else:
							wid3.setText(0, lod.split('_')[-1] + ' has no LODs!')
							wid3.setTextColor(0,self.yellow)
		self.exportTree.header().resizeSections(QtGui.QHeaderView.ResizeToContents)
		self.exportTree.expandAll()


	def refreshTree(self, debug=1):
		self.tree.clear()
		self.showEmpty = self.showEmptyCHK.isChecked()
		
		chars = cmds.ls(type='cryCharacter')
		if debug: print chars
		for char in chars:
			if debug: print char
			name = None
			if self.shortNamesCHK.isChecked() == True: name = char
			if self.shortNamesCHK.isChecked() == False: name = globals.longName(char)
			
			#ADD TOP LEVEL ITEMS (NODES)
			wid1 = QtGui.QTreeWidgetItem()
			
			font = wid1.font(0)
			font.setPointSize(15)
			
			#self.tree.setColumnCount(4)
			wid1.setText(0,name)
			
			wid1.setData(0,32,('CryCharacter: ' + str(char)))
			wid1.setIcon(0, self.iconLib['character'])
			charVersion = cmds.getAttr(char + '.version')
			wid1.setText(1, str(charVersion))
			self.tree.addTopLevelItem(wid1)
			wid1.setExpanded(True)
			wid1.setFont(0,font)
			
			#ADD CHILDREN (MARKED ATTRS)
			#---------------------------
			
			font = wid1.font(0)
			font.setPointSize(10)
			
			#character attrs
			charType = QtGui.QTreeWidgetItem()
			typeTxt = 'None'
			tNew = cmds.getAttr(char + '.characterType')
			if tNew: typeTxt = tNew
			charType.setText(0, ('TYPE: ' + typeTxt))
			wid1.addChild(charType)
			
			locator = QtGui.QTreeWidgetItem()
			locator.setText(0, 'LOCATOR: NONE')
			loc = self.getConnections(char + '.locomotion_locator')
			if not loc and self.showEmpty == False: pass
			else: 
				if loc: locator.setText(0, ('LOCATOR: ' + loc[0]))
				wid1.addChild(locator)
			
			#TODO: Add the same code for anim and export skel as for locator and global ctrl (dont show if nothing present)
			exportSkel = QtGui.QTreeWidgetItem()
			exportSkel.setText(0, 'EXPORT ROOT: NONE')
			eSkel = cr.getConnections(char + '.exportSkeletonRoot')
			if eSkel: exportSkel.setText(0, ('EXPORT ROOT: ' + eSkel[0]))
			wid1.addChild(exportSkel)
			
			animSkel = QtGui.QTreeWidgetItem()
			animSkel.setText(0, 'ANIM ROOT: NONE')
			aSkel = cr.getConnections(char + '.animSkeletonRoot')
			if aSkel: animSkel.setText(0, ('ANIM ROOT: ' + aSkel[0]))
			wid1.addChild(animSkel)
			
			globalControl = QtGui.QTreeWidgetItem()
			globalControl.setText(0, 'GLOBAL CTRL: NONE')
			gCont = cr.getConnections(char + '.globalCtrl')
			if not gCont and self.showEmpty == False: pass
			else: 
				if gCont: globalControl.setText(0, ('GLOBAL CTRL: ' + gCont[0]))
				wid1.addChild(globalControl)
			
			#spaces
			spaces = eval(cmds.getAttr(char + '.spaces'))
			spWid = QtGui.QTreeWidgetItem()
			spWid.setText(0, 'SPACES (' + str(len(spaces)) + ')')
			wid1.addChild(spWid)
			spWid.setIcon(0, self.iconLib['transform'])
			if spaces:
				for space in spaces.keys():
					wid2 = QtGui.QTreeWidgetItem()
					text = None
					if spaces[space]:
						text = space + ' : ' + spaces[space]
					else:
						text = space + ' : None'
					wid2.setText(0, text)
					spWid.addChild(wid2)
			
			#attachments
			attWid = QtGui.QTreeWidgetItem()
			atts = cmds.listConnections(char + '.attachments')
			num = 0
			if atts: num = len(atts)
			if num == 0 and self.showEmpty == False: pass
			else:
				attWid.setText(0, ('ATTACHMENT POINTS (' + str(num) +')'))
				wid1.addChild(attWid)
				if atts:
					for att in atts:
						wid2 = QtGui.QTreeWidgetItem()
						wid2.setText(0, att)
						attWid.addChild(wid2)
			
			#rig updates
			rups = eval(cmds.getAttr(char + '.rigUpdates'))
			rupWid = QtGui.QTreeWidgetItem()
			num = 0
			if rups: num = len(rups)
			if num == 0 and self.showEmpty == False: pass
			else:
				rupWid.setText(0, 'RIG UPDATES (' + str(num) + ')')
				wid1.addChild(rupWid)
				if rups:
					for rup in rups:
						wid2 = QtGui.QTreeWidgetItem()
						wid2.setText(0, rup)
						rupWid.addChild(wid2)
			
			#ghost joints
			gjs = cmds.listConnections(char + '.ghostJoints')
			gWid = QtGui.QTreeWidgetItem()
			num = 0
			if gjs: num = len(gjs)
			if num == 0 and self.showEmpty == False: pass
			else:
				gWid.setText(0, ('GHOST JOINTS (' + str(num) +')'))
				wid1.addChild(gWid)
				if gjs:
					blendWeightVertex = []
					blendWeightMap = []
					other = []
					for gj in gjs:
						if 'blendWeightVertex' in gj: blendWeightVertex.append(gj)
						elif 'blendWeightMap' in gj: blendWeightMap.append(gj)
						else: other.append(gj)
					
					wid4 = QtGui.QTreeWidgetItem()
					wid4.setText(0, ('Other (' + str(len(other)) + ')'))
					gWid.addChild(wid4)
					for gj in other:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, gj)
						wid4.addChild(_wid)
					
					wid3 = QtGui.QTreeWidgetItem()
					wid3.setText(0, ('BlendWeightMap (' + str(len(blendWeightMap)) + ')'))
					gWid.addChild(wid3)
					for gj in blendWeightMap:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, gj)
						wid3.addChild(_wid)
						
					wid2 = QtGui.QTreeWidgetItem()
					wid2.setText(0, ('BlendWeightVertex (' + str(len(blendWeightVertex)) + ')'))
					gWid.addChild(wid2)
					for gj in blendWeightVertex:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, gj)
						wid2.addChild(_wid)
			
			#helper jnts
			classJnts = cmds.listConnections(char + '.classHlpJnts')
			sharedJnts = cmds.listConnections(char + '.sharedHlpJnts')
			charJnts = cmds.listConnections(char + '.charHlpJnts')
			topWid = QtGui.QTreeWidgetItem()
			num = 0
			if classJnts: num += len(classJnts)
			if sharedJnts: num += len(sharedJnts)
			if charJnts: num += len(charJnts)
			if num == 0 and self.showEmpty == False: pass
			else:
				topWid.setText(0, ('HELPER JOINTS (' + str(num) +')'))
				wid1.addChild(topWid)
				if classJnts:
					wid4 = QtGui.QTreeWidgetItem()
					wid4.setText(0, ('Class Helper Joints (' + str(len(classJnts)) + ')'))
					topWid.addChild(wid4)
					for jnt in classJnts:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, jnt)
						wid4.addChild(_wid)
				if sharedJnts:
					wid3 = QtGui.QTreeWidgetItem()
					wid3.setText(0, ('Shared Helper Joints (' + str(len(sharedJnts)) + ')'))
					topWid.addChild(wid3)
					for jnt in sharedJnts:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, jnt)
						wid3.addChild(_wid)
				
				if charJnts:
					wid2 = QtGui.QTreeWidgetItem()
					wid2.setText(0, ('Character Helper Joints (' + str(len(charJnts)) + ')'))
					topWid.addChild(wid2)
					for jnt in charJnts:
						_wid = QtGui.QTreeWidgetItem()
						_wid.setText(0, jnt)
						wid2.addChild(_wid)
					
			
			#cryped
			pedoBrown = QtGui.QColor(200,150,80,255)
			cryPed = QtGui.QTreeWidgetItem()
			cryPed.setText(0, 'cryPed Rig Modules')
			cryPed.setTextColor(0,pedoBrown)
			wid1.addChild(cryPed)
			cryPed.setExpanded(True)
			cryPed.setFont(0,font)
			cryPed.setIcon(0, self.iconLib['cryped'])
			
			attr = (char + '.charParts')
			charParts = cr.getConnections(attr, debug=0)
			if charParts:
				for charPart in charParts:
					partVersion = cmds.getAttr(charPart + '.version')
					partMethod = cmds.getAttr(charPart + '.method')
					latestVersion = None
					#TODO - Riham - we will later use an attr 'side' instead of encoding the side into the method name
					
					if partMethod:
						fnSplit = partMethod.split('_')
						if len(fnSplit) > 1:
							if fnSplit[0].lower() == 'r' or 'l':
								partMethod = partMethod.replace(partMethod[0:2], '')
						latestVersion = self.getLatestVersion('cp', partMethod)
					
					font = wid1.font(0)
					#force no bold, since bold is inheritted
					font.setPointSize(10)
					wid2 = QtGui.QTreeWidgetItem()
					wid2.setText(0, charPart)
					#TODO: somehow check for latest version
					wid2.setText(1, str(partVersion))
					wid2.setText(3, str(partMethod))
					
					if latestVersion: wid2.setText(2, str(latestVersion))
					else: wid2.setText(2, str('None'))
					
					wid2.setFont(0,font)
					wid2.setTextColor(0,pedoBrown)
					wid2.setIcon(0, self.iconLib['charPart'])
					cryPed.addChild(wid2)
					
					#check for version match
					if latestVersion != partVersion:
						wid2.setTextColor(1,self.softRed)
						wid2.setTextColor(2,self.softRed)
					
					bColor = QtGui.QColor(120,175,255,200)
					
					rigParts = cmds.listConnections((charPart + '.rigParts'), type='cryRigPart')
					if rigParts:
						for rigPart in cmds.listConnections((charPart + '.rigParts'), type='cryRigPart'):
							font.setWeight(QtGui.QFont.Normal)
							font.setPointSize(8)
							wid3 = QtGui.QTreeWidgetItem()
							wid3.setText(0, rigPart)
							wid3.setFont(0,font)
							wid2.addChild(wid3)	
							
							#IK CHAIN
							if cmds.getAttr(rigPart + '.partType') == 'ikChain':
								wid3.setIcon(0, self.iconLib['ikHandle'])
								
								#start joint
								wid_sj = QtGui.QTreeWidgetItem()
								wid_sj.setText(0, ('START>> ' + cmds.listConnections((rigPart + '.startJoint'), type='transform')[0]))
								wid_sj.setFont(0,font)
								wid_sj.setIcon(0, self.iconLib['joint'])
								wid3.addChild(wid_sj)
								#end joint
								wid_ej = QtGui.QTreeWidgetItem()
								wid_ej.setText(0, ('END>> ' + cmds.listConnections((rigPart + '.endJoint'), type='transform')[0]))
								wid_ej.setFont(0,font)
								wid_ej.setIcon(0, self.iconLib['joint'])
								wid3.addChild(wid_ej)
								#pole vector
								if cmds.attributeQuery('poleVector', n=rigPart, ex=1):
									wid_pv = QtGui.QTreeWidgetItem()
									wid_pv.setText(0, ('PV>> ' + cmds.listConnections((rigPart + '.poleVector'), type='transform')[0]))
									wid_pv.setFont(0,font)
									wid_pv.setIcon(0, self.iconLib['pv'])
									wid3.addChild(wid_pv)
							
							#CONSTRAINTS
							if cmds.getAttr(rigPart + '.partType'):
								if 'Constraint' in cmds.getAttr(rigPart + '.partType'):
									wid3.setIcon(0, self.iconLib['constraint'])
									wid_driver = QtGui.QTreeWidgetItem()
									wid_driver.setFont(0,font)
									wid_driver.setText(0, ('DRIVER>> ' + cmds.listConnections((rigPart + '.driver'), type='transform')[0]))
									wid_driven = QtGui.QTreeWidgetItem()
									wid_driven.setFont(0,font)
									wid_driven.setText(0, ('DRIVEN>> ' + cmds.listConnections((rigPart + '.driven'), type='transform')[0]))
									
									wid3.addChild(wid_driver)
									wid3.addChild(wid_driven)
							
							#add 'rigging' group
							wid4 = QtGui.QTreeWidgetItem()
							wid4.setTextColor(0,bColor)
							wid4.setText(0, 'PROCEDURAL RIGGING')
							wid4.setIcon(0, self.iconLib['rigging'])
							wid4.setFont(0,font)
							wid3.addChild(wid4)
							
							if cr.attrExists(rigPart, 'rigging'):
								for rigging in cmds.listConnections((rigPart + '.rigging')):
									wid5 = QtGui.QTreeWidgetItem()
									#color blue
									wid5.setTextColor(0,bColor)
									font.setPointSize(8)
									wid5.setText(0, rigging)
									wid5.setIcon(0, self.iconLib['transform'])
									wid5.setFont(0,font)
									wid4.addChild(wid5)
		
		#Add orphans
		orphans = cr.findOrphanModules()
		if orphans:
			#ADD TOP LEVEL ITEMS (NODES)
			wid1 = QtGui.QTreeWidgetItem()
			
			font = wid1.font(0)
			font.setPointSize(15)
			
			#self.tree.setColumnCount(4)
			wid1.setText(0,'ORPHANS')
			
			wid1.setIcon(0, self.iconLib['character'])
			charVersion = cmds.getAttr(char + '.version')
			wid1.setText(1, str(len(orphans)))
			self.tree.addTopLevelItem(wid1)
			wid1.setExpanded(True)
			wid1.setFont(0,font)
			
			for orphan in orphans:
				partVersion = 'None'
				try: partVersion = cmds.getAttr(orphan + '.version')
				except: pass
				partMethod = 'None'
				try: partMethod = cmds.getAttr(orphan + '.method')
				except: pass
				
				latestVersion = None
				#TODO - Riham - we will later use an attr 'side' instead of encoding the side into the method name
				
				if partMethod:
					fnSplit = partMethod.split('_')
					if len(fnSplit) > 1:
						if fnSplit[0].lower() == 'r' or 'l':
							partMethod = partMethod.replace(partMethod[0:2], '')
					latestVersion = self.getLatestVersion('cp', partMethod)
				
				font = wid1.font(0)
				#force no bold, since bold is inheritted
				font.setPointSize(10)
				wid2 = QtGui.QTreeWidgetItem()
				wid2.setText(0, orphan)
				#TODO: somehow check for latest version
				wid2.setText(1, str(partVersion))
				wid2.setText(3, str(partMethod))
				
				if latestVersion: wid2.setText(2, str(latestVersion))
				else: wid2.setText(2, str('None'))
				
				wid2.setFont(0,font)
				if cmds.nodeType(orphan) == 'cryCharPart': wid2.setIcon(0, self.iconLib['charPart'])
				if cmds.nodeType(orphan) == 'cryRigPart': wid2.setIcon(0, self.iconLib['transform'])
				wid1.addChild(wid2)
				
				#check for version match
				if latestVersion != partVersion:
					wid2.setTextColor(1,self.softRed)
					wid2.setTextColor(2,self.softRed)
				
				bColor = QtGui.QColor(120,175,255,200)
		
		self.tree.header().resizeSections(QtGui.QHeaderView.ResizeToContents)
		'''
		#SKEL LINK
		if cmds.attributeQuery('skelLink', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'skelLink', 'self.yellow', self.nameColumn, extraTxt='>> SKEL LINK >>  ')
		
		#IK CHAIN
		if cmds.attributeQuery('tagIkEnd', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagIkEnd', 'self.red', self.nameColumn, extraTxt='>> IK START >>  ')
		if cmds.attributeQuery('tagIkStart', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagIkStart', 'self.red', self.nameColumn, extraTxt='>> IK END >>  ')
		if cmds.attributeQuery('tagIkPv', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagIkPv', 'self.blue', self.nameColumn, extraTxt='>> IK PV >>  ')
			
		#CONSTRAINTS
		if cmds.attributeQuery('tagOrientDriven', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagOrientDriven', 'self.red', self.nameColumn, extraTxt='>> ORIENT CONST >>  ')
		if cmds.attributeQuery('tagOrientDriver', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagOrientDriver', 'self.red', self.nameColumn, extraTxt='>> ORIENT CONST >>  ')
		if cmds.attributeQuery('tagPointDriven', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagPointDriven', 'self.red', self.nameColumn, extraTxt='>> POINT CONST >>  ')
		if cmds.attributeQuery('tagPointDriver', n=node.fullPathName(), ex=1) == True:
			self.addTag(wid1, node, 'tagPointDriver', 'self.red', self.nameColumn, extraTxt='>> POINT CONST >>  ')
		'''
		#self.tree.expandAll()
	
	
	def checkoutFn(self):
		for item in self.exportTree.selectedItems():
			print item.text(1)
	
	
	############################################################
	## TOOLBOX 
	############################################################
	
	## CHARACTER CLASSES
	####################
	def createClass(self, debug=0):
		char = str(self.charactersCMB.currentText())
		className = str(self.classNameLINE.text())
		lodNum = self.lodSPIN.value()
		if debug: print char, className, lodNum
		classList = self.classCache[str(self.charactersCMB.currentText())].keys()
		classList.append(str(className))
		if debug: print classList
		cr.createCharClasses(char, classList, lodNum, deleteCls=0, debug=1)
		
		self.refreshToolbox()
	
	def deleteClass(self, debug=1, className=None):
		char = str(self.charactersCMB.currentText())
		if not className:
			className = self.classTree.selectedItems()[0].text(0)
		lodNum = self.lodSPIN.value()
		if debug: print char, className, lodNum
		classList = self.classCache[str(self.charactersCMB.currentText())].keys()
		cr.createCharClasses(char, [className], lodNum, deleteCls=1, debug=1)
		
		self.refreshToolbox()
	
	def addMeshesToClassFn(self):
		meshes = cmds.ls(sl=1, type=['mesh', 'transform'])
		char = str(self.charactersCMB.currentText())
		selectedLOD = str(self.classTree.selectedItems()[0].text(0))
		cls = selectedLOD.split('_')[0]
		attr = char + '.classes.' + cls + '.' + selectedLOD
		cr.connectMeshLODs(attr, meshes)
		
		self.refreshToolbox()
	
	def openClassMenu(self, position, debug=0):
		menu = QtGui.QMenu()
		delete = menu.addAction("Delete")
		pos = self.classTree.mapToGlobal(position)
		action = menu.exec_(pos)
		if action == delete:
			item = self.classTree.itemAt(position)
			if item:
				cls = str(item.text(0))
				if debug: print 'deleting', cls
				self.deleteClass(className=cls)
	
	## MISC UTILS
	####################
	def connectSelectedItemAsFn(self):
		char = str(self.charactersCMB.currentText())
		try:
			cmds.undoInfo(openChunk=True)
			
			connectAs = self.connectSelectedItemAsCMB.currentText()
			nodes = cmds.ls(sl=1)
			if connectAs == 'Attachment Joints':
				cr.connectMsgAttrs(char + '.attachments', nodes, 'attachments', rebuild=0)
			if connectAs == 'Class HLP JNT':
				for node in nodes:
					if cmds.nodeType(node) != 'joint':
						cmds.error(node + ' is not a Joint!')
						return False
				cr.connectMsgAttrs(char + '.classHlpJnts', nodes, 'hlpJnt', rebuild=0)
			if connectAs == 'Shared HLP JNT':
				for node in nodes:
					if cmds.nodeType(node) != 'joint':
						cmds.error(node + ' is not a Joint!')
						return False
				cr.connectMsgAttrs(char + '.sharedHlpJnts', nodes, 'hlpJnt', rebuild=0)
			if connectAs == 'Character HLP JNT':
				for node in nodes:
					if cmds.nodeType(node) != 'joint':
						cmds.error(node + ' is not a Joint!')
						return False
				cr.connectMsgAttrs(char + '.charHlpJnts', nodes, 'hlpJnt', rebuild=0)
			if connectAs == 'CTRL Shared':
				for node in nodes:
					##add shared attribute and set it
					if not rp.attrExists(node , "shared"):
						cmds.addAttr(node, longName='shared', at='bool', k = 0 , dv = 1)
					cmds.setAttr(node + '.shared', 1)
				cr.connectMsgAttrs(char + '.controllers', nodes, 'controller', rebuild=0)
			if connectAs == 'CTRL Unique':
				for node in nodes:
					if not rp.attrExists(node , "shared"):
						cmds.addAttr(node, longName='shared', at='bool', k = 0 , dv = 1)
					cmds.setAttr(node + '.shared', 0)
				cr.connectMsgAttrs(char + '.controllers', nodes, 'controller', rebuild=0)	
			if connectAs == 'Ghost Joint':
				for node in nodes:
					if cmds.nodeType(node) != 'joint':
						cmds.error(node + ' is not a Joint!')
						return False
					cr.connectMsgAttrs(char + '.ghostJoints', nodes, 'ghostJoint', rebuild=0)
			if connectAs == 'Solver':
				#TODO: type check for diff solver types
				cr.connectMsgAttrs(char + '.solvers', nodes, 'charSolver', rebuild=0)
			
		finally:
			cmds.undoInfo(closeChunk=True)
	
	def updateControllerDefaultsFn(self):
		character = char = str(self.charactersCMB.currentText())
		cr.addCharDefaults(character)
		
	def findTexturesP4Fn(self):
		import CryCore as cc
		cc.rePathFileNodesP4(searchPath='//data/Games/Freedom/dev/GameRyse/Objects/characters')

	## RIG UPDATE & VALIDATION
	####################
	
	def refreshRigUpdate(self):
		#update char node combo box
		self.rigUpdateCMB.clear()
		self.validateCMB.clear()
		chars = cmds.ls(type='cryCharacter')
		self.rigUpdateCMB.addItems(chars)
		self.validateCMB.addItems(chars)
	
	def updateRigFn(self):
		from CryRigging import rigUpdate as ru
		cryChar = str(self.rigUpdateCMB.currentText())
		updates = ru.updateRig(cryChar)
		n=0
		for u in updates:
			if u: n+=1
		self.updateRigTXT.append('<font size=4 color=#6cdf9f><b>' + str(n)+ ' RigUpdate Patches Applied to CryCharacter: \'' + str(cryChar) + '\'</b></font>')
		for update in updates:
			if update:
				for line in update:
					self.updateRigTXT.append(line)
	
	def validateFn(self):
		valList = cr.validate.runValidation(str(self.validateCMB.currentText()))
		self.validateTree.clear()
		for item in valList:
			if item:
				#ADD TOP LEVEL ITEMS (NODES)
				wid1 = QtGui.QTreeWidgetItem()
				
				wid1.setText(0, item[0])
				
				font = wid1.font(0)
				font.setPointSize(10)
				wid1.setFont(0,font)
				self.validateTree.addTopLevelItem(wid1)
				
				if item[1]:
					for node in item[1].keys():
						font = wid1.font(0)
						font.setPointSize(8)
						wid2 = QtGui.QTreeWidgetItem()
						wid2.setText(0, item[1][node])
						wid2.setFont(0,font)
						wid1.addChild(wid2)
			
def show():
	global rigTools_win
	try:
		rigTools_win.close()
	except:pass
	rigTools_win = rigTools()
	rigTools_win.show()
	return rigTools_win
		
		
		
		
		