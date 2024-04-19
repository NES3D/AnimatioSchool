import maya.cmds as cmds
import random

# Очистка сцены от старой геометрии
def clearScene():
    allSpheres = cmds.ls(type = "mesh")
    allSpheres = cmds.listRelatives(allSpheres, parent=1)
    cmds.delete(allSpheres)

clearScene()

# Функция создания планеты
def createPlanet(planetRadiusMin, planetRadiusMax, planetName, moonsMin, moonsMax, moonRadiusMin, moonRadiusMax):

    # Установка минимальных и максимальных значений для параметров функции
    planetRadius = random.randint (planetRadiusMin, planetRadiusMax)

    moons = random.randint (moonsMin, moonsMax)

    moonRadius = random.uniform (moonRadiusMin, moonRadiusMax)

    # Создание главной планеты
    cmds.polySphere(name = planetName, r = planetRadius)
    
    # Определение первого и последнего кадра на таймлайне
    minTime = cmds.playbackOptions(query=1, minTime=True)
    
    maxTime = cmds.playbackOptions(query=1, maxTime=True)
    
    # Установка текущего значения времени в минильное положение
    cmds.currentTime(minTime, edit=True)
    
    # Анимация вращения главной планеты
    cmds.setKeyframe(planetName + ".rotateY", time=minTime, value=0)
    
    cmds.setKeyframe(planetName + ".rotateY", time=maxTime, value=360)

    # Установка типа анимации Linear
    cmds.keyTangent(inTangentType = "linear", outTangentType = "linear")
    
    # Цикл по созданию лун
    for i in range (moons):

        # Установка минимальных и максимальных значений радиусов лун
        moonRadius = random.uniform (moonRadiusMin, moonRadiusMax)
        
        # Создание Луны
        s = cmds.polySphere(r = moonRadius)[0]

        r = cmds.polySphere(s, query=1, r=1)

        # Установка дистанции для первой луны
        if i == 0:

            distance = planetRadius + moonRadius * 1.5

        # Установка дистанции для всех последующих лун           
        else:

            distance = distance + r
       
        cmds.xform(s, translation = [distance, 0, 0])

        # Создание оффсет групп для лун
        moonGRP = cmds.group(s)
        
        # Установка пивота для оффсетгрупп в мировое начало координат
        cmds.xform(moonGRP, ws = 1, a = 1, rp = [0, 0, 0])
        
        # Расстановка лун вокруг главной Планеты
        rotateZ = random.randint (-45, 45)
        
        rotateY = random.randint (0, 360)
     
        cmds.xform(moonGRP, rotation = [0, rotateY, rotateZ])

        # Парент лун и их оффсет групп к главной Планете        
        cmds.parent(moonGRP, planetName)

        # Анимация лун

        cmds.setKeyframe(moonGRP + ".rotateY", time=minTime, value= rotateY)
    
        cmds.setKeyframe(moonGRP + ".rotateY", time=maxTime, value= rotateY + 3240)

        cmds.keyTangent(inTangentType = "linear", outTangentType = "linear")

        distance = distance + r
                
createPlanet(planetName = "Earth", planetRadiusMin = 3, planetRadiusMax = 6, moonsMin = 2, moonsMax = 7, moonRadiusMin = 0.4, moonRadiusMax = 2.0)