import maya.cmds as cmds
import maya.OpenMayaUI as mui
import sip, os
from PyQt4 import QtGui, QtCore, uic
import CryRigging as cr
from CryRigging import charParts as cp

def show():
	return facialToolbox()

class facialToolbox(QtGui.QDialog):
	face = None
	head = None
	hmc = None
	
	def __init__(self):
		
		ptr = mui.MQtUtil.mainWindow()
		mayaMainWindow = sip.wrapinstance(long(ptr), QtCore.QObject)
		QtGui.QDialog.__init__(self, parent=mayaMainWindow)
		
		#TODO: use the namespace queries of the CryChar class to check these below, in case the CryChar is imported into a namespace
		
		#controllers as of v14 of the rig
		self.faceControls = [u'CTL_R_brow_raiseOut', u'CTL_R_brow_raiseIn', u'CTL_L_brow_raiseIn', u'CTL_L_brow_raiseOut', \
		u'CTL_R_brow_down', u'CTL_L_brow_down', u'CTL_R_brow_lateral', u'CTL_L_brow_lateral', u'CTL_L_neck_stretch', \
		u'CTL_R_neck_stretch', u'CTL_C_tongue', u'CTL_C_tongueRoll', u'CTL_L_eye', u'CTL_R_eye', u'CTL_C_eye', u'CTL_L_eye_blink', \
		u'CTL_R_eye_blink', u'CTL_L_mouth_dimple', u'CTL_L_mouth_cornerDepress', u'CTL_L_mouth_stretch', u'CTL_L_mouth_lowerLipDepress', \
		u'CTL_R_mouth_upperLipRaise', u'CTL_R_mouth_sharpCornerPull', u'CTL_R_mouth_cornerPull', u'CTL_R_mouth_dimple', \
		u'CTL_R_mouth_cornerDepress', u'CTL_R_mouth_stretch', u'CTL_R_mouth_lowerLipDepress', u'CTL_L_mouth_cornerPull', \
		u'CTL_L_mouth_sharpCornerPull', u'CTL_L_mouth_upperLipRaise', u'CTL_C_mouth', u'CTL_L_nose', u'CTL_R_nose', \
		u'CTL_C_jaw', u'CTL_L_ear_up', u'CTL_R_ear_up']
		
		self.eyeControls = [u'CTL_L_eye', u'CTL_R_eye', u'CTL_C_eye', u'CTL_L_eye_blink', u'CTL_R_eye_blink']
		
		self.lipControls = [u'CTL_R_mouth_upperLipRaise', u'CTL_R_mouth_sharpCornerPull', u'CTL_L_mouth_sharpCornerPull', \
		u'CTL_L_mouth_upperLipRaise', u'CTL_L_mouth_dimple', u'CTL_L_mouth_cornerDepress', u'CTL_L_mouth_stretch', \
		u'CTL_L_mouth_lowerLipDepress', u'CTL_R_mouth_stretch', u'CTL_R_mouth_lowerLipDepress', u'CTL_R_mouth_cornerPull', \
		u'CTL_R_mouth_dimple', u'CTL_R_mouth_cornerDepress', u'CTL_L_mouth_cornerPull']


		
		#pathing: home, local office, network
		uiPath = None
		print (os.path.dirname(str(__file__)) + '/facialLoad.ui').replace('/','\\')
		try: uiPath = (os.path.dirname(str(__file__)) + '/facialLoad.ui').replace('/','\\')
		except: uiPath = 'J:\\data\\Production\\TechArt\\Builds\\Latest\\Tools\\CryMayaTools\\CryRigging\\shapeWrangler\\shapeWrangler.ui'

		self.ui = uic.loadUi(uiPath)
		self.ui.show()
		
		self.connect(self.ui.characterCMB , QtCore.SIGNAL("currentIndexChanged(int)") , self.refreshUI)
		
		
		##Facial tools tab
		######################
		self.connect(self.ui.horizSelChkBTN, QtCore.SIGNAL("clicked()"), self.horizSelChkFn)
		self.connect(self.ui.vertSelChkBTN, QtCore.SIGNAL("clicked()"), self.vertSelChkFn)
		self.connect(self.ui.selectionDepthSLDR, QtCore.SIGNAL("valueChanged(int)"), self.selectionDepthFn)
		self.connect(self.ui.keyFaceBTN, QtCore.SIGNAL("clicked()"), self.keyFaceFn)
		self.connect(self.ui.keyEyesBTN, QtCore.SIGNAL("clicked()"), self.keyEyesFn)
		self.connect(self.ui.keyLipsBTN, QtCore.SIGNAL("clicked()"), self.keyLipsFn)
		self.connect(self.ui.resetFaceBTN, QtCore.SIGNAL("clicked()"), self.resetFaceFn)
		self.connect(self.ui.resetEyesBTN, QtCore.SIGNAL("clicked()"), self.resetEyesFn)
		self.connect(self.ui.resetLipsBTN, QtCore.SIGNAL("clicked()"), self.resetLipsFn)
		#cameras
		self.connect(self.ui.cameraHeadBTN, QtCore.SIGNAL("clicked()"), self.cameraHeadFn)
		
		
		##HMC tab
		######################
		self.connect(self.ui.loadBTN, QtCore.SIGNAL("clicked()"), self.loadMovie)
		self.connect(self.ui.tcInTimeSliderBTN, QtCore.SIGNAL("clicked()"), self.tcInTimeSliderFn)
		
		#on tab changed
		self.connect(self.ui.tabs, QtCore.SIGNAL("currentChanged(int)"), self.refreshUI)
		
		self.refreshCharacterCMB()
		
		#setup UI
		if self.face:
			if self.face.horizontalSelection == 1:
				self.ui.horizSelChkBTN.setChecked(True)
				self.ui.horizSelChkBTN.setText('HORIZONTAL SELECTION ON')
			if self.face.verticalSelection == 1:
				self.ui.vertSelChkBTN.setChecked(True)
				self.ui.vertSelChkBTN.setText('VERTICAL SELECTION ON')
			self.ui.selectionDepthSLDR.setValue(self.face.selectionDepth)
			
		#TODO: delete the HMC cam on close	
		
	def refreshCharacterCMB(self, debug=1):
		faces = []
		
		for charPart in cmds.ls(type = "cryCharPart"):
			if cmds.getAttr(charPart + '.partType') == 'face': faces.append(charPart)
		
		if debug: print faces
		
		if faces:
			self.ui.characterCMB.addItems(faces)
			self.face = cr.charParts.RyseFace(str(self.ui.characterCMB.currentText()))
			self.head = cr.CryChar(self.face.character)
		else:
			cmds.warning('facialToolbox>>> No faces in scene!')
			return False
	
	def refreshUI(self, index, debug=1):
		#query charCMB txt
		self.face = cp.RyseFace(str(self.ui.characterCMB.currentText()))
		self.head = cr.CryChar(self.face.character)
		
		#refresh tabs
		tab = self.ui.tabs.currentIndex()
		if tab == 0:
			if debug: print 'Refreshing Face Load Tab'
		if tab == 1:
			if debug: print 'Refreshing HMC Load Tab'
	
	def loadMovie(self, debug=1):
		fPath = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
		if fPath:
			#create shading node and plane
			if not cmds.objExists('hmc_video'):
				#create plane
				cmds.polyPlane(name='hmc_plane')
				
				#create / assign shader
				movieNode = cmds.shadingNode('movie', n='hmc_video', at=1)
				shaderNode = cmds.shadingNode('lambert', n='hmc_shader', asShader=1)
				cmds.setAttr('hmc_video.filterType', 0)
				cmds.setAttr('hmc_video.useFrameExtension', 1)
				cmds.connectAttr('hmc_video.outColor', 'hmc_shader.color', f=1)
				cmds.select('hmc_plane')
				cmds.hyperShade('hmc_plane', assign='hmc_shader')
			cmds.setAttr('hmc_video.fileTextureName', fPath, type='string')
			
			#fill in UI info
			hmc = str(fPath)
			self.ui.loadBTN.setText(fPath.split('/')[-1])
			tc = cmds.movieInfo(hmc, tc=1)
			ftc = '%s:%s:%s:%s' % (tc[0], tc[1], tc[2], tc[3])
			self.ui.tcLINE.setText(ftc)
			self.ui.numframesLINE.setText(str(cmds.movieInfo(hmc, f=1)[0]))
			self.ui.fpsLINE.setText(str(cmds.movieInfo(hmc, nf=1)[0]))
			self.ui.resolutionLINE.setText((str(cmds.movieInfo(hmc, w=1)[0]) + 'x' + str(cmds.movieInfo(hmc, h=1)[0])))
			if self.ui.setTimeRangeToHmcCHK.isChecked():
				frameStart = cr.tc2f([tc[0],tc[1],tc[2],tc[3]], frame_rate=30)
				numFrames = cmds.movieInfo(hmc, f=1)[0]
				if debug: print frameStart, numFrames
				frameEnd = (frameStart + numFrames)
				cmds.playbackOptions(max=frameEnd)
				cmds.playbackOptions(animationEndTime=frameEnd)
				cmds.playbackOptions(animationStartTime=frameStart)
				cmds.playbackOptions(min=frameStart)
	
	def loadFaceFn(self, debug=1):
		fPath = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.'))
		if fPath:
			fname = str(fPath.split('/')[-1])
			if debug: print 'loadFaceFn>>>',fPath, fname
			cmds.file(fPath, i=1, type='mayaAscii', ra=1, namespace='face:')
	
	def tcInTimeSliderFn(self):
		if self.ui.tcInTimeSliderBTN.isChecked():
			cmds.animDisplay(timeCode=1)
		else: cmds.animDisplay(timeCode=0)
	
	############################################################################
	##FACIAL TOOLS TAB
	############################################################################
	
	def horizSelChkFn(self):
		if self.ui.horizSelChkBTN.isChecked():
			self.face.horizontalSelection = 1
			self.ui.horizSelChkBTN.setText('HORIZONTAL SELECTION ON')
		else: 
			self.face.horizontalSelection = 0
			self.ui.horizSelChkBTN.setText('HORIZONTAL SELECTION OFF')
			
	def vertSelChkFn(self):
		if self.ui.vertSelChkBTN.isChecked():
			self.face.verticalSelection = 1
			self.ui.vertSelChkBTN.setText('VERTICAL SELECTION ON')
		else: 
			self.face.verticalSelection = 0
			self.ui.vertSelChkBTN.setText('VERTICAL SELECTION OFF')
			
	def selectionDepthFn(self, val):
		self.head.selectionDepth = val
		
	def keyFaceFn(self):
		cmds.setKeyframe(self.faceControls)
	
	def keyEyesFn(self):
		cmds.setKeyframe(self.eyeControls)
	
	def keyLipsFn(self):
		cmds.setKeyframe(self.lipControls)
	
	def resetFaceFn(self):
		cmds.cutKey(self.faceControls, time=(cmds.currentTime(q=1),))
	
	def resetEyesFn(self):
		cmds.cutKey(self.eyeControls, time=(cmds.currentTime(q=1),))
	
	def resetLipsFn(self):
		cmds.cutKey(self.lipControls, time=(cmds.currentTime(q=1),))
		
	def cameraHeadFn(self):
		if self.face:
			if not self.hmc: self.hmc = cmds.camera(name='hmc_cam')[0]
			facialRoot = None
			for jnt in cr.skeleTools.selectHi(self.head.animSkeletonRoot[0]):
				if 'FacialRoot' in jnt: facialRoot = jnt
			if facialRoot:
				cmds.xform(self.hmc, m=cmds.xform(facialRoot, m=1, q=1, ws=1))
				cmds.setAttr(self.hmc + '.translateZ', -46)
				cmds.lookThru(self.hmc)
