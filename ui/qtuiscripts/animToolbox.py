from PyQt4 import QtGui, QtCore, uic
from functools import partial
from copy import deepcopy
import sys, os, sip

import maya.cmds as cmds
import maya.OpenMayaUI as mui
import maya.OpenMaya as om

import CryRigging as cr
from CryRigging import rigParts as rp
from CryRigging import charParts as cp
import CryCore as cc
from CryPythonTools import pyTek
import CryAnimation.globals as cag
import CryAnimation.Scene_Manager_Keys as k

__author__ = 'riham', 'haraldz'
__version__ = 0.21


## quick runtime fix
gdp = cmds.optionVar( q = 'CryGameDataPath' )
cmds.optionVar( stringValue = ( "CryGameDataPath", gdp.replace( '\\', '/' ) ) )

'''
from CryAnimation.animToolbox import animToolbox
animToolbox.show()
'''

def getMayaWindow():
	##'Get the maya main window as a QMainWindow instance'	
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance( long( ptr ), QtCore.QObject )

## Get the absolute path to my ui file
uiFile = ( os.path.dirname( str( __file__ ) ) + '/animToolbox.ui' ).replace( '/', '\\' )
form_class, base_class = uic.loadUiType( uiFile )

@pyTek.catchErrors
class Window( base_class, form_class ):	

	def __init__( self, parent = getMayaWindow() ):
		super( base_class, self ).__init__( parent )
		self.setupUi( self )
		self.projectPath = cmds.optionVar( q = 'CryGameDataPath' )
		self.currentCharacter = None

		##character tab signals/slots
		self.connect( self.get_character_BTN, QtCore.SIGNAL( "clicked()" ) , self.get_character_fn )
		self.connect( self.selectAllCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectAllCtrls_fn )
		self.connect( self.selectUniqueCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectUniqueCtrls_fn )
		self.connect( self.selectFkCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectFkCtrls_fn )
		self.connect( self.selectIkCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectIkCtrls_fn )
		self.connect( self.selectDSMBCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectDSMBCtrls_fn )
		self.connect( self.selectSettingsCtrls_BTN, QtCore.SIGNAL( "clicked()" ), self.selectSettingsCtrls_fn )
		self.connect( self.selectNullSpaces_BTN, QtCore.SIGNAL( "clicked()" ), self.selectNullSpaces_fn )
		self.connect( self.selectGlobalCtrl_BTN, QtCore.SIGNAL( "clicked()" ), self.selectGlobalCtrl_fn )
		self.connect( self.resetToDefault_BTN, QtCore.SIGNAL( "clicked()" ), self.resetToDefault_fn )
		self.connect( self.characterParts_tree , QtCore.SIGNAL( "itemDoubleClicked ( QTreeWidgetItem*, int)" ) , self.selectAllCtrls_fn )
		self.connect( self.characters_CMB , QtCore.SIGNAL( "currentIndexChanged(int)" ) , self.refreshUI )

		self.connect( self.bakeAndSetToFK_BTN, QtCore.SIGNAL( "clicked()" ), self.bakeAndSetFK_fn )
		self.connect( self.bakeAndSetToIK_BTN, QtCore.SIGNAL( "clicked()" ), self.bakeAndSetIK_fn )
		self.connect( self.loadPropsBTN, QtCore.SIGNAL( "clicked()" ), self.syncProps_fn )
		self.connect( self.refreshPropsBTN, QtCore.SIGNAL( "clicked()" ), self.refreshPropsList_fn )
		self.connect( self.refreshAttachmentPointsBTN, QtCore.SIGNAL( "clicked()" ), self.refreshAttachmentsPointsList_fn )
		self.connect( self.selectCharacterNode_BTN, QtCore.SIGNAL( "clicked()" ), self.selectCharacterNode_fn )
		
		self.connect( self.attachDefaultProps_ba_BTN, QtCore.SIGNAL( "clicked()" ), self.quickAttach_ba_fn )
		self.connect( self.attachDefaultProps_bd_BTN, QtCore.SIGNAL( "clicked()" ), self.quickAttach_bd_fn )
		self.connect( self.attachDefaultProps_bs_BTN, QtCore.SIGNAL( "clicked()" ), self.quickAttach_bs_fn )
		self.connect( self.attachDefaultProps_rs_BTN, QtCore.SIGNAL( "clicked()" ), self.quickAttach_rs_fn )
		
		if not os.environ.get( "USERNAME" ) == 'haraldz':
			self.selectCharacterNode_BTN.setHidden(True)
		
		##simulation tab signals/slots
		self.connect( self.selectSolvers_BTN, QtCore.SIGNAL( "clicked()" ) , self.selectSolvers_fn )
		self.connect( self.setSolverStartFrameToTimeSlider_BTN, QtCore.SIGNAL( "clicked()" ), self.setSolverStartFrameToTimeSlider_fn )
		self.connect( self.set_BTN, QtCore.SIGNAL( "clicked()" ), self.set_fn )

		
		##props tab setup
		self.propsList = []
		self.propAttachmentDict = {}
		##stores whether the tool has sync'd in the current session
		self.sync = None
		self.propsFolder = ( '%s/Objects/characters/props/_workfiles/MAYA/' % ( self.projectPath ) ).replace( '//', '/' )
		
		##hide p4 options
#		self.loadPropsBTN.setHidden( True )
#		self.propPathLINE.setHidden( True )
#		self.label_3.setHidden( True )
		self.propPathLINE.setText( self.propsFolder + '...' )
		
		##default starting prop.ma path
		#self.propPathLINE.setText( '//data/Games/Freedom/dev/GameRyse/Objects/characters/props/_workfiles/MAYA/props.ma' )
		#self.connect( self.loadPropsBTN, QtCore.SIGNAL( "clicked()" ) , self.getPropsP4 )
		self.connect( self.attachPropBTN, QtCore.SIGNAL( "clicked()" ) , self.attachPropFn )
		
		##on tab changed
		self.connect( self.animToolBox_tab, QtCore.SIGNAL( "currentChanged(int)" ), self.refreshUI )

		##refresh the char combo and UI on load
		self.refreshCharacter( None )
	
	def selectCharacterNode_fn( self, debug = 0 ):
		character = str( self.characters_CMB.currentText() )
		if character:
			if cmds.objExists( character ):
				cmds.select( character )
			
	def bakeAndSet_fn( self, ik = 0 ):
		startTime = cmds.playbackOptions( q = 1, min = 1 )
		endTime = cmds.playbackOptions( q = 1, max = 1 )
		
		allConstraints = []
		allControllers = []
		settingsControllers = []
		
		charParts = self.getSelectedItem()
		if not charParts:
			charParts = self.getConnections( self.getSelectedChar() + ".charParts" , "d" )
			
		for charPart in charParts:
			data = {}
			if '_arm' in charPart:
				if ik:
					data = cp.arm_fkToIk_bake( charPart, silent = 1, doNotBake = 1 )
				else:
					data = cp.arm_ikToFk_bake( charPart, silent = 1, doNotBake = 1 )
				settingsControllers.append ( cmds.listConnections( charPart + '.settingsCtrl', d = 1 )[0] )
			if '_leg' in charPart:
				if ik:
					data = cp.leg_fkToIk_bake( charPart, silent = 1, doNotBake = 1 )
				else:
					data = cp.leg_ikToFk_bake( charPart, silent = 1, doNotBake = 1 )
				settingsControllers.append ( cmds.listConnections( charPart + '.settingsCtrl', d = 1 )[0] )
			if data:
				allConstraints += data['constraints']
				allControllers += data['controllers']
		
		if allConstraints and allControllers:
			##baking keys
			cmds.bakeSimulation( allControllers, t = ( startTime, endTime ), sb = 1 )
			'''
			for i in range (startTime, endTime+1):
				cmds.currentTime(i, e=1)
				for ctl in allControllers:
					cmds.setKeyframe(ctl, breakdown=0, hierarchy='none', controlPoints=0, shape=1)
			'''
			
			##deleting constraints
			for con in allConstraints:
				cmds.delete( con )
				
			
			##setting the controller to FK
			for obj in settingsControllers:
				settingsValue = 0
				if ik:
					settingsValue = 1
				print obj
				if cmds.attributeQuery( 'arm_enableIk', node = obj, ex = True ):
					##print 'setting arm'
					try:
						animNode = cmds.listConnections( obj + '.arm_enableIk', source = 1, type = 'animCurve' )[0]
						cmds.delete( animNode )
					except:
						pass
					cmds.setAttr( '%s.arm_enableIk' % obj, settingsValue )
				if cmds.attributeQuery( 'leg_enableIk', node = obj, ex = True ):
					##print 'setting leg'
					try:
						animNode = cmds.listConnections( obj + '.leg_enableIk', source = 1, type = 'animCurve' )[0]
						cmds.delete( animNode )
					except:
						pass
					cmds.setAttr( '%s.leg_enableIk' % obj, settingsValue )
		
	def bakeAndSetFK_fn( self ):
		self.bakeAndSet_fn()

	def bakeAndSetIK_fn( self ):
		self.bakeAndSet_fn( ik = 1 )
				

	def refreshUI( self, doNotUse, debug = 0 ):
		##two 'indexChanged' functions feed into this method, i query the index instead of taking it in
		
		##query tab index
		index = self.animToolBox_tab.currentIndex()
		##query charCMB txt
		selected = str( self.characters_CMB.currentText() )
		self.currentCharacter = selected
		
		##character selection tab
		if index == 0:
			self.characterParts_tree_fn()
			if debug: print '>>>charExplorer: Refreshing character tab'
		##tools tab
		if index == 1:
			self.refreshPropsTab()
			if debug: print '>>>charExplorer: Refreshing prop tab'
		##simulation tab
		if index == 2:
			self.solvers_tree_fn()
			if debug: print '>>>charExplorer: Refreshing simulation tab'

	def getSelectedChar( self ):
		character = str( self.characters_CMB.currentText() )
		if character:
			self.currentCharacter = character
			return character
		else:
			return None

	def refreshCharacter( self, index, debug = 0 ):
		self.characters_CMB.clear()
		characters = cmds.ls( type = "cryCharacter" )
		toAdd = []
		for char in characters:
			charType = cmds.getAttr( ( char + '.characterType' ) )
			if self.ignorePropsCHK.isChecked():
				if charType != 'prop':
					toAdd.append( char )
			else:
				toAdd.append( char )
		if debug: print toAdd
		self.characters_CMB.addItems( toAdd )
		self.currentCharacter = str( self.characters_CMB.currentText() )
		
	def getConnections( self , attr , direction = 's', type = None, debug = 0 ):
		try:
			if type:
				return eval( "cmds.listConnections(attr, %s=1, type=\'%s\')" % ( direction, type ) )
			else:
				return eval( "cmds.listConnections(attr, %s=1)" % direction )
		except ValueError:
			if debug: 'Value Error: ', attr, 'Direction: ', direction
			return None	


	## CHARACTER TAB
	############

	def getCharacterFromSel( self ):
		character = cmds.ls( sl = True )
		if character:
			character = character[0]
			if cmds.nodeType( character ) == "cryCharacter":
				pass
			elif rp.attrExists( character, "rigging" ):
				charPart = self.getConnections( character + ".rigging" )
				if charPart:
					if cmds.nodeType( charPart[0] ) == "cryCharPart":
						charNode = self.getConnections( charPart[0] + ".character" )
						if charNode:
							character = charNode[0]
					elif cmds.nodeType( charPart[0] ) == "cryCharacter":
						character = charPart[0]
		return character

	def get_character_fn( self ):
		character = self.getCharacterFromSel()
		if character:
			self.characters_CMB.setCurrentIndex( self.characters_CMB.findText( character ) )

	def characterParts_tree_fn( self ):
		self.characterParts_tree.clear()
		character = self.getSelectedChar()			

		if character:
			charParts = self.getConnections( character + ".charParts" , "d" )
			if charParts:
				for part in charParts:
					wid1 = QtGui.QTreeWidgetItem()
					wid1.setText( 0, part )
					font = wid1.font( 0 )
					font.setPointSize( 11 )
					wid1.setFont( 0, font )
					self.characterParts_tree.addTopLevelItem( wid1 )
				
	def getSelectedItem( self ):
		items = self.characterParts_tree.selectedItems()
		itemsList = []
		for i in items:
			itemsList.append( str( i.text( 0 ) ) )
		return itemsList
				
	def selectAllCtrls_fn( self, temp = 0 ):
		charParts = self.getSelectedItem()
		##check if there are character parts selected
		if charParts:
			cmds.select( clear = 1 )
			for part in charParts:
				ctrls = self.getConnections( part + ".controllers" , "d" )
				if ctrls:
					for c in ctrls:
						cmds.select( c , add = 1 )
		##if there are no character parts selected , this means that the user wants to select all the character controllers
		else:
			if self.currentCharacter:
				ctrls = cr.getCharacterCons( self.currentCharacter, shared = 0 , unique = 0 , all = 1 )
				cmds.select( ctrls )

	def selectCtrls_fn( self , conType ):
		items = self.getSelectedItem()
		returnCtrls = []
		charParts = []
		
		if items: #charParts were selected
			charParts = items
		else: # no charParts selected - query ALL charParts for the character
			charParts = cr.getCharParts( self.currentCharacter )
			
		for charPart in charParts:
			controllers = cr.getCons( charPart, conType )
			returnCtrls += controllers			

		if returnCtrls:
			cmds.select ( returnCtrls )
		else:
			if items:
				print ( 'No %s controllers found for selected character parts' % conType )
			else:
				print ( "Character doesn't have any %s controllers" % conType )

	def selectUniqueCtrls_fn( self ):
		ctrls = self.selectCtrls_fn( "UNQ" )
			
	def selectFkCtrls_fn( self ):
		ctrls = self.selectCtrls_fn( "FK" )
	
	def selectIkCtrls_fn( self ):
		ctrls = self.selectCtrls_fn( "IK" )
			
	def selectDSMBCtrls_fn( self ):
		self.selectCtrls_fn( "DSMB" )
			
	def selectSettingsCtrls_fn( self ):
		charParts = []
		items = self.getSelectedItem()
		##check if there are character parts selected
		if items:
			charParts = items
		else:
			charParts = self.getConnections( self.currentCharacter + ".charParts" , "d" )
		if charParts:
			cmds.select( clear = 1 )
			for part in charParts:
				if rp.attrExists( part , "settingsCtrl" ):
					settingsCtrls = self.getConnections( part + ".settingsCtrl" , "d" )
					if settingsCtrls:
						for ctrl in settingsCtrls:
							cmds.select( ctrl, add = 1 )
					else:
						cmds.warning( "there are no settings controllers for %s" % part )
						print ( "there are no settings controllers for %s" % part )
				else:
					print ( "there are no settings controllers for %s" % part )
					
	def selectNullSpaces_fn( self ):
		character = self.currentCharacter
		if character:
			if rp.attrExists( character, "nullSpaces" ):
				nulls = self.getConnections( character + ".nullSpaces" , "d" )
				if nulls:
					cmds.select( clear = 1 )
					cmds.select( nulls )
				else:
					cmds.warning( "there are no null spaces controllers for %s" % character )
					print ( "there are no null spaces controllers for %s" % character )
					
	def selectGlobalCtrl_fn( self ):
		character = self.currentCharacter
		if character:
			if rp.attrExists( self.currentCharacter, "globalCtrl" ):
				globalCtrl = self.getConnections( self.currentCharacter + ".globalCtrl" , "d" )
				if globalCtrl:
					cmds.select( clear = 1 )
					cmds.select( globalCtrl )
				else:
					cmds.warning( "there is no global controller for %s" % character )
					print ( "there is no global controller for %s" % character )
					
	def resetToDefault_fn( self ):
		cmds.undoInfo( openChunk = True )
		try:
			sel = cmds.ls( sl = 1 )
			attrList = []
			attrListTemp = []
			attrListTemp2 = []
			if sel:
				for ctrl in sel:
					attrList = cmds.listAttr( ctrl , k = True , se = 1 , u = 1 )
					userDefinedList = cmds.listAttr( ctrl , k = True , se = 1 , ud = 1, u = 1 )

					##get defaults for user defined attributes
					if rp.attrExists( ctrl , "defaults" ):
						defaultString = cmds.getAttr( ctrl + ".defaults" )
						defaultDict = eval( defaultString )
						for attr in defaultDict:
							if not cmds.getAttr( "%s.%s" % ( ctrl , attr ) , lock = True ):
								cmds.setAttr( "%s.%s" % ( ctrl , attr ), defaultDict[attr] )
					
					##exclude connected and user defined attributes
					attrListTemp = deepcopy( attrList )
					if not attrListTemp:
						continue
					for a in attrListTemp:
							connected = cmds.listConnections( "%s.%s" % ( ctrl, a ) , s = 1 , d = 0 )
							if connected:
								if cmds.nodeType( connected ) == "animCurveTL" or cmds.nodeType( connected ) == "animCurveTA" or cmds.nodeType( connected ) == "animCurveTU" :
									pass
								else:
									attrList.remove( a )
			
					attrListTemp2 = deepcopy( attrList )
					if userDefinedList and attrListTemp2:
						for u in userDefinedList:
							if u in attrListTemp2:
								attrList.remove( u )
					
					##set translation , rotation and scale attributes if available to their default values
					if not attrList:
						continue
					for i in attrList:
						if not cmds.getAttr( "%s.%s" % ( ctrl , i ) , lock = True ):
							if i == "scaleX" or i == "scaleY" or i == "scaleZ":
								cmds.setAttr( "%s.%s" % ( ctrl , i ) , 1 )
							else:
								cmds.setAttr( "%s.%s" % ( ctrl , i ) , 0 )

		finally:
			cmds.undoInfo( closeChunk = True )
					

	## PROP TAB
	############
	##refreshes the entire props tab
	def refreshPropsTab( self, debug = 0 ):
		self.refreshAttachmentsPointsList_fn( debug = debug )
		self.fillPropsList_fn( debug = debug )
		
	def refreshAttachmentsPointsList_fn( self, debug = 0 ):
		self.attachmentPointCMB.clear()
		atts = None
		if self.currentCharacter:
			atts = self.getConnections( str( self.currentCharacter ) + '.attachments', direction = 's' )
			if debug: print self.currentCharacter, atts
		if atts:
			for att in atts:
				self.attachmentPointCMB.addItem( att )
	
	def fillPropsList_fn( self, debug = 0 ):
		if not self.propsList:
			self.propCMB.clear()
			self.propsList = cag.listFiles_in_Folder( self.propsFolder, '.ma' )
			
			if self.propsList:
				for prop in self.propsList:
					self.propCMB.addItem( prop.replace( self.propsFolder, '' ) )
			else:
				cmds.warning( 'No props files found! Please sync %s' % self.propsFolder )
				
	def refreshPropsList_fn( self, debug = 0 ):
		self.propsList = None
		self.fillPropsList_fn( debug = debug )
	
	def syncProps_fn( self, debug = 0 ):
		from P4 import P4, P4Exception
		
		if debug: 'print getting props from p4'
		p4 = P4()
		try:
			p4.connect()
		except:
			print 'Cannot connect!'
			return False
		
		p4Path = str( self.propPathLINE.text() )
		
		try:
			p4.run_sync( p4Path )
		except P4Exception as e:
			if 'up-to-date' in e: print 'Props library up to date with P4.'
		p4.disconnect()
		self.refreshPropsList_fn( debug = debug )
		return True
		
#	##loads props from P4, refreshes tab
#	def loadPropsFn( self, debug = 0 ):
#		if not self.sync: 
#			if self.getPropsP4(): print 'Updated props from P4'
#			else: print 'Failed to get props from P4'
#		self.refreshPropsTab()	
#	##gets props from p4 (and syncs), returns True on sync, False on failure
#	def getPropsP4( self, debug = 0 ):
#		from P4 import P4, P4Exception
#		
#		if debug: 'print getting props from p4'
#		p4 = P4()
#		try:
#			p4.connect()
#		except:
#			print 'Cannot connect!'
#			return False
#		
#		p4Path = str( self.propPathLINE.text() )
#		
#		up2date = False
#		if cmds.objExists( 'cryPropLib' ): cmds.delete( 'cryPropLib' )
#		try:
#			p4.run_sync( p4Path )
#		except P4Exception as e:
#			if 'up-to-date' in e: print 'Props library up to date with P4.'
#			up2date = True
#		newFile = p4.run( 'fstat', p4Path )[0]['clientFile']
#		self.propsList = self.importPropLib( newFile )
#		self.sync = newFile
#		p4.disconnect()
#		return True
		
	##attaches props to attachment
	def attachPropFn( self ):
		filePath = self.propsFolder + str( self.propCMB.currentText() )
		
		importedProps = cag.importMayaScene_returnNodes( filePath, nameSpace = 'prop', nodeTypes = ['transform'] )
		
		if self.currentCharacter and importedProps:
			cmds.setAttr ( '%s.overrideEnabled' % importedProps[0], 1 )
			cmds.setAttr ( '%s.overrideDisplayType' % importedProps[0], 2 )
			attachment = str( self.attachmentPointCMB.currentText() )
			cag.attachProp_to_character( importedProps[0], str( self.currentCharacter ), attachment )
	
	def quickAttachPropFn( self, props = [], attachments = [] ):
		numProps = len( props )
		tokens = str( self.attachmentPointCMB.currentText() ).split( ':' )
		cryPrefix = '%s:%s:' % ( tokens[0], tokens[1] )
		for i in range( 0, numProps ):
			filePath = self.propsFolder + props[i] + '.ma'
			
			importedProps = cag.importMayaScene_returnNodes( filePath, nameSpace = 'prop', nodeTypes = ['transform'] )
			
			if self.currentCharacter and importedProps:
				cmds.setAttr ( '%s.overrideEnabled' % importedProps[0], 1 )
				cmds.setAttr ( '%s.overrideDisplayType' % importedProps[0], 2 )
				attachment = cryPrefix + attachments[i]
				cag.attachProp_to_character( importedProps[0], str( self.currentCharacter ), attachment )
	
	def quickAttach_ba_fn( self ):
		props = ['barb_1hnd_axe', 'barb_shield']
		attachments = ['R_Weapon', 'L_Weapon']
		self.quickAttachPropFn( props = props, attachments = attachments )
	def quickAttach_bd_fn( self ):
		props = ['barb_1hnd_sword', 'barb_1hnd_sword']
		attachments = ['R_Weapon', 'L_Weapon']
		self.quickAttachPropFn( props = props, attachments = attachments )
	def quickAttach_bs_fn( self ):
		props = ['barb_1hnd_sword', 'barb_shield']
		attachments = ['R_Weapon', 'L_Weapon']
		self.quickAttachPropFn( props = props, attachments = attachments )
	def quickAttach_rs_fn( self ):
		props = ['romn_marius_sword', 'romn_marius_shld']
		attachments = ['R_Weapon', 'L_Weapon']
		self.quickAttachPropFn( props = props, attachments = attachments )

	## Simulation TAB
	############
	def solvers_tree_fn( self ):
		self.solvers_tree.clear()
		character = self.getSelectedChar()			
		if character:
			if rp.attrExists(character,'solvers'):
				solvers= self.getConnections( character + ".solvers" , "d" )
				if solvers:
					for solv in solvers:
						wid1 = QtGui.QTreeWidgetItem()
						wid1.setText( 0, solv)
						font = wid1.font( 0 )
						font.setPointSize( 11 )
						wid1.setFont( 0, font )
						self.solvers_tree.addTopLevelItem( wid1)
				else:
					wid1 = QtGui.QTreeWidgetItem()
					wid1.setText( 0, "There are no solvers for this character")
					font = wid1.font( 0 )
					font.setPointSize( 11 )
					wid1.setFont( 0, font )
					self.solvers_tree.addTopLevelItem( wid1)
			else:
				wid1 = QtGui.QTreeWidgetItem()
				wid1.setText( 0, "There is no solvers attribute on your charcater Node")
				font = wid1.font( 0 )
				font.setPointSize( 11 )
				wid1.setFont( 0, font )
				self.solvers_tree.addTopLevelItem( wid1)
				
	def getSelectedSolver( self ):
		solvers = self.solvers_tree.selectedItems()
		solversList = []
		for sol in solvers:
			solversList.append(str(sol.text( 0 )))
		return solversList
	
	def selectSolvers_fn(self):
		solver = self.getSelectedSolver()
		selected = []
		if not solver:
			return False
		else:
			cmds.select(clear = True)
			for sel in solver:
				cmds.select(sel , add = 1)
	
	def setSolverStartFrameToTimeSlider_fn(self):
		solvers = self.getSelectedSolver()
		if solvers:
			startFrame = cmds.playbackOptions(q = 1 , minTime = 1)
			for sol in solvers:
				shape = cmds.listRelatives(sol, shapes = 1)[0]
				cmds.setAttr(shape+".startFrame" , startFrame)
		
	def setSolverStartFrameToTimeSlider_fn(self):
		solvers = self.getSelectedSolver()
		if solvers:
			startFrame = cmds.playbackOptions(q = 1 , minTime = 1)
			for sol in solvers:
				if cmds.nodeType(sol) == "nucleus":
					print "nucleus"
					cmds.setAttr(sol+".startFrame" , startFrame)
				else:
					shape = cmds.listRelatives(sol , shapes = 1)[0]
					cmds.setAttr(shape+".startFrame" , startFrame)
	def set_fn(self):
		solvers = self.getSelectedSolver()
		if solvers:
			startFrame = self.setSolverStartFrameTo_SB.value()
			for sol in solvers:
				if cmds.nodeType(sol) == "nucleus":
					print "nucleus"
					cmds.setAttr(sol+".startFrame" , startFrame)
				else:
					shape = cmds.listRelatives(sol, shapes = 1)[0]
					cmds.setAttr(shape+".startFrame" , startFrame)
		
def show():
	global UiWindow
	try:
		UiWindow.close()
	except:pass
	UiWindow = Window()
	UiWindow.show()
	return UiWindow
