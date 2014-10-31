__author__ = 'Crytek'


import maya.cmds as cmds



def createPoseReader(name="cryPoseReader"):


	if (name == ""):
		name = "cryPoseReader"
	sl = cmds.ls(sl=1)
	try:
		incr = 0
		while cmds.objExists(str(name)):
			name = "cryPoseReader" + str(incr)
			incr += 1
		node = cmds.createNode("cryPoseReader", n=name)
		transform = cmds.listRelatives(node, p=1)[0]
		transform = cmds.rename(transform, name + "_transform")

		cmds.undoInfo(openChunk=True)
		i = 0
		for s in sl:


			parent = cmds.listRelatives(s, p=1)

			poseLoc = cmds.spaceLocator(n=name + "_" + s + "_pose_loc")[0]

			cmds.setAttr(poseLoc + ".visibility", 0)
			cmds.delete(cmds.pointConstraint(s, poseLoc))
			cmds.delete(cmds.orientConstraint(s, poseLoc))

			if parent:
				cmds.parentConstraint(parent, poseLoc, mo=1)



			separatorAttr = s
			cmds.addAttr(transform, ln=separatorAttr, at="enum", en="-------------:0")
			cmds.setAttr(transform + "." + separatorAttr, k=1, cb=1)
			cmds.setAttr(transform + "." + separatorAttr, l=1)


			cmds.connectAttr(poseLoc + ".worldMatrix", node + ".poseReaderMatrix[" + str(i) + "]")
			cmds.connectAttr(s + ".worldMatrix", node + ".inputMatrix[" + str(i) + "]")
			cmds.connectAttr(s + ".parentMatrix", node + ".inputParentMatrix[" + str(i) + "]")
			cmds.connectAttr(s + ".rotatePivot", node + ".inputRotatePivot[" + str(i) + "]")

			volumeAttr = "volumeRadius" + str(i)
			cmds.addAttr(transform, ln=volumeAttr, at="float")
			cmds.setAttr(transform + "." + volumeAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + volumeAttr, node + ".volumeRadius[" + str(i) + "]")

			inputWeightAttr = "inputWeight" + str(i)
			cmds.addAttr(transform, ln=inputWeightAttr, at="float")
			cmds.setAttr(transform + "." + inputWeightAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + inputWeightAttr, node + ".inputWeight[" + str(i) + "]")


			minAngleAttr = "minAngle" + str(i)
			cmds.addAttr(transform, ln=minAngleAttr, at="float")
			cmds.setAttr(transform + "." + minAngleAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + minAngleAttr, node + ".minAngle[" + str(i) + "]")

			maxAngleAttr = "maxAngle" + str(i)
			cmds.addAttr(transform, ln=maxAngleAttr, at="float")
			cmds.setAttr(transform + "." + maxAngleAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + maxAngleAttr, node + ".maxAngle[" + str(i) + "]")

			minTwistAngleAttr = "minTwistAngle" + str(i)
			cmds.addAttr(transform, ln=minTwistAngleAttr, at="float")
			cmds.setAttr(transform + "." + minTwistAngleAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + minTwistAngleAttr, node + ".minTwistAngle[" + str(i) + "]")

			maxTwistAngleAttr = "maxTwistAngle" + str(i)
			cmds.addAttr(transform, ln=maxTwistAngleAttr, at="float")
			cmds.setAttr(transform + "." + maxTwistAngleAttr, k=1, cb=1)
			cmds.connectAttr( transform + "." + maxTwistAngleAttr, node + ".maxTwistAngle[" + str(i) + "]")


			cmds.setAttr(transform + "." + volumeAttr, 1.0)
			cmds.setAttr(transform + "." + inputWeightAttr, 1.0)

			cmds.setAttr(transform + "." + minAngleAttr, 0.0)
			cmds.setAttr(transform + "."  + maxAngleAttr, 90.0)
			cmds.setAttr(transform + "." + minTwistAngleAttr, 0.0)
			cmds.setAttr(transform + "." + maxTwistAngleAttr, 90.0)


			i +=1
	finally:
		cmds.undoInfo(closeChunk=True)
		return node

