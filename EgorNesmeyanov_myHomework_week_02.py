import maya.cmds as cmds
import random

def clearScene():
    allSpheres = cmds.ls(type = "mesh")
    allSpheres = cmds.listRelatives(allSpheres, parent=1)
    cmds.delete(allSpheres)

clearScene()

def createPlanet(planetRadiusMin, planetRadiusMax, planetName, moonsMin, moonsMax, moonRadiusMin, moonRadiusMax):

    planetRadius = random.randint (planetRadiusMin, planetRadiusMax)

    moons = random.randint (moonsMin, moonsMax)

    moonRadius = random.uniform (moonRadiusMin, moonRadiusMax)

    cmds.polySphere(name = planetName, r = planetRadius)
    
    minTime = cmds.playbackOptions(query=1, minTime=True)
    
    maxTime = cmds.playbackOptions(query=1, maxTime=True)
    
    cmds.currentTime(minTime, edit=True)
    
    cmds.setKeyframe(planetName + ".rotateY", time=minTime, value=0)
    
    cmds.setKeyframe(planetName + ".rotateY", time=maxTime, value=360)

    cmds.keyTangent(inTangentType = "linear", outTangentType = "linear")
 
    for i in range (moons):

        moonRadius = random.uniform (moonRadiusMin, moonRadiusMax)
        
        s = cmds.polySphere(r = moonRadius)[0]

        r = cmds.polySphere(s, query=1, r=1)

        if i == 0:

            distance = planetRadius + moonRadius * 1.5
                   
        else:

            distance = distance + r
               
        cmds.xform(s, translation = [distance, 0, 0])
        
        cmds.xform(ws = 1, a = 1, rp = [0, 0, 0])
        
        rotateZ = random.randint (-45, 20)
        
        rotateY = random.randint (0, 360)
     
        cmds.xform(rotation = [0, rotateY, rotateZ])
                
        cmds.parent(s, planetName)

        # Animate Moons

        cmds.setKeyframe(s + ".rotateY", time=minTime, value= rotateY)
    
        cmds.setKeyframe(s + ".rotateY", time=maxTime, value= rotateY + 3240)

        cmds.keyTangent(inTangentType = "linear", outTangentType = "linear")

        distance = distance + r
                
createPlanet(planetName = "Earth", planetRadiusMin = 3, planetRadiusMax = 6, moonsMin = 2, moonsMax = 7, moonRadiusMin = 0.4, moonRadiusMax = 2.0)