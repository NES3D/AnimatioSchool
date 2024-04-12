import maya.cmds as cmds
sph = cmds.polySphere(r=1, name="MySphere")[0]
minTime = cmds.playbackOptions(query=1, minTime=True)
maxTime = cmds.playbackOptions(query=1, maxTime=True)
cmds.currentTime(minTime, edit=True)
cmds.setKeyframe(sph + ".translateX", time=minTime, value=-10)
cmds.setKeyframe(sph + ".translateX", time=maxTime, value=10)

cube = cmds.polyCube(name="MyCube")[0]
cmds.move(-10,0,10)
cmds.parentConstraint(sph, cube, maintainOffset=True)
cmds.bakeResults(cube + ".translateX", simulation=True, time=(minTime,maxTime))
cmds.delete(cube, constraints=True)
