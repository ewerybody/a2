'''
Created on 7 Apr 2011

@author: owen
'''

from PyQt4 import QtGui, QtCore, uic
from pymel.core import *

CryMaya_AlignTool_Ui = 'J:/data/Games/Crysis3/dev/Tools/CryMayaTools/Modeling/python/CryMaya_AlignTool_UI.ui'
		  
class CryMaya_AlignToolDialog(QtGui.QDialog):
	def __init__ (self, parent = None):
		
		super(CryMaya_AlignToolDialog, self).__init__(parent)
		uic.loadUi(CryMaya_AlignTool_Ui, self)
		#Main
		QtCore.QObject.connect(self.btn_apply, QtCore.SIGNAL("clicked()"), self.apply_onClick)
		QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL("clicked()"), self.ok_onClick)
		QtCore.QObject.connect(self.btn_cancel, QtCore.SIGNAL("clicked()"), self.cancel_onClick)
		QtCore.QObject.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)
		QtCore.QObject.connect(self, QtCore.SIGNAL('triggered()'), self.showEvent)
		
		#Position
		QtCore.QObject.connect(self.chk_pos_xPos, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_pos_yPos, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_pos_zPos, QtCore.SIGNAL("clicked()"), self.updatePreview)
			#Source
		QtCore.QObject.connect(self.rb_pos_src_center, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_src_max, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_src_min, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_src_pivot, QtCore.SIGNAL("clicked()"), self.updatePreview)
			#Target
		QtCore.QObject.connect(self.rb_pos_tar_center, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_tar_max, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_tar_min, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.rb_pos_tar_pivot, QtCore.SIGNAL("clicked()"), self.updatePreview)
		
		#Oreintation
		QtCore.QObject.connect(self.chk_orient_xAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_orient_yAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_orient_zAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		
		#Scale
		QtCore.QObject.connect(self.chk_scale_xAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_scale_yAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		QtCore.QObject.connect(self.chk_scale_zAxis, QtCore.SIGNAL("clicked()"), self.updatePreview)
		
		#Define Class vars
		self.sourceNodes = []
		self.sourceNodesAttr = []
		self.targetNode = []
		self.targetBB = []
		
		
	def cancel_onClick(self):
		self.done(0)
		
	def ok_onClick(self):
		self.done(1)
	
	def apply_onClick(self):
		## Don't close undo chunk on apply!
		# Re-Generate Source info arrays
		self.sourceNodesAttr = []
		
		for node in self.sourceNodes :
			self.sourceNodesAttr.append(CryMaya_AlignToolSourceNode(node))

			
		## Reset UI
			self.chk_pos_xPos.setChecked(False)
			self.chk_pos_yPos.setChecked(False)
			self.chk_pos_zPos.setChecked(False)
			self.chk_scale_xAxis.setChecked(False)
			self.chk_scale_yAxis.setChecked(False)
			self.chk_scale_zAxis.setChecked(False)
			self.chk_orient_xAxis.setChecked(False)
			self.chk_orient_yAxis.setChecked(False)
			self.chk_orient_zAxis.setChecked(False)
			
		self.updatePreview()
		
		
	def updatePreview(self):
		
		targetAlignTo = self.targetNode.getTranslation(space='world')
			
		#Generate Target Pos Coords with offset
		if self.rb_pos_tar_center.isChecked():
			if self.chk_pos_xPos.isChecked(): targetAlignTo[0] = objectCenter(self.targetNode)[0]
			if self.chk_pos_yPos.isChecked(): targetAlignTo[1] = objectCenter(self.targetNode)[1]
			if self.chk_pos_zPos.isChecked(): targetAlignTo[2] = objectCenter(self.targetNode)[2]
		
		if self.rb_pos_tar_min.isChecked():
			if self.chk_pos_xPos.isChecked(): targetAlignTo[0] = self.targetBB[0]
			if self.chk_pos_yPos.isChecked(): targetAlignTo[1] = self.targetBB[1]
			if self.chk_pos_zPos.isChecked(): targetAlignTo[2] = self.targetBB[2]
			
		if self.rb_pos_tar_max.isChecked():
			if self.chk_pos_xPos.isChecked(): targetAlignTo[0] = self.targetBB[3]
			if self.chk_pos_yPos.isChecked(): targetAlignTo[1] = self.targetBB[4]
			if self.chk_pos_zPos.isChecked(): targetAlignTo[2] = self.targetBB[5]

		if self.rb_pos_tar_pivot.isChecked():
			if self.chk_pos_xPos.isChecked(): targetAlignTo[0] = self.targetNode.getRotatePivot(space='world')[0]
			if self.chk_pos_yPos.isChecked(): targetAlignTo[1] = self.targetNode.getRotatePivot(space='world')[1]
			if self.chk_pos_zPos.isChecked(): targetAlignTo[2] = self.targetNode.getRotatePivot(space='world')[2]
			
			

		## Generate source pos coords offset
		for i in range(len(self.sourceNodes)):
			## SCALING	
			
			targetScale = self.getAbsoluteScale(self.targetNode)
			
			if self.chk_scale_xAxis.isChecked():
				scale(self.sourceNodes[i],targetScale[0], scaleX=True, absolute=True)
			else:
				scale(self.sourceNodes[i],self.sourceNodesAttr[i].scale[0], scaleX=True, absolute=True)
			   
			if self.chk_scale_yAxis.isChecked():
				scale(self.sourceNodes[i],targetScale[1], scaleY=True, absolute=True)
			else:
				scale(self.sourceNodes[i],self.sourceNodesAttr[i].scale[1], scaleY=True, absolute=True)
						   
			if self.chk_scale_zAxis.isChecked():
				scale(self.sourceNodes[i],targetScale[2], scaleZ=True, absolute=True)
			else:
				scale(self.sourceNodes[i],self.sourceNodesAttr[i].scale[2], scaleZ=True, absolute=True)
			
			
			## ROTATION
				  
			if self.chk_orient_xAxis.isChecked():
				rotate(self.sourceNodes[i],self.targetNode.getRotation(space="world")[0], rotateX=True, absolute=True, euler=True)
			else:
				rotate(self.sourceNodes[i],self.sourceNodesAttr[i].rotation[0], rotateX=True, absolute=True, euler=True)
			   
			if self.chk_orient_yAxis.isChecked():
				rotate(self.sourceNodes[i],self.targetNode.getRotation(space="world")[1], rotateY=True, absolute=True, euler=True)
			else:
				rotate(self.sourceNodes[i],self.sourceNodesAttr[i].rotation[1], rotateY=True, absolute=True, euler=True)
				
			if self.chk_orient_zAxis.isChecked():
				rotate(self.sourceNodes[i],self.targetNode.getRotation(space="world")[2], rotateZ=True, absolute=True, euler=True)
			else:
				rotate(self.sourceNodes[i],self.sourceNodesAttr[i].rotation[2], rotateZ=True, absolute=True, euler=True)
			
			
			
			## POSITION
			targetAlignToOffset = targetAlignTo[:]
			
			if self.rb_pos_src_center.isChecked():
				if self.chk_pos_xPos.isChecked(): targetAlignToOffset[0] += (self.sourceNodesAttr[i].position[0] - self.sourceNodesAttr[i].center[0])
				if self.chk_pos_yPos.isChecked(): targetAlignToOffset[1] += (self.sourceNodesAttr[i].position[1] - self.sourceNodesAttr[i].center[1])
				if self.chk_pos_zPos.isChecked(): targetAlignToOffset[2] += (self.sourceNodesAttr[i].position[2] - self.sourceNodesAttr[i].center[2])
			
			if self.rb_pos_src_min.isChecked():
				if self.chk_pos_xPos.isChecked(): targetAlignToOffset[0] += (self.sourceNodesAttr[i].position[0] - self.sourceNodesAttr[i].boundingBox[0])
				if self.chk_pos_yPos.isChecked(): targetAlignToOffset[1] += (self.sourceNodesAttr[i].position[1] - self.sourceNodesAttr[i].boundingBox[1])
				if self.chk_pos_zPos.isChecked(): targetAlignToOffset[2] += (self.sourceNodesAttr[i].position[2] - self.sourceNodesAttr[i].boundingBox[2])
				
			if self.rb_pos_src_max.isChecked():
				if self.chk_pos_xPos.isChecked(): targetAlignToOffset[0] += (self.sourceNodesAttr[i].position[0] - self.sourceNodesAttr[i].boundingBox[3])
				if self.chk_pos_yPos.isChecked(): targetAlignToOffset[1] += (self.sourceNodesAttr[i].position[1] - self.sourceNodesAttr[i].boundingBox[4])
				if self.chk_pos_zPos.isChecked(): targetAlignToOffset[2] += (self.sourceNodesAttr[i].position[2] - self.sourceNodesAttr[i].boundingBox[5])
				
			if self.rb_pos_src_pivot.isChecked():
				if self.chk_pos_xPos.isChecked(): targetAlignToOffset[0] += (self.sourceNodesAttr[i].position[0] - self.sourceNodesAttr[i].pivot[0])
				if self.chk_pos_yPos.isChecked(): targetAlignToOffset[1] += (self.sourceNodesAttr[i].position[1] - self.sourceNodesAttr[i].pivot[1])
				if self.chk_pos_zPos.isChecked(): targetAlignToOffset[2] += (self.sourceNodesAttr[i].position[2] - self.sourceNodesAttr[i].pivot[2])
			
			
			#Apply final offset to target coords, and perform the move 
			finalTargetPos = self.sourceNodesAttr[i].position[:]
		   
			 
			if self.chk_pos_xPos.isChecked():
				finalTargetPos[0] = targetAlignToOffset[0]
			if self.chk_pos_yPos.isChecked():
				finalTargetPos[1] = targetAlignToOffset[1]
			if self.chk_pos_zPos.isChecked():
				finalTargetPos[2] = targetAlignToOffset[2]
			
			move(self.sourceNodes[i],finalTargetPos)
				  
				   
			
	def getAbsoluteScale(self,node):
		currentNode = node
		currentScale = node.getScale()

		while currentNode :
			if currentNode.getParent() :
				currentNode = currentNode.getParent()
				currentScale[0] *= currentNode.getScale()[0]
				currentScale[1] *= currentNode.getScale()[1]
				currentScale[2] *= currentNode.getScale()[2]
			else:
				currentNode = False;
		return currentScale
	

	def showEvent(self, event):
		## OPEN UNDO CHUNK!
		undoInfo(openChunk = True)
		self.targetNode = selected()[len(selected())-1]
		if (listRelatives(self.targetNode)[0].nodeType() == "mesh"):
			self.targetBB = exactWorldBoundingBox(listRelatives(self.targetNode)[0])
		else:	
			self.targetBB = exactWorldBoundingBox(self.targetNode)
		
		self.sourceNodes = selected()[:-1]
		self.sourceNodesAttr = []
		
		# Generate bounding box coords for source and target nodes
		for node in self.sourceNodes :
			self.sourceNodesAttr.append(CryMaya_AlignToolSourceNode(node))
		
		self.updatePreview()
		
class CryMaya_AlignToolSourceNode():
	def __init__(self, node):
		self.position = node.getTranslation(space='world')
		self.pivot = node.getRotatePivot(space='world')
		self.rotation = node.getRotation()
		self.scale = node.getScale()
		if (listRelatives(node)[0].nodeType() == "mesh"):
			self.boundingBox = exactWorldBoundingBox(listRelatives(node)[0])
			self.center = objectCenter(listRelatives(node)[0])
		else:
			self.boundingBox = exactWorldBoundingBox(node)
			self.center = objectCenter(node)
		
		

def CryMaya_AlignTool():
		
	if (len(selected()) == 0):
		warning("Nothing Selected! : Select 2 or more nodes to align")
	elif (len(selected()) == 1):
		warning("No Target Selected! : Select 2 or more nodes to align")
	elif (len(selected()) > 1):
		#Open Align Dialog
		
		result = CryMayaAlignTool.exec_()
		undoInfo(closeChunk = True)
		#closed undo chunk!
		#if dialog was cancelled/closed
		if result == 0 :
			undo()
		
		



#On script load/import, create instance
CryMayaAlignTool = CryMaya_AlignToolDialog()
