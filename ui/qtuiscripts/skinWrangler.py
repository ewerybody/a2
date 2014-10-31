'''
skinWrangler
@author = Chris Evans
version = 1.6
'''


import maya.cmds as cmds
import os
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as mui
import sip

def show():
	return skinWrangler()

class skinWrangler(QtGui.QDialog):	
	currentMesh = None
	currentSkin = None
	currentInf = None
	currentVerts = None
	
	scriptJobNum = None
	copyCache = None
	
	previousColor = None
	
	jointLoc = None
	
	iconLib = {}
	iconPath = os.environ.get('MAYA_LOCATION', None) + '/icons/'
	iconLib['joint'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'kinJoint.png'))
	iconLib['ikHandle'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'kinHandle.png'))
	iconLib['transform'] = QtGui.QIcon(QtGui.QPixmap(iconPath + 'orientJoint.png'))
	
	def __init__(self):
		ptr = mui.MQtUtil.mainWindow()
		mayaMainWindow = sip.wrapinstance(long(ptr), QtCore.QObject)
		QtGui.QDialog.__init__(self, parent=mayaMainWindow)
		
		#pathing: home, local office, network
		uiPath = None
		try: uiPath = (os.path.dirname(str(__file__)) + '/skinWrangler.ui').replace('/','\\')
		#except: uiPath = 'X:\\projects\\2011\\crytek\\Tools\\CryMayaTools\\CryRigging\\skinWrangler\\skinWrangler.ui'
		except: uiPath = 'D:\\data\\data\\Production\\TechArt\\Builds\\Latest\\Tools\\CryMayaTools\\CryRigging\\skinWrangler\\skinWrangler.ui'
		uic.loadUi(uiPath, self)
		wName = mui.MQtUtil.fullName(long(sip.unwrapinstance(self)))
		
		## Connect UI
		###############
		self.connect(self.refreshBTN, QtCore.SIGNAL("clicked()"), self.refreshUI)
		
		#selection buttons
		self.connect(self.selShellBTN, QtCore.SIGNAL("clicked()"), self.selShellFn)
		self.connect(self.selGrowBTN, QtCore.SIGNAL("clicked()"), self.selGrowFn)
		self.connect(self.selShrinkBTN, QtCore.SIGNAL("clicked()"), self.selShrinkFn)
		self.connect(self.selLoopBTN, QtCore.SIGNAL("clicked()"), self.selLoopFn)
		self.connect(self.selPointsEffectedBTN, QtCore.SIGNAL("clicked()"), self.selPointsEffectedFn)
		
		#weight buttons
		self.connect(self.weightZeroBTN, QtCore.SIGNAL("clicked()"), self.weightZeroFn)
		self.connect(self.weightHalfBTN, QtCore.SIGNAL("clicked()"), self.weightHalfFn)
		self.connect(self.weightFullBTN, QtCore.SIGNAL("clicked()"), self.weightFullFn)
		self.connect(self.setWeightBTN, QtCore.SIGNAL("clicked()"), self.setWeightFn)
		self.connect(self.plusWeightBTN, QtCore.SIGNAL("clicked()"), self.plusWeightFn)
		self.connect(self.minusWeightBTN, QtCore.SIGNAL("clicked()"), self.minusWeightFn)
		self.connect(self.copyBTN, QtCore.SIGNAL("clicked()"), self.copyFn)
		self.connect(self.pasteBTN, QtCore.SIGNAL("clicked()"), self.pasteFn)
		self.connect(self.clampInfBTN, QtCore.SIGNAL("clicked()"), self.clampInfFn)
		self.connect(self.selectVertsWithInfBTN, QtCore.SIGNAL("clicked()"), self.selectVertsWithInfFn)
		self.connect(self.setAverageWeightBTN, QtCore.SIGNAL("clicked()"), self.setAverageWeightFn)
		self.connect(self.bindPoseBTN, QtCore.SIGNAL("clicked()"), self.bindPoseFn)
		self.connect(self.removeUnusedBTN, QtCore.SIGNAL("clicked()"), self.removeUnusedFn)
		
		#self.connect(self.jointLST, QtCore.SIGNAL('itemSelectionChanged()'), self.jointListSelChanged)
		self.connect(self.jointLST, QtCore.SIGNAL('currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)'), self.onItemChanged)
		self.connect(self.listAllCHK, QtCore.SIGNAL('stateChanged(int)'), self.listAllChanged)
		self.connect(self.nameSpaceCHK, QtCore.SIGNAL('stateChanged(int)'), self.cutNamespace)
		
		self.connect(self.filterLINE, QtCore.SIGNAL('returnPressed ()'), self.refreshUI)
		self.connect(self.filterBTN, QtCore.SIGNAL("clicked()"), self.refreshUI)
		
		#TOOLS TAB
		self.connect(self.jointOnBboxCenterBTN, QtCore.SIGNAL("clicked()"), self.jointOnBboxCenterFn)
		
		print 'skinWrangler initialized as', wName
		self.scriptJobNum = cmds.scriptJob(e=['SelectionChanged', 'crySkinWrangler.refreshUI()'], p=wName, kws=1)
		self.refreshUI()
		
	def closeEvent(self, e):
		print '[skinWrangler] Killing scriptJob (' + str(self.scriptJobNum) + ')'
		cmds.scriptJob( kill=self.scriptJobNum, force=1)

	def averageWeights(self, weights):
		total = 0.0
		for w in weights: total += w
		return total/len(weights)
	
	def findRelatedSkinCluster(self, skinObject):
		'''Python implementation of MEL command: http://takkun.nyamuuuu.net/blog/archives/592'''
		
		skinShape = None
		skinShapeWithPath = None
		hiddenShape = None
		hiddenShapeWithPath = None
	
		cpTest = cmds.ls( skinObject, typ="controlPoint" )
		if len( cpTest ):
			skinShape = skinObject
	
		else:
			rels = cmds.listRelatives( skinObject )
			if rels == None: return False
			for r in rels :
				cpTest = cmds.ls( "%s|%s" % ( skinObject, r ), typ="controlPoint" )
				if len( cpTest ) == 0:
					continue
	
				io = cmds.getAttr( "%s|%s.io" % ( skinObject, r ) )
				if io:
					continue
	
				visible = cmds.getAttr( "%s|%s.v" % ( skinObject, r ) )
				if not visible:
					hiddenShape = r
					hiddenShapeWithPath = "%s|%s" % ( skinObject, r )
					continue
	
				skinShape = r
				skinShapeWithPath = "%s|%s" % ( skinObject, r )
				break
	
		if skinShape:
			if len( skinShape ) == 0:
				if len( hiddenShape ) == 0:
					return None
		
				else:
					skinShape = hiddenShape
					skinShapeWithPath = hiddenShapeWithPath
	
		clusters = cmds.ls( typ="skinCluster" )
		for c in clusters:
			geom = cmds.skinCluster( c, q=True, g=True )
			for g in geom:
				if g == skinShape or g == skinShapeWithPath:
					return c
	
		return None
	

	## GET FROM SCENE
	####################
	def getSelected(self):
		#TODO check selection type that it really returns mesh
		msh = cmds.ls(sl=1, o=1)
		if msh:
			#cmds.ConvertSelectionToVertices()
			skin = self.findRelatedSkinCluster(msh[0])
			if not skin: return False
			self.currentSkin = skin
			self.currentMesh = msh[0]
			if cmds.selectMode(component=1, q=1):
				sel = cmds.ls(sl=1, flatten = 1)
				if sel:
					msh = msh[0]
					vtx = None
					if sel != msh:
						if sel:
							vtx = len(sel)
						else: vtx = 0
					self.currentVerts = sel
					
					if not skin: return False
					
					return sel, msh, vtx, skin
		else: return False
	
	def getAvgVertWeights(self, sel, skin):
		wDict = {}
		for jnt in cmds.skinCluster(skin, q=1, wi=1):
			amt = cmds.skinPercent(skin, sel, q=1, t=jnt)
			if amt > 0.0: wDict[jnt] = amt
		return wDict
		
	def vDictToTv(self, wDict):
		re = []
		for inf in wDict.keys():
			re.append((inf, wDict[inf]))
		return re
	
	## POLY SELECTION UI
	######################
	def selGrowFn(self):
		cmds.GrowPolygonSelectionRegion()
		self.refreshUI()
	def selShrinkFn(self):
		cmds.ShrinkPolygonSelectionRegion()
		self.refreshUI()
	def selShellFn(self):
		cmds.ConvertSelectionToShell()
		self.refreshUI()
	def selLoopFn(self):
		cmds.polySelectSp(loop=1)
		self.refreshUI()
	def selPointsEffectedFn(self):
		cmds.skinCluster(self.currentSkin, e=1, selectInfluenceVerts=self.currentInf)
	
	
	## JOINT LIST
	###############
	def onItemChanged(self, current, previous):
		#update current joint
		try:
			cmds.undoInfo( swf=0 )
			if previous:
				if previous: previous = str(previous.text(0))
			if current:
				current = str(current.text(0))
				self.currentInf = current
			else: self.currentInf = None
			
			if previous == 'MAKE A COMPONENT\n SELECTION ON\n SKINNED MESH': previous = None
			if current == 'MAKE A COMPONENT\n SELECTION ON\n SKINNED MESH': current = None
			
			#REMOVED COLORING UNTIL I CAN GET IT UNDER CONTROL
			'''#set coloring
			if previous:
					if self.previousColor:
						cmds.setAttr(previous + '.overrideEnabled', 1)
						cmds.setAttr(previous + '.overrideColor', self.previousColor)
					else:
						cmds.setAttr(previous + '.overrideEnabled', 0)
			if current:
					isOverride = cmds.getAttr(current + '.overrideEnabled')
					cmds.setAttr(current + '.overrideEnabled', 1)
					cmds.setAttr(current + '.overrideColor', 13)
					if isOverride: self.previousColor = cmds.getAttr(current + '.overrideColor')'''
			cmds.undoInfo( swf=1)
		except Exception as e:
			cmds.warning(e)
			cmds.undoInfo( swf=1)
	
	#deprecated, now using onItemChanged to get the previous and change some coloring
	def jointListSelChanged(self):
		joint = self.jointLST.selectedItems()
		if joint:
			self.currentInf = str(joint[0].text(0))
		else: self.currentInf = None
	
	def getJointFromList(self, jnt):
		for i in range(0, self.jointLST.topLevelItemCount()):
			item = self.jointLST.topLevelItem(i)
			if item.text(0) == jnt: return item
		return False
		
	def listAllChanged(self):
		self.refreshUI()
		
	def cutNamespace(self):
		self.refreshUI()
	
	## SKINNING FUNCTIONS
	########################
	def weightZeroFn(self):
		cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), 0.0])
		self.refreshUI()
	def weightHalfFn(self):
		cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), 0.5])
		self.refreshUI()
	def weightFullFn(self):
		cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), 1.0])
		self.refreshUI()
	def setWeightFn(self):
		cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), self.setWeightSpin.value()])
		self.refreshUI()
		
	def plusWeightFn(self):
		if self.currentInf:
			val = self.setWeightSpin.value()
			cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), val], r=1)
		else: cmds.warning('[skinWrangler] No influences/joints selected')
		print 'undo'
		self.refreshUI()
	
	def minusWeightFn(self):
		if self.currentInf:
			val = -self.setWeightSpin.value()
			cmds.skinPercent(self.currentSkin, self.currentVerts, tv=[str(self.currentInf), val], r=1)
		else: cmds.warning('[skinWrangler] No influences/joints selected')
		self.refreshUI()
	
	def copyFn(self):
		if self.copyBTN.isChecked() == True:
			self.copyBTN.setText('WEIGHTS COPIED')
			self.getSelected()
			self.copyCache = self.getAvgVertWeights(self.currentVerts, self.currentSkin)
			toolTip = ''
			for item in self.copyCache.keys():
				toolTip += (item + ' - ' + str("%.4f" % self.copyCache[item]) + '\n')
			self.copyBTN.setToolTip(toolTip)
		else:
			self.copyBTN.setText('COPY')
			self.copyBTN.setToolTip('')
			self.copyCache = None
		
	def pasteFn(self):
		self.getSelected()
		tvTuples = self.vDictToTv(self.copyCache)
		print '[skinWrangler] Pasting weights to current selection: ', tvTuples
		cmds.skinPercent(self.currentSkin, self.currentVerts, tv=tvTuples)
		self.refreshUI()
	
	def selectVertsWithInfFn(self):
		self.checkMaxSkinInfluences(self.currentMesh, self.selectVertsWithInfSPIN.value(), select=1)
	
	def setAverageWeightFn(self):
		cmds.undoInfo(openChunk=True)
		sel = cmds.ls(sl=1)
		cmds.ConvertSelectionToVertices()
		newSel = cmds.ls(sl=1, flatten=1)
		for vert in newSel:
			self.setAverageWeight(vert)
		self.clampInfluences(self.currentMesh, self.clampInfSPIN.value(), force=1)
		cmds.select(sel)
		cmds.undoInfo(closeChunk=True)
	
	def setAverageWeight(self, vtx):
		msh = vtx.split('.')[0]
		cmds.select(vtx)
		cmds.ConvertSelectionToEdges()
		cmds.ConvertSelectionToVertices()
		neighbors = cmds.ls(sl=1, flatten=1)
		neighbors.pop(neighbors.index(vtx))
		infList = {}
		skin = self.findRelatedSkinCluster(msh)
		for vert in neighbors:
			for jnt in cmds.skinCluster(skin, q=1, wi=1):
				amt = cmds.skinPercent(skin, vert, q=1, t=jnt)
				if amt > 0.0:
					if jnt in infList: infList[jnt].append(amt)
					else: infList[str(jnt)] = [amt]
		for inf in infList:
			total = None
			for w in infList[inf]:
				if not total: total = w
				else: total += w
			weight = total/len(infList[inf])
			cmds.skinPercent(self.currentSkin, vtx, tv=[str(inf), weight], nrm=1)
	
	def checkMaxSkinInfluences(self, node, maxInf, debug=1, select=0):
		'''Takes node name string and max influences int.
		From CG talk thread (MEL converted to Python, then added some things)'''
		
		cmds.select(cl=1)
		skinClust = self.findRelatedSkinCluster(node)
		if skinClust == "": cmds.error("checkSkinInfluences: can't find skinCluster connected to '" + node + "'.\n");
	
		verts = cmds.polyEvaluate(node, v=1)
		returnVerts = []
		if debug: print 'Verts:', verts
		for i in range(0,verts):
			inf= cmds.skinPercent(skinClust, (node + ".vtx[" + str(i) + "]"), q=1, v=1)
			activeInf = []
			for j in range(0,len(inf)):
				if inf[j] > 0.0: activeInf.append(inf[j])
			if len(activeInf) > maxInf:
				returnVerts.append(i)
		
		if select:
			for vert in returnVerts:
				cmds.select((node + '.vtx[' + str(vert) + ']'), add=1)
		
		return returnVerts
	
	def checkLockedInfluences(self, skinCluster):
		'''
		Check if provided skinCluster has locked influences
		'''
		influenceObjects = cmds.skinCluster(skinCluster,q=True, inf=True )
		for currentJoint in influenceObjects:
			if (cmds.skinCluster(skinCluster,q=True,lw=True, inf=currentJoint )):
				return True
		return False
	
	def clampInfFn(self):
		self.clampInfluences(self.currentMesh, self.clampInfSPIN.value(), force=1)
		
	def bindPoseFn(self):
		if self.currentSkin:
			bp = cmds.listConnections(self.currentSkin + '.bindPose', s=1)
			if len(bp) > 0: cmds.dagPose(bp[0], r=1)
			else: cmds.warning('Multiple bind poses detected: ' + str(bp))
		else: cmds.warning('No skin cluster loaded or mesh with skin cluster selected.')
	
	def removeUnusedFn(self):
		if self.currentSkin:
			cmds.skinCluster(self.currentMesh, removeUnusedInfluence=1)
			self.refreshUI()
		else: cmds.warning('No skin cluster loaded or mesh with skin cluster selected.')
	
	def clampInfluences(self, mesh, maxInf, debug=0, force=False):
		'''
		Sets max influences on skincluster of mesh / cutting off smallest ones
		'''
		skinClust = self.findRelatedSkinCluster(mesh)
	
		lockedInfluences = self.checkLockedInfluences(skinClust)
		doit = True
		if lockedInfluences:
			if force:
				self.unlockLockedInfluences(skinClust)
				cmds.warning('Locked influences were unlocked on skinCluster')
			else:
				doit = False
		
		if doit:
			verts = self.checkMaxSkinInfluences(mesh, maxInf)
			
			print 'pruneVertWeights>> Pruning', len(verts), 'vertices'
			
			for v in verts:
				infs = cmds.skinPercent(skinClust, (mesh + ".vtx[" + str(v) + "]"), q=1, v=1)
				active = []
				for inf in infs:
					if inf > 0.0: active.append(inf)
				active = list(reversed(sorted(active)))
				if debug: print 'Clamping vertex', v, 'to', active[maxInf]
				cmds.skinPercent(skinClust, (mesh + ".vtx[" + str(v) + "]"), pruneWeights=(active[maxInf]*1.001))
		else:
			cmds.warning('Cannot clamp influences due to locked weights on skinCluster')
	

	## TOOLS TAB
	###############
	def makeLocOnSel(self):
		tool = cmds.currentCtx()
		cmds.setToolTo( 'moveSuperContext' )
		pos = cmds.manipMoveContext( 'Move', q=True, p=True )
		startLoc = cmds.spaceLocator (n = ('skinWrangler_jointBboxLocator'))[0]
		cmds.move(pos[0] ,pos[1] ,pos[2] ,startLoc, ws = 1 , a =1)
		cmds.setToolTo(tool)
		return startLoc
	
	def jointOnBboxCenterFn(self):
		if self.jointOnBboxCenterBTN.isChecked() == True:
			self.jointOnBboxCenterBTN.setText('CREATE JOINT FROM ALIGN LOC')
			self.jointLoc = self.makeLocOnSel()
			cmds.setAttr(self.jointLoc + '.displayLocalAxis', 1)
			cmds.select(self.jointLoc)
		else:
			self.jointOnBboxCenterBTN.setText('MAKE JOINT ON BBOX CENTER')
			locXform = cmds.getAttr(self.jointLoc+'.worldMatrix')
			
			#get name
			newName = 'createdJoint'
			inputName, ok = QtGui.QInputDialog.getText(None, 'Creating Node', 'Enter node name:', text=newName)
			if ok: newName = str(inputName)
			cmds.select(cl=1)
			jnt = cmds.joint(name=newName)
			cmds.xform(jnt, m=locXform)
			cmds.delete(self.jointLoc)
		
	
	## REFRESH UI
	###############
	def refreshUI(self):
		refInf = self.currentInf
		self.jointLST.clear()
		self.currentInf = refInf
		
		filter = str(self.filterLINE.text()).lower()
		
		wid = QtGui.QTreeWidgetItem()
		font = wid.font(0)
		#font.setWeight(QtGui.QFont.Normal)
		font.setPointSize(8)
		
		vertSel = True
		s = self.getSelected()
		if s:
			sel, msh, vtx, skin = s
			self.vtxLBL.setText(str(vtx))
		else:
			wid = QtGui.QTreeWidgetItem()
			wid.setText(0, 'MAKE A COMPONENT\n SELECTION ON\n SKINNED MESH')
			wid.setFont(0, font)
			self.jointLST.addTopLevelItem(wid)
			cmds.undoInfo( swf=1)
			self.currentInf = None
			vertSel = False

		skin = None
		if self.currentMesh: self.mshLBL.setText(self.currentMesh)
		if self.currentSkin:
			self.sknLBL.setText(self.currentSkin)
			skin = self.currentSkin
		
		if skin:
			#skin method
			m = cmds.skinCluster(skin, q=1, sm=1)
			if m == 0: self.skinAlgoLBL.setText('Linear')
			if m == 1: self.skinAlgoLBL.setText('DualQuat')
			if m == 2: self.skinAlgoLBL.setText('Blended')
			
			#normalization
			n = cmds.skinCluster(skin, q=1, nw=1)
			if m == 0: self.skinNormalLBL.setText('None')
			if m == 1: self.skinNormalLBL.setText('Interactive')
			if m == 2: self.skinNormalLBL.setText('Post')
			
			#max weights
			self.skinMaxInfLBL.setText(str(cmds.skinCluster(skin, q=1, mi=1)))
			
			if not vertSel: return False
			
			#update jointList
			wDict = self.getAvgVertWeights(sel, skin)
			red = QtGui.QColor(200,75,75,255)
			for inf in wDict.keys():
				if filter in inf.lower() or filter == '':
					wid = QtGui.QTreeWidgetItem()
					infName = inf
					if self.nameSpaceCHK.isChecked(): infName = inf.split(':')[-1]
					wid.setText(0, infName)
					wid.setTextColor(0,red)
					wid.setTextColor(1,red)
					wid.setIcon(0, self.iconLib['joint'])
					wid.setText(1, str("%.4f" % wDict[inf]))
					self.jointLST.addTopLevelItem(wid)
			if self.listAllCHK.isChecked() == True:
				for inf in cmds.skinCluster(self.currentSkin, q=1, inf=1):
					if inf not in wDict.keys():
						if filter in inf.lower() or filter == '':
							wid = QtGui.QTreeWidgetItem()
							wid.setIcon(0, self.iconLib['joint'])
							if self.nameSpaceCHK.isChecked(): inf = inf.split(':')[-1]
							wid.setText(0, inf)
							self.jointLST.addTopLevelItem(wid)
					
			#set previous influence
			item = self.getJointFromList(self.currentInf)
			if item: self.jointLST.setCurrentItem(item)
			else:
				pass
				#print 'Unable to find INF:', self.currentInf

	def profileRefreshUI(self):
		import hotshot
		import hotshot.stats
		
		prof = hotshot.Profile("c:\\myFn.prof")
		prof.runcall(self.refreshUI)
		prof.close()
		#now we load the profile stats
		stats = hotshot.stats.load("c:\\myFn.prof")
		stats.strip_dirs()
		stats.sort_stats('time', 'calls')
		 
		#and finally, we print the profile stats to the disk in a file 'myFn.log'
		saveout = sys.stdout
		fsock = open('c:\\myFn.log', 'w')
		sys.stdout = fsock
		stats.print_stats(20)
		sys.stdout = saveout
		fsock.close()