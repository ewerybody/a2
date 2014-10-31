import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import sys
import os
import sip
import maya.OpenMayaUI as mui
import maya.OpenMaya as om
from CryRigging import rigParts as rp
'''
create a rope chain between two points and a connector Node
example:
from CryRigging.ropeSetup import ropeChainSetup
ropeChainSetup.show()
@author=RihamT
'''
def getMayaWindow():
	
	#'Get the maya main window as a QMainWindow instance'	
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

## Get the absolute path to my ui file
uiFile = (os.path.dirname(str(__file__)) + '/ropeChainSetup.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class Window(base_class, form_class):	
	def __init__(self, parent= getMayaWindow()):
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		##create joints UI
		self.ropeParentGet_call= lambda who="ropeParentText": self.addSelectedObject(who)
		self.startPointGet_call= lambda who="startPointText": self.addSelectedObject(who)
		self.endPointGet_call= lambda who="endPointText": self.addSelectedObject(who)
		
		self.connect(self.ropeParentGet, QtCore.SIGNAL("clicked()") , self.ropeParentGet_call)
		self.connect(self.startPointGet, QtCore.SIGNAL("clicked()") , self.startPointGet_call)
		self.connect(self.endPointGet, QtCore.SIGNAL("clicked()") , self.endPointGet_call)
		self.connect(self.createBTN, QtCore.SIGNAL("clicked()") , self.createChain)
		
		##create Rigging UI
		self.connect(self.startJointGet, QtCore.SIGNAL("clicked()") , self.addSelectedJoint)
		self.connect(self.charPartGet, QtCore.SIGNAL("clicked()") , self.addSelectedcharPart)
		self.connect(self.rigPartsGet , QtCore.SIGNAL("clicked()") , self.addSelectedRigParts)
		self.connect(self.addRiggingBTN, QtCore.SIGNAL("clicked()") , self.createRigging)
		self.connect(self.dynamicsCB, QtCore.SIGNAL("clicked()") , self.addNucleus)
		self.addShapes()

	## ------------create joints-------------------##		
	def addSelectedObject(self , field):
		sel = cmds.ls( sl = True)
		selString = ', '.join(sel)
		if (len(sel) < 1):
			cmds.warning("please select a point or a face or an object")
			cmds.error("please select a point or a face or an object")
		newText = "self.%s.setText(selString)"%field
		eval(newText)

	def getProperName(self):
		ropeName = str(self.ropeNameTxt.text())
		strings = cmds.ls(ropeName+"__Seg*" , et = "joint")
		no = 0
		name = ""
		for s in strings:
			no = s.split(ropeName+"__Seg")[1]
			no = int(no)
	
		if (no+1)<10:
			name = ropeName+"__Seg0"+str(no+1)
		elif (no+1)>=10:
			name = ropeName+"__Seg"+str(no+1)
		return name
		
	def createChain(self):
		ropeParent = str(self.ropeParentText.text())
		ropeName = str(self.ropeNameTxt.text())
		startPoint = str(self.startPointText.text())
		startPointList = startPoint.split(",")
		endPoint = str(self.endPointText.text())
		endPointList = endPoint.split(",")
		startLoc = None
		endLoc = None
		locatorsList =[]
		
		if not startPoint or not endPoint :
			cmds.warning("Please select a start point and end point")
			cmds.error("Please select a start point and end point")
		if 	startPoint == endPoint:
			cmds.warning("start and end point can't be the same")
			cmds.error("start and end point can't be the same")
			
		cmds.undoInfo(openChunk=True)

		try:
			pos = None
			for s in startPointList:
				cmds.select(s)
				tool = cmds.currentCtx()
				cmds.setToolTo( 'moveSuperContext' )
				pos = cmds.manipMoveContext( 'Move', q=True, p=True )
			startLoc = cmds.spaceLocator (n = "startAverage#")[0]
			cmds.move (pos[0] ,pos[1] ,pos[2] ,startLoc, ws = 1 , a =1)
			cmds.setToolTo(tool)

			for e in endPointList:
				cmds.select(e)
				tool = cmds.currentCtx()
				cmds.setToolTo( 'moveSuperContext' )
				pos = cmds.manipMoveContext( 'Move', q=True, p=True )
			endLoc = cmds.spaceLocator (n = "endAverage#")[0]
			cmds.move (pos[0] ,pos[1] ,pos[2] ,endLoc, ws = 1 , a =1)
			cmds.setToolTo(tool)
			
			locatorsList.append(startLoc)
			
			startLocPos = cmds.xform(startLoc ,t = 1, q = 1 , ws = 1, a=1)
			startLocVec = om.MVector(startLocPos[0] , startLocPos[1] , startLocPos[2])
			endLocPos = cmds.xform(endLoc ,t = 1, q = 1 , ws = 1, a=1)
			endLocVec = om.MVector(endLocPos[0] , endLocPos[1] , endLocPos[2])
			
			diff = endLocVec - startLocVec
			len = diff.length()
			dir = (diff).normal()
			splits = self.noOfJoints.value()
			scale =	None
			div = len/(splits-1)

			for m in range( 2, splits):
				b = div*(m-1)
				tempLoc = cmds.spaceLocator(n = "temp#")[0]
				pos = startLocVec + (dir * b)
				cmds.move(pos.x , pos.y ,pos.z , tempLoc,ws = 1 )
				locatorsList.append(tempLoc)
				
			locatorsList.append(endLoc)
			
			jointsList = []
			cmds.select(cl = True)
			for i in locatorsList:
				locPos = cmds.xform(i ,t = 1, q = 1 , ws = 1, a=1)
				joint = cmds.joint(n = self.getProperName(), p = (locPos[0] , locPos[1] ,locPos[2]) , a = True)
				jointsList.append(joint)
				
			cmds.joint(jointsList[0] , e = 1 , oj='xyz' , ch = 1 , secondaryAxisOrient = "zup")
			cmds.setAttr(jointsList[-1] +".jointOrientX" , 0)
			cmds.setAttr(jointsList[-1] +".jointOrientY" , 0)
			cmds.setAttr(jointsList[-1] +".jointOrientZ" , 0)
			
			for l in locatorsList:
				cmds.delete(l)
			cmds.select(cl = True)
			
			if ropeParent:
				cmds.parent(jointsList[0] , ropeParent)
			
		finally:
			cmds.undoInfo(closeChunk=True)
			
	## ------------create Rigging-------------------##
	def addSelectedJoint(self):
		sel = cmds.ls( sl = True)
		selString = ', '.join(sel)
		if (len(sel) < 1):
			cmds.warning("please select a joint to add")
			cmds.error("please select a joint to add")
			return False
		else:
			for jnt in sel:
				if (cmds.nodeType(jnt) == "joint"):
					self.startJointTxt.setText(selString)
				else:
					cmds.warning("please select a joint")
					cmds.error("please select a joint")
					return False
	
	def addSelectedcharPart(self):
			sel = cmds.ls( sl = True)
			if (len(sel) > 1):
				cmds.warning("please select only one character part")
				cmds.error("please select only one character part")
				return False
			else:
				for charPart in sel:
					if (cmds.nodeType(charPart) == "cryCharPart"):
						self.charPartTxt.setText(charPart)
					else:
						cmds.warning("please select a character part")
						cmds.error("please select a character part")
						return False
	
	def addSelectedRigParts(self):
		sel = cmds.ls( sl = True)
		selString = ', '.join(sel)
		if (len(sel) < 1):
			cmds.warning("please select at least one rig part")
			cmds.error("please select at least one rig part")
			return False
		else:
			for rigPart in sel:
				if (cmds.nodeType(rigPart) == "cryRigPart"):
					if cmds.getAttr(rigPart+".partType") == "rope":
						self.rigPartsTxt.setText(selString)
					else:
						cmds.warning("please select a rigPart of part type rope")
						cmds.error("please select a rigPart of part type rope")
						return False
				else:
					cmds.warning("please select a rigPart")
					cmds.error("please select a rigPart")
					return False						
	
	def addShapes(self):
		filePath = os.path.realpath(__file__)
		localIconPath = (filePath.replace(filePath.split('\\')[-1], '') + 'icons\\')
		shapesList = ["fourArrowCircle" , "threeArrowCircle" , "twoArrowCircle","oneArrowCircle" , "cube", "arrow01" , "arrow02" ,"arrow07", "arrow08", "arrow09", "arrow10",
						"implicitSphere03", "circle01" , "circle02", "circle03", "circle04", "circle05","fourFingersHand" ,"fiveFingersHand" , "star", "implicitSphere01", 
						"implicitSphere02","eye", "key", "cross01" , "cross02", "bulb","square"]
			
		##add shapes to fk and ik combo boxes
		for shape in shapesList:
			self.fkShapeCMB.addItem(QtGui.QIcon(localIconPath+"%s_on.bmp"%shape),shape)
			self.ikShapeCMB.addItem(QtGui.QIcon(localIconPath+"%s_on.bmp"%shape),shape)

	def addNucleus(self):
		self.NucleusCMB.clear()
		nucleusItemList = ["New"]
		nucleusList = cmds.ls(type = "nucleus")
		for nucleus in nucleusList:
			nucleusItemList.append(nucleus)
		self.NucleusCMB.addItems(nucleusItemList)
	
	def createRigging(self):
		cmds.undoInfo(openChunk=True)
		try:
			startJnt = str(self.startJointTxt.text())
			startJntList = startJnt.split(",")
			controlsNo = self.noOfControls.value()
			prefix = str(self.prefixTxt.text())
			dynamics = int(self.dynamicsCB.isChecked())
			fkShape =  str(self.fkShapeCMB.currentText())
			ikShape =  str(self.ikShapeCMB.currentText())
			shared = int(self.sharedCB.isChecked())
			RotOrder = str(self.rotationOrderCMB.currentText())
			nucleus = str(self.NucleusCMB.currentText())
			nucleusName = nucleus
			if nucleus == "New":
				nucleusName = None
				
			prefixName = None
			rigPartsList = []
			##start Rigging
			if startJntList:
				if len(startJntList) > 1 :
					for jntChain in startJntList:
						if prefix:
							prefixName = prefix+("_%s_chain"%jntChain)
						else:
							prefixName = "%s_chain"%jntChain
						rigPart = prefixName  + "_rigPart"
						ropePart = rp.ropeSegment(parentJoint = jntChain ,rigPart = rigPart, numberOfControls = controlsNo, shared = shared ,dynamic = dynamics ,nucleusSolver = nucleusName, prefix = prefixName,ikShape = ikShape , fkShape = fkShape ,rotationOrder = RotOrder)
						rigPartsList.append(ropePart)
				elif len(startJntList) == 1 :
					if prefix:
						prefixName = prefix
					else:
						prefixName = "%s_chain"%startJntList[0]
					rigPart = prefixName  + "_rigPart"
					ropePart = rp.ropeSegment(parentJoint = startJntList[0] ,rigPart = rigPart, numberOfControls = controlsNo, shared = shared ,dynamic = dynamics ,nucleusSolver = nucleusName, prefix = prefixName,ikShape = ikShape , fkShape = fkShape ,rotationOrder = RotOrder)
					rigPartsList.append(ropePart)
			else:
				cmds.warning("please selct a parent joint to start rigging")
				cmds.error("please selct a parent joint to start rigging")
				return False
			
			##add rig parts created to existing rig parts field
			self.rigPartsTxt.setText(rigPartsList)
		finally:
			cmds.undoInfo(closeChunk=True)
	def connectRopes(self):
		prefix = str(self.prefixTxt.text())
		shared = int(self.sharedCB.isChecked())
		charpart = str(self.charPartTxt.text())
		rigParts = str(self.rigPartsTxt.text())
		rigPartsList = rigParts.split(",")

		
		
def show():
	global UiWindow
	try:
		UiWindow.close()
	except:pass
	UiWindow = Window()
	UiWindow.show()
	return UiWindow