
#===============================================================================
#
# RETARGET_TOOL.PY 
#
# Author: Marcus Krautwurst
# 
#===============================================================================

import maya.standalone
import math
import os 
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as mui
import maya.OpenMaya as OpenMaya 
import maya.OpenMayaMPx as OpenMayaMPx 
import sip
import pymel.core.datatypes as dt
from PyQt4 import QtGui, QtCore, uic
from pymel.all import *
import xml.dom.minidom as minidom
from time import time
from pymel.core.general import getAttr

import CryAnimation




def getScriptPath():
	newString = (os.path.abspath(__file__))
	return os.path.dirname(newString)

sCryRetargetRoothPath = getScriptPath()
intVersion = "0.9"



#===============================================================================
# ## Basic Vars
#===============================================================================

aSrcNodes = []
aSrcNodeNames = []
aTgtNodes = []
aTgtNodeOffsets = []
aOffsetPos = []
aOffsetRot = []
aTmpConstraints = []
aImportFiles= []
aBatchImportFiles = []
vDialogChecked = False

#===============================================================================
# Load UI Files and instance classes
#===============================================================================


## Load the ui file, and create my class
uiFile=(sCryRetargetRoothPath + "\cryRetarget.ui")
form_class, base_class = uic.loadUiType(uiFile)


## Load the ui file, and create my class
uiMappingError=(sCryRetargetRoothPath + "\dialog_mapping_error.ui")
form_class_ErrorDialog, base_class_ErrorDialog = uic.loadUiType(uiMappingError)


## Get maya window instance and use it as a parent for the tool window
def getMayaWindow():
	'Get the maya main window as a QMainWindow instance'
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)



class cryMappingError(form_class_ErrorDialog, base_class_ErrorDialog):
	def __init__(self, parent=getMayaWindow()):
		## A custom window with a demo set of ui widgets
		super(base_class_ErrorDialog, self).__init__(parent)
		## uic adds a function to our class called setupUi, calling this creates all the widgets from the .ui file
		self.setupUi(self)
		self.setObjectName("wMappingError")		
		
		self.btnDontLoad.clicked.connect(self.fnDontLoad)
		self.btnLoad.clicked.connect(self.fnLoad)
		
	def fnDontLoad(self):	
		vDialogChecked = True
		
	def fnLoad(self):
		vDialogChecked = True  

class SourceNodes(list):

	rootPath = ""
	absPath = ""
	
	   
class cryRetargetClass(base_class, form_class):
	def __init__(self, parent=getMayaWindow()):		
		super(base_class, self).__init__(parent)
		
		## uic adds a function to our class called setupUi, calling this creates all the widgets from the .ui file
		self.setupUi(self)
		self.setObjectName("wCryRetarget")
		self.setWindowTitle("cryRetarget " + intVersion)

#===============================================================================
# Member variables
#===============================================================================
		self.inBatch = False
		
		
#===============================================================================
# UI FUNCTIONS
#===============================================================================

		
		self.btnSrcAdd.clicked.connect(self.fnAddSrcNode)
		self.btnSrcDel.clicked.connect(self.fnDelSrcNode)
		
		self.btnTgtAdd.clicked.connect(self.fnAddTargetNode)
		self.btnClearAnim.clicked.connect(self.fnClearTargetAnim)		
		self.btnUpdateOffsetAll.clicked.connect(self.fnUpdateOffsetAll)
		
		self.btnNew.clicked.connect(self.fnNewMapping)
		self.btnSave.clicked.connect(self.fnSaveMapping)
		self.btnLoad.clicked.connect(self.fnLoadMapping)		
		self.btnTest.clicked.connect(self.fnRunRetarget)
		
		self.chk_Pos.stateChanged.connect(self.fnPosChangeState)
		self.chk_Rot.stateChanged.connect(self.fnRotChangeState)	   
		
		
		self.lsSrc.itemSelectionChanged.connect(self.OnSrcListClick)
		self.lsTgt.itemSelectionChanged.connect(self.OnTgtListClick)
		
		self.lsSrc.clicked.connect(self.OnSrcListClick)
		self.lsTgt.clicked.connect(self.OnTgtListClick)
		
		self.btnRangeStart.clicked.connect(self.fnResetRangeStart)
		self.btnRangeEnd.clicked.connect(self.fnResetRangeEnd)		
		
		self.exportPathChange.clicked.connect(self.fnSetExportPath)
		self.btnAddFolder.clicked.connect(self.fnAddFolder)

		self.srcRigAutoFill.clicked.connect(self.fnAutoFillSourceRigPath)
		
		self.btnBatch.clicked.connect(self.fnStartBatch)
   
		self.btnCreateConstraints.clicked.connect(self.fnCreateConstraints)
		self.btnDeleteConstraints.clicked.connect(self.fnBreakConstraints)
		
		## Set some inital UI states
		self.progressBar.setHidden(True)

		self.progressBarBatch.setHidden(True)
		

		self.chk_Redraw.setChecked(0)
		
		self.animRangeStart.setValue(int(playbackOptions(query=1,animationStartTime=1)))
		self.animRangeEnd.setValue(int(playbackOptions(query=1,animationEndTime=1)))
		self.fnAutoFillSourceRigPath()
#===============================================================================
# UI EVENTS
#===============================================================================

	def fnStartBatch(self):		
		if len(aSrcNodes) > 0 and len(aTgtNodes) > 0:
			startBatchTime = self.fnStartTimer()			
			self.progressBarBatch.setHidden(False)
			
			self.inBatch = True
			vSrcRig = str(self.srcRigPath.text())		
			vExportPath = str(self.exportPath.text())
			vExportPath.replace("FBX","MA")
			
			## Count Files
			intFileCount = 0
			intFilesProcessed = 0
			for path in aBatchImportFiles: 
				intFileCount += len(path[1])

			for path in aBatchImportFiles:  
				## Define root path
				rootPath = path[0]
				
				for file in path[1]:
					self.progressBarBatch.setValue(100.0/intFileCount*intFilesProcessed)
					importFile = rootPath+file
					saveFile = vExportPath+file
					
					## Parse string to create new folder
					Idx = saveFile.rfind("\\")+1
					newFolder = saveFile[0:Idx]
					sysFile(newFolder,makeDir=True)					
					
					## Open maya target rig
					cmds.file(vSrcRig, force=True, open=True)
					###################
					if self.chckDefConstraints.isChecked() == True:
						self.fnCreateConstraints()
					else:
						self.fnClearTargetAnim() # anim on target is deleted while creating parent constraints, but since we skip that, we need to delete in manually.
					## Import FBX				
					# cmds.file(importFile, force=True,type="FBX", i=True)
					# loading FBX with FBXImport command instead
					importFile2 = str.replace(importFile, "\\", "/")
					evalString = 'FBXImport -f "' + importFile2 + '";'
					mel.eval(evalString)
					
					self.fnRunRetarget()
					###################
					#if self.chckDefConstraints.isChecked() == True:					
					#	self.fnBreakConstraints()

					aNewCurves = CryAnimation.getCurvesFromNodes(aTgtNodes, excludeAttributes=['visibility'],showProgress=True,debug=False,cutNamespace=False)
					CryAnimation.saveCurvesIntoFile(saveFile.replace(".fbx",".aff"), aNewCurves)
					## Rename and save the file
					#cmds.file(rename=saveFile)
					#cmds.file(force=True,type="mayaAscii", save=True)
					intFilesProcessed += 1
			self.inBatch = True
			cmds.file(vSrcRig, force=True, open=True)
			self.progressBarBatch.setHidden(True)
			self.fnStopTimer(startBatchTime)
		else:
			warning("cryRetarget: Please create or load a mapping")
	 
	def OnSrcListClick(self):
		## Turn undo off
		undoInfo(state=False, stateWithoutFlush=True)
		srcIdx = self.lsSrc.currentRow()				
		self.lsTgt.setCurrentRow(srcIdx)
		srcWidg = self.lsTgt.currentItem()
		self.lsTgt.scrollToItem(srcWidg)
		try:
			select (aSrcNodes[srcIdx])						
		except: 
			pass
		self.fnUpdateNodeSettings(srcIdx)
		
		## Turn undo on
		undoInfo(state=True)
		
		
	def OnTgtListClick(self):
		## Turn undo off
		undoInfo(state=False, stateWithoutFlush=True)
		
		tgtIdx = self.lsTgt.currentRow()	
		self.lsSrc.setCurrentRow(tgtIdx)
		try:			
			select (aTgtNodes[tgtIdx])
		except: 
			pass			 
		self.fnUpdateNodeSettings(tgtIdx)
		 
		## Turn undo on
		undoInfo(state=True)
	
	def fnAutoFillSourceRigPath(self):
		self.srcRigPath.setText(str(sceneName()))
			
	def fnResetRangeStart(self):
		self.animRangeStart.setValue(int(playbackOptions(query=1,animationStartTime=1)))
		
	def fnResetRangeEnd(self):
		self.animRangeEnd.setValue(int(playbackOptions(query=1,animationEndTime=1)))
		
	def fnNewMapping(self):
		if len(aSrcNodes) > 0: 
			self.fnClearSrcList()
		if len(aTgtNodes) > 0:
			self.fnClearTgtList()
	
	def fnSetExportPath(self):
		filepath = fileDialog2(startingDirectory =sCryRetargetRoothPath, fileFilter="*", dialogStyle=0, caption="Set Export folder", fileMode=3)
		if filepath != None:
			self.exportPath.setText(str(filepath[0]))
			
			
	def fnGetFilesFromFolder(self,root,ext):
		fileList = []		
		for root, subFolders, files in os.walk(root):
			for file in files:
				f = os.path.join(root,file)
				if (os.path.splitext(f)[1]) == ext:
					fileList.append(f)		
		if len(fileList)>0:
			return fileList
		else:
			return None
			
	def fnAddFolder(self):
		filepath = fileDialog2(startingDirectory ="J:\\Work\\Gface\\", fileFilter="*", dialogStyle=0, caption="Add source folder", fileMode=3)[0]
		if filepath != None:
			filepath = os.path.normpath(filepath)
			aImportFiles = self.fnGetFilesFromFolder(filepath,".fbx")
			if aImportFiles != None and len(aImportFiles)>0:				
				topitem = QtGui.QTreeWidgetItem(filepath)
				
				## Format TopItem							   
				font = topitem.font(0)
				font.setBold(True)
				font.setPixelSize(15)
				topitem.setFont(0,font)
				topitem.setText(0,filepath)
				self.lsExport.insertTopLevelItem(0,topitem)
				topitem.setBackgroundColor(0,QtGui.QColor(217, 151, 151))
				topitem.setForeground(0,QtGui.QColor(0, 0, 0))
				
				tmpFiles = []
				for f in aImportFiles:
					item = QtGui.QTreeWidgetItem(f)
					relPath = f.replace(filepath,"")
					item.setText(0,relPath)
					topitem.addChild(item)
					tmpFiles.append(str(relPath))					
				self.SourceFileNodeCount.setText("Source Nodes: (" + str(len(aImportFiles)) + ")" )
				aBatchImportFiles.append([str(filepath),tmpFiles])
			self.lsExport.expandItem(topitem)



#===============================================================================
# UI Operations Source Nodes
#===============================================================================

	def fnAddSrcNode(self):
		## Add selected nodes to the provided list			
		mySelection = ls(selection=True)
		for item in mySelection:
			name = item.name()			
			if name not in aSrcNodes:
				aSrcNodes.append(name)
			else: 
				warning("cryRetarget: " + name +" is already added to the source list")
		self.fnUpdateSrcList()
		self.lsSrc.setCurrentRow(len(aSrcNodes)-1)
		
		
		
	def fnDelSrcNode(self):
		selRef = self.lsSrc.currentRow()
		aSrcNodes.pop(selRef)
		aTgtNodes.pop(selRef)
		aTgtNodeOffsets.pop(selRef)
		aOffsetPos.pop(selRef)
		aOffsetRot.pop(selRef)
		self.fnUpdateSrcList()
		self.fnUpdateTgtList()
		if selRef==len(aSrcNodes):
			self.lsSrc.setCurrentRow(selRef-1)
			self.lsTgt.setCurrentRow(selRef-1)
		else:			
			self.lsSrc.setCurrentRow(selRef)
			self.lsTgt.setCurrentRow(selRef)
			
	def fnUpdateSrcList(self):
		self.lsSrc.clear()
		if len(aSrcNodes) > 0:
			for item in aSrcNodes:			
				self.lsSrc.addItem(item)
		self.lblSrcNodes.setText("Source Nodes: (" + str(len(aSrcNodes)) + ")" )			
   
			
	def fnClearSrcList(self):		
		del aSrcNodes[:]
		del aTgtNodes[:]
		del aTgtNodeOffsets[:]
		del aOffsetPos[:]
		del aOffsetRot[:]
		self.fnUpdateSrcList()
		self.fnUpdateTgtList()
		
		
		
#===============================================================================
# UI Operations Target Nodes	 
#===============================================================================
 
	def fnAddTargetNode(self):
		## Add selected nodes to the provided list			 
		mySelection = ls(selection=True)
		for item in mySelection:
			name = item.name()			
			if name not in aTgtNodes:
				## Add Target to target array			   
				aTgtNodes.append(name) 
							   
				## Get the the new target index to get the correct node in source for offset calculation
				srcObj = ls(aSrcNodes[len(aSrcNodes)-1])[0]
				tgtObj = ls(aTgtNodes[len(aTgtNodes)-1])[0]
				
				srcWorldTM = srcObj.getMatrix(worldSpace=True)
				tgtWorldTM = tgtObj.getMatrix(worldSpace=True)
				
				self.fnDeleteAllKeyFrames(tgtObj) 
				
				## Recalculate Offset in Local Target Space and append it to the offset array
				locTM =  tgtWorldTM * srcWorldTM.inverse()				
				aTgtNodeOffsets.append(locTM)
				
				## Set Position and Rotation Offset to 2 by default
				aOffsetPos.append(2)
				aOffsetRot.append(2)									  
				
			else: 
				warning("cryRetarget: " + name +" is already added to the target list")						
		self.fnUpdateTgtList()
		self.lsTgt.setCurrentRow(len(aTgtNodes)-1)
		
	
	def fnUpdateTgtList(self):		
		self.lsTgt.clear()
		if len(aTgtNodes) > 0:
			for item in aTgtNodes:
				self.lsTgt.addItem(item)
				
			self.fnUpdateNodeSettings(len(aTgtNodes)-1)
		
		## Set Headline for the node count
		self.lblTgtNodes.setText("Target Nodes: (" + str(len(aTgtNodes)) + ")" )		


		
#===============================================================================
# UI Operations  misc	 
#===============================================================================

	
	def fnStartTimer(self):
		startTime = time()
		return startTime
	
	
	def fnStopTimer(self,t):
		result = time()-t
		warning("cryRetarget: Completed in " + str(round(result,2)) + " seconds")
	
			
	def fnUpdateOffsetAll(self):		
		## store the pre-selection
		preSelIdx = self.lsTgt.currentRow()		
		intUpdated = 0
		for item in range(0,len(aSrcNodes)):			
			## Get objects from row
			srcObj = ls(aSrcNodes[item])[0]
			tgtObj = ls(aTgtNodes[item])[0]
			
			## Receive updated matrices
			if srcObj != None and tgtObj != None:
				srcWorldTM = srcObj.getMatrix(worldSpace=True)
				tgtWorldTM = tgtObj.getMatrix(worldSpace=True)			
				
				## Recalculate Offset in Local Target Space			  
				locTM =  tgtWorldTM * srcWorldTM.inverse()
				
				oldOffset = aTgtNodeOffsets[item]
				if locTM != oldOffset:
					intUpdated += 1
					aTgtNodeOffsets[item] = locTM					
				
			else:
				warning("cryRetarget: Some objects in the list are no longer available")
		
		if intUpdated == 0:
			warning("cryRetarget: No offset update required")
		else:
			warning("cryRetarget: " + str(intUpdated) + " offsets updated")
		
		## Update and restore the pre-selection
		self.fnUpdateNodeSettings(preSelIdx)
		self.lsTgt.setCurrentRow(preSelIdx)		
		
		
	def fnUpdateNodeSettings(self,node):		
		## Update the checkboxes for position and rotation		   
		## Read the values from the arrays
		if aOffsetPos[node] == 2:
			nodeStatusPos = True
		else:
			nodeStatusPos = False
			
		if aOffsetRot[node] == 2:
			nodeStatusRot = True
		else:
			nodeStatusRot = False			
		
		## Set all states
		self.chk_Pos.setChecked(nodeStatusPos)
		self.chk_Rot.setChecked(nodeStatusRot)
		self.linePosOffset.setEnabled(aOffsetPos[node])
		self.lineRotOffset.setEnabled(aOffsetRot[node])
		
		## Set text for position matrix display			
		TM = aTgtNodeOffsets[node]
		
		## If status is 2 then enable the text if not then empty it
		if nodeStatusPos == True:
			self.linePosOffset.setText(str(TM[3]))
		else:
			self.linePosOffset.setText("-disabled-")
		if nodeStatusRot == True:
			self.lineRotOffset.setText(str(TM[0]) + str(TM[1]) + str(TM[2]))
		else:
			self.lineRotOffset.setText("-disabled-")
		
		## Set the cursor to the start of the line
		self.linePosOffset.home(False)
		self.lineRotOffset.home(False)
		

		
	def fnDialogMappingError(self,node):		
		cryMappingErrorWindow = cryMappingError()
		cryMappingErrorWindow.show()
		cryMappingErrorWindow.nodeName.setText(node)
		
	def fnClearTargetAnim(self):		
		if len(aTgtNodes) > 0:			
			for i in range(0,len(aTgtNodes)):
				self.fnDeleteAllKeyFrames(aTgtNodes[i])

	def fnPosChangeState(self,state):		
		tgtItem = self.lsTgt.currentRow()
		if tgtItem != None:
			aOffsetPos[tgtItem] = state
		self.fnUpdateNodeSettings(tgtItem)
	
	def fnRotChangeState(self,state):		
		tgtItem = self.lsTgt.currentRow()
		if tgtItem != None:
			aOffsetRot[tgtItem] = state		
		self.fnUpdateNodeSettings(tgtItem)
		
		
#===============================================================================
# Logic
#===============================================================================


	def fnSaveMapping(self):
		filepath = fileDialog2(startingDirectory =sCryRetargetRoothPath, fileFilter="CryRetarget Mapping File (*.retarget)", dialogStyle=0, caption="Save Mapping File", fileMode=0)

		
		if filepath != None:				
			doc = minidom.Document()
			wml = doc.createElement("retarget")
			wml.setAttribute("version", str(2))
			doc.appendChild(wml)		
			  
			## Create the <source> element
			srcNodes = doc.createElement("sources")
			wml.appendChild(srcNodes)
			for i in range(0,len(aSrcNodes)):
				srcNode = doc.createElement("source")
				srcNode.setAttribute("name", aSrcNodes[i])
				srcNodes.appendChild(srcNode)
							 
			 ## Save XML
			tgtNodes = doc.createElement("targets")
			wml.appendChild(tgtNodes)
			for i in range(0, len(aTgtNodes)):			  
			## Create the <target> element				
				tgtNode = doc.createElement("target")
				tgtNode.setAttribute("name", aTgtNodes[i])
				tgtNodes.appendChild(tgtNode)
				
			## Create the <offset> element			
				offset = doc.createElement("offset")			
				offset.setAttribute("TM", str(aTgtNodeOffsets[i]))
				tgtNode.appendChild(offset)
				
			## Create the <posOffset> element (state of the position checkbox)   
				posOffset = doc.createElement("posOffset")			
				posOffset.setAttribute("state", str(aOffsetPos[i]))
				tgtNode.appendChild(posOffset)
				
			## Create the <rotOffset> element (state of the rotation checkbox)
				rotOffset = doc.createElement("rotOffset")			
				rotOffset.setAttribute("state", str(aOffsetRot[i]))
				tgtNode.appendChild(rotOffset)
							
			file = open(filepath[0], 'w')
			file.write(doc.toprettyxml())
			warning("cryRetarget: Saved " + filepath[0])
		
		
	def fnStringToTM(self,stringTM): 
		tmp1 = (stringTM.split("[["))[1]
		tmp2 = (tmp1.split("]]"))[0]
		tmp3 = tmp2.split("], [")
		convertTM = []
		for Idx in range(0,len(tmp3)):
			tmp4 = tmp3[Idx].split(", ")
			for each in range(0,4):
				tmp4[each] = float(tmp4[each])
			convertTM.append(tmp4)
						
		newTM = dt.Matrix(convertTM)
		return newTM
	
	def checkNodeByName(self,strNode):
		if objExists(strNode) == True:	  
			return True
		else:
			return False
				
		
	def fnLoadMapping(self):
		filepath = fileDialog2(startingDirectory =sCryRetargetRoothPath, fileFilter="CryRetarget Mapping File (*.retarget)",dialogStyle=0, caption="Load Mapping File", fileMode=1)
		
		if filepath != None:
			## Empty old lists
			self.fnClearSrcList()						
			
			## Parse XML 
			doc = minidom.parse(filepath[0])
			
			## Convert Doc to XML format and load into memory
			doc.toxml()
			
			## Get root node
			root = doc.childNodes[0]
			
			## Update Progress Bar
			self.progressBar.setHidden(False)
			self.progressBar.setValue(0)			
			
			if root.hasAttribute("version") and root.getAttribute("version") == "2":
				self.fnLoadMappingV2(root)
			else:				
				self.fnLoadMappingV1(root)
				  
				
			## Update Progress Bar
			self.progressBar.setValue(100)
			self.progressBar.setHidden(True)			
			warning("cryRetarget: Loaded " + filepath[0])
 
	def fnLoadMappingV1(self, root):

		## Read the nodes from the document			
		for i in range(0,len(root.childNodes)):
						   
			self.progressBar.setValue(100.0/len(root.childNodes)*(i+1))
			srcNode = root.childNodes[i].attributes.item(0).nodeValue
			tgtNode = root.childNodes[i].childNodes[0].attributes.item(0).nodeValue			
			strOffsetTM = root.childNodes[i].childNodes[1].attributes.item(0).nodeValue
			offsetTM = self.fnStringToTM(strOffsetTM)
			
			bPosOffset = root.childNodes[i].childNodes[2].attributes.item(0).nodeValue
			bRotOffset = root.childNodes[i].childNodes[3].attributes.item(0).nodeValue				
			
			## Check if the nodes are in the scene and give the user options what to do if they do not exist
			
			aSrcNodes.append(srcNode)				
			aTgtNodes.append(tgtNode)
			
			aTgtNodeOffsets.append(offsetTM)
			aOffsetPos.append(int(bPosOffset))
			aOffsetRot.append(int(bRotOffset))
			
			self.fnUpdateSrcList()
			self.fnUpdateTgtList()
			self.lsTgt.setCurrentRow(len(aTgtNodes)-1)
	
	def fnLoadMappingV2(self, root):
		sourceNds = root.getElementsByTagName("sources")[0].getElementsByTagName("source")
		for srcNd in sourceNds:
			aSrcNodes.append(srcNd.attributes.item(0).nodeValue)  
		targetNds = root.getElementsByTagName("targets")[0].getElementsByTagName("target")
		for tgtNd in targetNds:
			aTgtNodes.append(tgtNd.attributes.item(0).nodeValue)
			strOffsetTM = tgtNd.getElementsByTagName("offset")[0].attributes.item(0).nodeValue
			offsetTM = self.fnStringToTM(strOffsetTM)
			
			bPosOffset = tgtNd.getElementsByTagName("posOffset")[0].attributes.item(0).nodeValue
			bRotOffset = tgtNd.getElementsByTagName("rotOffset")[0].attributes.item(0).nodeValue
			aTgtNodeOffsets.append(offsetTM)
			aOffsetPos.append(int(bPosOffset))
			aOffsetRot.append(int(bRotOffset))  
		
		self.fnUpdateSrcList()
		self.fnUpdateTgtList()
		self.lsTgt.setCurrentRow(len(aTgtNodes)-1)								  

	def fnRunRetarget(self):
		## New undo chunk		
		undoInfo(openChunk=True)
		
		## Redraw check
		if self.chk_Redraw.isChecked() == 0:
			refresh(suspend=True)
		if len(aSrcNodes) > 0  and len(aTgtNodes) >0:
			self.fnAlignNodes()
		else:
			warning("cryRetarget: No objects to retarget")
		
		## Close undo chunk
		undoInfo(closeChunk=True)
		
		## Turn redraw on
		refresh(suspend=False)
		


	def fnDeleteAllKeyFrames(self,pNode):
		"""
		This function inputs a node and delete all keyframes
		on translate, rotate, scale on it
		"""
		attributes=["_translateX" , "_translateY" , "_translateZ" , "_rotateX" , "_rotateY" , "_rotateZ" , "_scaleX" , "_scaleY" , "_scaleZ"]
		for attribute in attributes:
			if objExists(pNode+attribute) == True:
				delete(pNode+attribute)
				
	
	
	
	def fnGetAnimCurveByNode(sNode,sAttribute):
		tmpString = connectionInfo ( (sNode+"."+sAttribute), sourceFromDestination=True)
		tmpString = tmpString.split(".")[0]
		return tmpString
	
	
	def fnCreateConstraints(self):
		global aTmpConstraints		
		self.fnBreakConstraints()
		for node in range(0,len(aSrcNodes)):			
			tgtParent = None
			## Set vars for the nodes
			srcObj = ls(aSrcNodes[node])[0]
			tgtObj = ls(aTgtNodes[node])[0]
			
			self.fnDeleteAllKeyFrames(aTgtNodes[node])
			setKeyframe(tgtObj)			
			select(srcObj,tgtObj)	 
			
			skipPos = ["x", "y", "z"]
			skipRot = ["x", "y", "z"]
			
			if aOffsetPos[node]==2:
				skipPos = []
			if aOffsetRot[node]==2:
				skipRot = []
			
			if not cmds.objExists(tgtObj):
				print(srcObj + "   " + tgtObj)
			
			
			pConstraint = parentConstraint(srcObj,tgtObj,mo=1,st=skipPos, sr=skipRot).getName()				
			setAttr(tgtObj+".blendParent1",1)
			aTmpConstraints.append(str(pConstraint))	 

	def fnBreakConstraints(self):
		global aTmpConstraints
		## Delete all constraints		  
		if len(aTmpConstraints) > 0:
			for obj in range(0,len(aTmpConstraints)):
				if(objExists(obj)):
					select(obj)
					delete(obj)
			aTmpConstraints = []

 
	def fnAlignNodes(self):

		
		## Start the timer
		#startTime = self.fnStartTimer()				
		
		## Get animation range and align src to tgt		
   
		self.inBatch = True
		 # we need determine difference between manual run and batch, manual run should take values from UI, batch should read it from special FBX node, or calculate 
		if(self.inBatch):
			# for now we don't have node, so we calculate every time
			animLength = self.fnGetAnimLenght()
			starttime = animLength[0]
			endtime = animLength[1]
			cmds.playbackOptions( animationStartTime=starttime, animationEndTime=endtime, min = starttime, max = endtime )
		else:
			starttime = self.animRangeStart.value()
			endtime = self.animRangeEnd.value()+1	 
		
		
		#	  for node in range(0,len(aSrcNodes)):			
		#		  tgtParent = None
		#		  srcObj = ls(aSrcNodes[node])[0]			
		#		  tgtObj = ls(aTgtNodes[node])[0]
		## If target has keys delete them
		
		
		## Bake the animation	
		bakeSimulation( aTgtNodes, t=(starttime,endtime), sb=1, at=["rx","ry","rz","tx","ty","tz"])

		 
		## Update Progress Bar		
		self.progressBar.setValue(100)
		self.progressBar.setHidden(True)
		## Stop the timer	  
	   # start = self.fnStopTimer(startTime)
	   
	def fnGetAnimLenght(self):	
		aAttribsToGet = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']
		maxKey = 0.0
		minKey = 9999.0
		for node in range(0,len(aSrcNodes)):
			#print "------------------------"
			srcObj = ls(aSrcNodes[node])[0]
			print srcObj
			node_max_arr = []
			node_min_arr = []
			for attrib in aAttribsToGet:
				#print attrib
				res = cmds.keyframe( srcObj+"", at=attrib, q=True, tc=True )
				if not res == None:
					if res[-1] > maxKey:
						maxKey = res[-1]
					if res[0] < minKey:
						minKey = res[0]
		return [minKey,maxKey]

def showWindow():
	global cryRetargetWindow
	cryRetargetWindow = cryRetargetClass()
	cryRetargetWindow.show()

if __name__ == "__main__":
	global cryRetargetWindow
	cryRetargetWindow = cryRetargetClass()
	cryRetargetWindow.show()