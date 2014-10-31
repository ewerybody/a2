'''
Requires a selected object in the middle.
Load objects that relate to the middle object in the appropriate direction using the UI.
there are no arguments required.
Use the navigate mode to navigate through the objects after creating the relations in the create mode.

Example:
>>> import CryAnimation.pickWalkAuthor as pw
>>> pw.show()

User can use the AddPickWalk method to add the message nodes manually
Example :

import maya.cmds as cmds
from CryAnimation.pickWalkAuthor
CryAnimation.pickWalkAuthor.AddPickWalk("locator1 ", up = "locator2" ,down =  "locator3" , left = None , right = None)

# Created by: Riham Toulan
# Creation date: 2012/02/03
'''


import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import sys
import os
import sip
import maya.OpenMayaUI as mui

def getMayaWindow():
	
	#'Get the maya main window as a QMainWindow instance'	
	ptr = mui.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QtCore.QObject)
	
    	
## Get the absolute path to my ui file
uiFile = (os.path.dirname(str(__file__)) + '/pickWalkUI.ui').replace('/','\\')
form_class, base_class = uic.loadUiType(uiFile)

class Window(base_class, form_class):	
	def __init__(self, parent= getMayaWindow()):
		super(base_class, self).__init__(parent)
		self.setupUi(self)
		self.connect(self.createRadioBTN, QtCore.SIGNAL("clicked()"), self.SetPickWalkMode)		
		self.connect(self.navigateRadioBTN ,QtCore.SIGNAL("clicked()"), self.SetPickWalkMode)
		self.connect(self.medPushBTN, QtCore.SIGNAL("clicked()"), self.addSelectedObjectToMiddle)
		self.buttonUpCall = lambda who="upPushBTN": self.makePickWalkButtonClicked(who)
		self.buttonDownCall = lambda who="downPushBTN": self.makePickWalkButtonClicked(who)
		self.buttonLeftCall = lambda who="leftPushBTN": self.makePickWalkButtonClicked(who)
		self.buttonRightCall = lambda who="rightPushBTN": self.makePickWalkButtonClicked(who)						
		self.connect(self.upPushBTN, QtCore.SIGNAL("clicked()"), self.buttonUpCall)
		self.connect(self.downPushBTN, QtCore.SIGNAL("clicked()"), self.buttonDownCall)
		self.connect(self.leftPushBTN, QtCore.SIGNAL("clicked()"), self.buttonLeftCall)
		self.connect(self.rightPushBTN, QtCore.SIGNAL("clicked()"), self.buttonRightCall)
											   
	##checks and makes sure that the direction is valid		
	def returnValidDir (self,dir) :
		if (dir == "u") or (dir == "n") or (dir == "up") or (dir == "north") :
			return "up"
		
		if (dir == "l") or (dir == "w") or (dir == "left") or (dir == "west") :
			return "left"

		if (dir == "r") or (dir == "e") or (dir == "right") or (dir == "east") :
			return "right"
		
		else :
			return ""
			
	def SetPickWalkMode(self):		
		global pickWalkMode				
		if(self.createRadioBTN.isChecked()):
			pickWalkMode = "create"
			return 1
			
		elif (self.navigateRadioBTN.isChecked()):
			pickWalkMode = "navigate"
			return 0
			

	def resetPickWalkButtons(self):
		self.upPushBTN.setText("blank")
		self.medPushBTN.setText("nothing selected")
		self.downPushBTN.setText("blank")
		self.leftPushBTN.setText("blank")
		self.rightPushBTN.setText("blank")
	
	def addSelectedObjectToMiddle(self):
		sel = [0]
		sel = cmds.ls( sl = True)
		if (len(sel) > 1):
			cmds.warning("you can't load more than one object per time")
			cmds.error("you can't load more than one object per time")
		self.medPushBTN.setText(sel[0])
		self.updatePickWalkWin()
				
	def updatePickWalkWin(self):
		medObj = str(self.medPushBTN.text())
		if not (cmds.objExists (medObj)):
			self.resetPickWalkButtons()
			
		elif cmds.objExists(medObj):	
			up = self.returnConnectedObj(medObj,"up")
			down = self.returnConnectedObj(medObj,"down")
			left = self.returnConnectedObj(medObj,"left")
			right = self.returnConnectedObj(medObj,"right")				
		##now replace them if they're true
			self.upPushBTN.setText(up)
			self.downPushBTN.setText(down)
			self.leftPushBTN.setText(left)
			self.rightPushBTN.setText(right)
			
			
	## get the button based on the dir			
	def makePickWalkButtonClicked (self ,buttonSelected = ""):
		dir = ""
		attr = ""
		if (buttonSelected == "upPushBTN"):
			dir = "up"
			attr = "pickWalk_up"
			
		if (buttonSelected == "downPushBTN"):
			dir = "down"
			attr = "pickWalk_down"
			
		if (buttonSelected == "leftPushBTN"):
			dir = "left"
			attr = "pickWalk_left"
			
		if (buttonSelected == "rightPushBTN"):
			dir = "right"
			attr = "pickWalk_right"
			
		medObj = str(self.medPushBTN.text())
		
		if (cmds.objExists(medObj)):
			##when we are in the creation mode
			if (self.SetPickWalkMode()):
				##check if there's something selected.if not, clear that direction
				sel = [0]
				sel = cmds.ls( sl = True)
				if not sel :
					labelUpBTN = str(self.upPushBTN.text())
					labelDownBTN = str(self.downPushBTN.text())
					labelLeftBTN = str(self.leftPushBTN.text())
					labelRightBTN = str(self.rightPushBTN.text())
					labels = [labelUpBTN , labelDownBTN , labelLeftBTN , labelRightBTN]
					for label in labels:
						if (label != "blank"):
							result = cmds.confirmDialog (m = (("You have nothing selected.\nDo you want to clear the %s direction for %s ?")%(dir,medObj)), b =["Yes","No"], cancelButton = "No")
							if (result == "Yes"):
								con = cmds.listConnections (medObj + "." + attr)
								cmds.disconnectAttr ((con[0] + ".message"),(medObj+ "." + attr))
						self.updatePickWalkWin()			
							
				##if there's something selected, let's make the connection
				else :
					checkAttr = cmds.attributeQuery(attr, n = medObj ,ex = True)
					if not checkAttr :	
						cmds.addAttr (medObj , ln = attr , at = "message")
					##make sure they're not the same object first, urrgghhhhhhh 
					if (medObj == sel[0]):					
						cmds.confirmDialog (m = "You're trying to make an object pickWalk to itself.. it can't do that!\n")
						cmds.error ("You're trying to make an object pickWalk to itself.. it can't do that!\n")
					##make the connection finally	
					else :
						cmds.connectAttr ((sel[0] + ".message"),(medObj + "." + attr), f = True)
						
			##we are in Navigation mode				
			else:
				self.GoPickWalk(dir)
				self.addSelectedObjectToMiddle()	
			self.updatePickWalkWin()
		
	##given an object and a direction, this proc returns the name of the connected object.		
	def returnConnectedObj (self , obj ,dir):
		if cmds.attributeQuery (("pickWalk_"+dir) , exists = True , node = obj) :
			con = [0]
			con = cmds.listConnections (obj + ".pickWalk_" + dir)
			return con[0]
		return ""
		
	##now get a list of selected objects	
	def GoPickWalk(self , dir):
		print "Go Pick walk"
		obj= [0]
		obj =cmds.ls (sl = True)
		connected = self.returnConnectedObj(obj[0],dir)
		print connected
		cmds.select(connected)
		
def AddPickWalk( node , up = None, down = None , left = None , right = None):
	
	if up:
		dir = "up"
		attr = "pickWalk_up"
		checkAttr = cmds.attributeQuery(attr, n = node ,ex = True)
		if not checkAttr :	
			cmds.addAttr (node, ln = attr , at = "message")
			if (node == up):					
				cmds.confirmDialog (m = "You're trying to make an object pickWalk to itself.. it can't do that!\n")
			else:
				cmds.connectAttr ((up + ".message"),(node+ "." + attr), f = True)		
	if down:
		dir = "down"
		attr = "pickWalk_down"			
		checkAttr = cmds.attributeQuery(attr, n = node ,ex = True)
		if not checkAttr :	
			cmds.addAttr (node, ln = attr , at = "message")
			if (node == down):					
				cmds.confirmDialog (m = "You're trying to make an object pickWalk to itself.. it can't do that!\n")
			else:
				cmds.connectAttr ((down + ".message"),(node + "." + attr), f = True)					
		
	if left:
		dir = "left"
		attr = "pickWalk_left"
		checkAttr = cmds.attributeQuery(attr, n = node ,ex = True)
		if not checkAttr:
			cmds.addAttr (node, ln = attr , at = "message")
			if (node == left):					
				cmds.confirmDialog (m = "You're trying to make an object pickWalk to itself.. it can't do that!\n")
			else:
				cmds.connectAttr ((left + ".message"),(node+ "." + attr), f = True)		
	if right:
		dir = "right"
		attr = "pickWalk_right"
		checkAttr = cmds.attributeQuery(attr, n = node ,ex = True)
		if not checkAttr:
			cmds.addAttr (node, ln = attr , at = "message")
			if (node == right):
				cmds.confirmDialog (m = "You're trying to make an object pickWalk to itself.. it can't do that!\n")
			else:
				cmds.connectAttr ((right + ".message"),(node + "." + attr), f = True)
							
def show():
	window = Window()
	window.show()
	return window