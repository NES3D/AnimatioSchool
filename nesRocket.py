import maya.cmds as cmds
import math
import sys

class Rocket(object):

    def __init__(self, bodyParts = 1, noseConeHeight = 1, fuelTanks = 1, rocketRadius = 1):

        self.bodyParts = bodyParts
        self.noseConeHeight = noseConeHeight
        self.fuelTanks = fuelTanks
        self.rocketRadius = rocketRadius
        
    def generateModel(self):

        # Очистка сцены
        cmds.select(all=True)
        cmds.delete()
    
        self.create_body()
        self.create_nose()
        self.create_fuel_tanks()
        self.group_rocket()
        
    # Создание тела ракеты
    def create_body(self):

        rocket_body_parts = []

        if self.bodyParts and self.rocketRadius >= 1:
            bodyParts_int = int(round(self.bodyParts))
            for i in range(bodyParts_int):
                rocket_body = cmds.polyCylinder(name = "Body", r = self.rocketRadius)
                self.rocket_body_node = rocket_body[1]
                self.rocket_body_name = rocket_body[0]
                self.bodyPart_BB = cmds.xform(self.rocket_body_name, q=1, bb=1, ws=1) # Xmin Ymin Zmin Xmax Ymax Zmax
                cmds.xform(ws=True, t=[0, (((self.bodyPart_BB[4] - self.bodyPart_BB[1]))*i), 0])
                rocket_body_parts.append(self.rocket_body_name)
            
            self.body_group = cmds.group(rocket_body_parts, name="Body_GRP")
            self.body_group_BB = cmds.xform(self.body_group, q=True, bb=True, ws=True)

        else:
            cmds.confirmDialog(title='Information', message='bodyParts and rocketRadius must be >= 1', button=['OK'], defaultButton='OK')
            sys.exit()

    #Создаём носовыю часть    
    def create_nose(self):

        if self.noseConeHeight > 0:

            rocket_nose = cmds.polyCone(name = "Nose", radius = 0.1 + self.body_group_BB[3], height = self.noseConeHeight)
            rocket_nose_BB = cmds.xform(rocket_nose, q=True, bb=True, ws=True) # Xmin Ymin Zmin Xmax Ymax Zmax
            cmds.xform(ws=True, t=[0, (self.body_group_BB[4]+rocket_nose_BB[4]), 0])
            self.nose_group = cmds.group(rocket_nose, name="Nose_GRP")

        else:
            cmds.confirmDialog(title='Information', message='noseConeHeight must be > 0', button=['OK'], defaultButton='OK')
            cmds.select(all=True)
            cmds.delete()
            sys.exit()

    def create_fuel_tanks(self):
      
        # Создание конусов для баков
        cones = []
        if self.fuelTanks >= 2:
            fuelTanks_int = int(round(self.fuelTanks))
            for i in range(fuelTanks_int):
                angle = (2 * math.pi / fuelTanks_int) * i  # Рассчитываем угол для текущего конуса
                x = self.body_group_BB[0] * math.cos(angle)  # Рассчитываем координату X
                z = self.body_group_BB[0] * math.sin(angle)  # Рассчитываем координату Z
                rocket_fuel_tanks = cmds.polyCone(name="Fuel_Tank", radius = self.body_group_BB[3] - 1, height = self.body_group_BB[3] - 0.2)[0]  # Создаем конус
                rocket_tanks_BB = cmds.xform(rocket_fuel_tanks, q=True, bb=True, ws=True) # Xmin Ymin Zmin Xmax Ymax Zmax
                cmds.xform(rocket_fuel_tanks, t=[x, (self.body_group_BB[1]+rocket_tanks_BB[1]), z])  # Перемещаем конус в рассчитанную позицию
                cones.append(rocket_fuel_tanks)

            # Группировка конусов
            self.tanks_group = cmds.group(cones, name="Tanks_GRP")

        else:
            cmds.confirmDialog(title='Information', message='fuelTanks must be >= 2', button=['OK'], defaultButton='OK')
            cmds.select(all=True)
            cmds.delete()
            sys.exit()

    # Группируем и устанавливаем в ноль всю коснтркуцию ракеты
    def group_rocket(self):
        self.rocket_group = cmds.group(self.body_group, self.nose_group, self.tanks_group, name="Rocket_GRP")
        self.rocket_BB = cmds.xform(self.rocket_group, q=1, bb=1, ws=1) # Xmin Ymin Zmin Xmax Ymax Zmax
        cmds.xform(ws=True, t=[0, (self.rocket_BB[1]*(-1)), 0])
        cmds.makeIdentity(apply=True) # reset transform

   

myRocket = Rocket (bodyParts = 5, noseConeHeight = 3, fuelTanks = 6, rocketRadius = 1)
myRocket.generateModel() # только при вызове этой функции должна быть создана модель ракеты