import os
import sip

from PyQt4 import QtGui, QtCore, uic

import maya.OpenMayaUI as openMayaUI
import maya.OpenMaya as openMaya
import maya.mel as mel
import maya.cmds as cmds

def getMayaWindow():
	ptr = openMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)

selfDirectory = os.path.dirname(__file__)
uiFile = selfDirectory + '/orientDriver.ui'

form_class, base_class = uic.loadUiType(uiFile)

def open():
	global orientDriverWindow
	try:
		orientDriverWindow.close()
	except:
		pass

	orientDriverWindow = orientDriverUI()
	orientDriverWindow.show()
	
class orientDriverUI(base_class, form_class):
	title = 'cryOrientDriver v0.1 alpha'
	
	def __init__(self, parent=getMayaWindow()):
		super(orientDriverUI, self).__init__(parent)

		self.setupUi(self)
		self.setWindowTitle(self.title)

		windowUIName = openMayaUI.MQtUtil.fullName(long(sip.unwrapinstance(self)))
		if cmds.window('orientDriverWindow', q=1, ex=1):
			cmds.deleteUI('orientDriverWindow')

		cmds.window('orientDriverWindow', widthHeight=(380, 600), resizeToFitChildren=1)
		
		# create
		self.connect(self.bDriverJoint, QtCore.SIGNAL("clicked()"), self.fnDriverJoint)
		self.connect(self.bParentJoint, QtCore.SIGNAL("clicked()"), self.fnParentJoint)
		self.connect(self.bCreateOrientDriver, QtCore.SIGNAL("clicked()"), self.fnCreateOrientDriver)
		
		# manage
		self.connect(self.bDelete, QtCore.SIGNAL("clicked()"), self.fnDelete)
		self.connect(self.bSceneRefresh, QtCore.SIGNAL("clicked()"), self.fnSceneRefresh)
		
		# connections
		self.lOrientDriverList.itemClicked.connect(self.fnOrientDriverListItemClicked)
		self.lTab3OrientDriverList.itemClicked.connect(self.fnTab3OrientDriverList)
		self.spMinAngle.valueChanged.connect(self.fnMinAngle)
		self.spMaxAngle.valueChanged.connect(self.fnMaxAngle)
		self.spMinWeightClamp.valueChanged.connect(self.fnMinWeightClamp)
		self.spMaxWeightClamp.valueChanged.connect(self.fnMaxWeightClamp)
		self.spScale.valueChanged.connect(self.fnScale)
		self.cbLocalAim.currentIndexChanged.connect(self.fnLocalAimIndexChanged)
		
		# driven joints
		self.connect(self.bTab3DrivenJoint, QtCore.SIGNAL("clicked()"), self.fnTab3DrivenJoint)
		self.connect(self.bTab3CreateCtrl, QtCore.SIGNAL("clicked()"), self.fnTab3CreateCtrl)
		self.connect(self.bTab3GetCtrl, QtCore.SIGNAL("clicked()"), self.fnTab3GetCtrl)
		self.connect(self.bTab3GetStartLocator, QtCore.SIGNAL("clicked()"), self.fnTab3GetStartLocator)
		self.connect(self.bTab3GetEndLocator, QtCore.SIGNAL("clicked()"), self.fnTab3GetEndLocator)
		
		self.connect(self.bTab3EndTransform, QtCore.SIGNAL("clicked()"), self.fnTab3EndTransform)
		self.connect(self.bTab3StartTransform, QtCore.SIGNAL("clicked()"), self.fnTab3StartTransform)
		self.connect(self.bTab3CreateInterpolator, QtCore.SIGNAL("clicked()"), self.fnTab3CreateInterpolator)
		self.connect(self.bTab3DeleteInterpolator, QtCore.SIGNAL("clicked()"), self.fnTab3DeleteInterpolator)
		self.connect(self.bTab3RefreshInterpolator, QtCore.SIGNAL("clicked()"), self.fnTab3RefreshInterpolator)
		self.connect(self.bTab3CreateLink, QtCore.SIGNAL("clicked()"), self.fnTab3CreateLink)
		self.cbInterpolators.currentIndexChanged.connect(self.fnInterpolatorsIndexChanged)
		self.connect(self.bTab3SceneRefresh, QtCore.SIGNAL("clicked()"), self.fnTab3SceneRefresh)
		
		# export
		self.connect(self.bExport, QtCore.SIGNAL("clicked()"), self.fnExport)
		
								
		self.fnRefreshOrientDriverList(self.lOrientDriverList)
		self.fnRefreshOrientDriverList(self.lTab3OrientDriverList)
		self.fnTab3RefreshInterpolator()
		
	def fnExport(self):
		filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".odf"))
		cmds.cryOdCmd(jj=filename)
		
	def fnTab3GetCtrl(self):
		selection = cmds.ls(sl=1, type='transform')
		if len(selection) > 0:
			self.edTab3CtrlGrp.setText(selection[0])
			
	def fnTab3GetStartLocator(self):
		selection = cmds.ls(sl=1, type='transform')
		if len(selection) > 0:
			self.edTab3StartLoc.setText(selection[0])
		
	def fnTab3GetEndLocator(self):
		selection = cmds.ls(sl=1, type='transform')
		if len(selection) > 0:
			self.edTab3EndLoc.setText(selection[0])

	def fnInterpolatorsIndexChanged(self):
		itemText = str(self.cbInterpolators.currentText())
		if itemText is None:
			return
			
		cmds.select(itemText)
		
	def fnTab3SceneRefresh(self):
		self.fnRefreshOrientDriverList(self.lTab3OrientDriverList)

	def fnRefreshOrientDriverList(self, container):
		container.clear()
		orientDriverNodes = cmds.ls(type='cryOrientDriver')
		for odn in orientDriverNodes:
			container.addItem(odn);

	def fnTab3DeleteInterpolator(self):
		itemText = str(self.cbInterpolators.currentText())
		if len(itemText) == 0:
			return
			
		cmds.delete(itemText)
		self.fnTab3RefreshInterpolator()
			
	def fnTab3RefreshInterpolator(self):
		self.cbInterpolators.clear()
		interpNodes = cmds.ls(type='cryInterpolator')
		for o in interpNodes:
			self.cbInterpolators.addItem(o);
			
	def fnTab3CreateInterpolator(self):
		cmds.createNode('cryInterpolator')
		self.fnTab3RefreshInterpolator()
		
	def fnTab3CreateLink(self):
		orientDriverNode = self.fnGetCurrentItem(self.lTab3OrientDriverList)
		if orientDriverNode is None or len(orientDriverNode) == 0:
			cmds.warning("No orientDriver node selected")
			return
			
		interpNode = str(self.cbInterpolators.currentText())
		if len(interpNode) == 0:
			cmds.warning("No cryInterpolator node node selected")
			return			

		drivenJointName = str(self.edTab3DrivenJoint.text())
		if len(drivenJointName) == 0:
			cmds.warning("No driven joint found. Please enter one")
			return
		
		fromLoc = str(self.edTab3StartLoc.text())
		if len(fromLoc) == 0:
			cmds.warning("Select a start locator")
			return
			
		toLoc = str(self.edTab3EndLoc.text())
		if len(toLoc) == 0:
			cmds.warning("Select an end locator")
			return

		ctrlCurve = str(self.edTab3CtrlGrp.text())
		if len(ctrlCurve) == 0:
			cmds.warning("Select a joints controller")
			return
			
		ctrlGrp = cmds.listRelatives(ctrlCurve, p=True)[0]
		if ctrlGrp is None:
			cmds.error("Controller " + ctrlCurve + " has no parent")
			return
			
		numConns = cmds.getAttr(interpNode+'.transforms', size=1)
		nextConn = str(numConns)

		cmds.connectAttr(fromLoc+'.worldMatrix[0]', interpNode+'.transforms['+nextConn+'].fromMatrix')
		cmds.connectAttr(fromLoc+'.parentMatrix[0]', interpNode+'.transforms['+nextConn+'].fromParentMatrix')
		
		cmds.connectAttr(toLoc+'.worldMatrix[0]', interpNode+'.transforms['+nextConn+'].toMatrix')
		cmds.connectAttr(toLoc+'.parentMatrix[0]', interpNode+'.transforms['+nextConn+'].toParentMatrix')

		cmds.connectAttr(orientDriverNode+'.outWeight', interpNode+'.transforms['+nextConn+'].weight')
		
		# we only connect once
		if numConns == 0:
			cmds.connectAttr(interpNode+'.translate', ctrlGrp+'.translate')
			cmds.connectAttr(interpNode+'.rotate', ctrlGrp+'.rotate')
			
		# remove offset created on the controller
		cmds.setAttr(ctrlCurve+'.tx', 0)
		cmds.setAttr(ctrlCurve+'.ty', 0)
		cmds.setAttr(ctrlCurve+'.tz', 0)
		cmds.setAttr(ctrlCurve+'.rx', 0)
		cmds.setAttr(ctrlCurve+'.ry', 0)
		cmds.setAttr(ctrlCurve+'.rz', 0)
			
		print('Created link: ' + orientDriverNode + ' -> ' + interpNode + ' -> ' + str(ctrlGrp))

	def fnTab3StartTransform(self):
		drivenJointName = str(self.edTab3DrivenJoint.text())
		if (drivenJointName is None) or (len(drivenJointName) == 0):
			cmds.warning("No driven joint found. Please enter one")
			return
		
		startLocator = cmds.spaceLocator(name=drivenJointName+'_startLoc_#')[0]
		grp = cmds.group(startLocator, n = drivenJointName+'_grp_startLoc_#')
		
		cmds.delete(cmds.pointConstraint(drivenJointName, grp, w=1))
		cmds.delete(cmds.orientConstraint(drivenJointName, grp, w=1))

		prt = cmds.listRelatives(drivenJointName, type='joint', p=True)[0]
		cmds.parent(grp, prt)
		
		self.edTab3StartLoc.setText(startLocator)

	def fnTab3EndTransform(self):
		drivenJointName = str(self.edTab3DrivenJoint.text())
		if len(drivenJointName) == 0:
			cmds.warning("No driven joint found. Please enter one")
			return
			
		startGrp = str(self.edTab3StartLoc.text())
		
		endLocator = cmds.spaceLocator(name=drivenJointName+'_endLoc_#')[0]
		grp = cmds.group(endLocator, n = drivenJointName+'_grp_endLoc_#')
		
		cmds.delete(cmds.pointConstraint(startGrp, grp, w=1))
		cmds.delete(cmds.orientConstraint(startGrp, grp, w=1))

		cmds.delete(cmds.pointConstraint(drivenJointName, endLocator, w=1))
		cmds.delete(cmds.orientConstraint(drivenJointName, endLocator, w=1))

		prt = cmds.listRelatives(drivenJointName, type='joint', p=True)[0]
		if prt is not None:
			cmds.parent(grp, prt)
		
		self.edTab3EndLoc.setText(endLocator)
		
	def fnTab3CreateCtrl(self):
		drivenJointName = str(self.edTab3DrivenJoint.text())
		if len(drivenJointName) == 0:
			cmds.warning("No driven joint found. Please enter one")
			return
		
		curve = cmds.circle (n = drivenJointName + 'driven_ctrl_#', c =(0, 0, 0), nr = (0, 1, 0), sw = 360, r = 4, d = 3, ut = 0, tol = 0.01, s = 8, ch = 0)
		grp = cmds.group(curve, n = drivenJointName + 'driven_group_#')
		grp2 = cmds.group(grp, n = drivenJointName + 'driven_group_#')
		
		prt = cmds.listRelatives(drivenJointName, type='joint', p=True)[0]
		cmds.delete(cmds.pointConstraint(drivenJointName, grp2, w=1))
		cmds.delete(cmds.orientConstraint(drivenJointName, grp2, w=1))
		
		if prt is not None:
			cmds.parent(grp2, prt)
		cmds.parentConstraint(curve, drivenJointName, w=1)
		
		self.edTab3CtrlGrp.setText(curve[0])
		
	def fnTab3DrivenJoint(self):
		selection = cmds.ls(sl=1, type='joint')
		if len(selection) > 0:
			self.edTab3DrivenJoint.setText(selection[0])
		
	def fnMinAngle(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		value = self.spMinAngle.value()
		cmds.setAttr(itemText+'.minAngle', value)
		
	def fnMaxAngle(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		value = self.spMaxAngle.value()
		cmds.setAttr(itemText+'.maxAngle', value)

	def fnMinWeightClamp(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		value = self.spMinWeightClamp.value()
		cmds.setAttr(itemText+'.minWeightClamp', value)

	def fnMaxWeightClamp(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		value = self.spMaxWeightClamp.value()
		cmds.setAttr(itemText+'.maxWeightClamp', value)
		
	def fnScale(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		value = self.spScale.value()
		cmds.setAttr(itemText+'.scaleLimits', value)
		
	def fnLocalAimIndexChanged(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
		
		index = self.cbLocalAim.currentIndex()
		cmds.setAttr(itemText+'.localAim', index)

	def fnGetCurrentItem(self, container):
		item = container.currentItem()
		if item is None:
			return
		
		itemText = str(item.text())
		if not cmds.objExists(itemText):
			return
		
		return itemText
		
	def fnTab3OrientDriverList(self):
		itemText = self.fnGetCurrentItem(self.lTab3OrientDriverList)
		if len(itemText) == 0:
			return
			
		cmds.select(itemText)
		
	def fnOrientDriverListItemClicked(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			return
			
		cmds.select(itemText)
			
		minAngle = cmds.getAttr(itemText+'.minAngle')
		self.spMinAngle.setValue(minAngle)
		maxAngle = cmds.getAttr(itemText+'.maxAngle')
		self.spMaxAngle.setValue(maxAngle)
		minWeightClamp = cmds.getAttr(itemText+'.minWeightClamp')
		self.spMinWeightClamp.setValue(minWeightClamp)
		maxWeightClamp = cmds.getAttr(itemText+'.maxWeightClamp')
		self.spMaxWeightClamp.setValue(maxWeightClamp)
		scaleLimits = cmds.getAttr(itemText+'.scaleLimits')
		self.spScale.setValue(scaleLimits)
		localAim = cmds.getAttr(itemText+'.localAim')
		self.cbLocalAim.setCurrentIndex(localAim)

	def fnDelete(self):
		itemText = self.fnGetCurrentItem(self.lOrientDriverList)
		if len(itemText) == 0:
			xform = cmds.listRelatives(itemText, type='transform', p=True)[0]
			cmds.delete(itemText)
			cmds.delete(xform)
			self.fnRefreshOrientDriverList(self.lOrientDriverList)
			self.fnRefreshOrientDriverList(self.lTab3OrientDriverList)

	def fnSceneRefresh(self):
		self.fnRefreshOrientDriverList(self.lOrientDriverList)
			
	def fnCreateNewName(self, prefix, text):
		ns = text.rpartition(':')[0]
		name = text.rpartition(':')[2]

		final = prefix + '_' + name
		if len(ns) > 0:
			final = ns + ':' + final
			
		return final
		
	def fnDriverJoint(self):
		selection = cmds.ls(sl=1, type='joint')
		if len(selection) > 0:
			finalName = self.fnCreateNewName('orientDriver', selection[0])
			self.edDriverJoint.setText(selection[0])
			self.edName.setText(finalName)
			prt = cmds.listRelatives(selection[0], type='joint', p=True)[0]
			self.edParentJoint.setText(str(prt))

	def fnParentJoint(self):
		selection = cmds.ls(sl=1, type='joint')
		if len(selection) > 0:
			self.edParentJoint.setText(selection[0])

	def fnCreateOrientDriver(self):
		driverJoint = str(self.edDriverJoint.text())
		parentJoint = str(self.edParentJoint.text())
		orientDriverName = str(self.edName.text())
		
		if len(driverJoint) > 0 or len(parentJoint) > 0:
			if cmds.objExists(driverJoint) and cmds.objExists(parentJoint):
				orientDriverNode = cmds.createNode('cryOrientDriver', n=orientDriverName+'_#')
				xformOrientDriver = cmds.listRelatives(orientDriverNode, type='transform', p=True)[0]

				cmds.connectAttr(xformOrientDriver+'.worldMatrix[0]', orientDriverNode+'.worldMatrixPose')
				cmds.connectAttr(driverJoint+'.worldMatrix[0]', orientDriverNode+'.worldMatrixLive')

				cmds.delete(cmds.pointConstraint(driverJoint, xformOrientDriver, w=1))
				cmds.delete(cmds.orientConstraint(driverJoint, xformOrientDriver, w=1))
				cmds.parent(xformOrientDriver, parentJoint)
				
				xformName = self.fnCreateNewName('xform', orientDriverName)
				xformOrientDriver = cmds.rename(xformOrientDriver, xformName);

				self.edDriverJoint.setText("")
				self.edParentJoint.setText("")
				self.edName.setText("")
				
				self.fnRefreshOrientDriverList(self.lOrientDriverList)
				self.fnRefreshOrientDriverList(self.lTab3OrientDriverList)
				
