import maya.cmds as cmds

# Close Window Function
def closeWindow():    
    if cmds.window("MyWindow", exists=1):
        cmds.deleteUI("MyWindow")
        
    if cmds.windowPref("MyWindow", exists=1):
        cmds.windowPref("MyWindow", remove=1)

closeWindow()

# Создаем окно
cmds.window("MyWindow", title="Polygon Primitives")

# Создаём основной лэйаут
main_layout = cmds.columnLayout(adjustableColumn=True)

cmds.text(parent=main_layout, label=' ', height=20) #offset

# Дочерний лэйаут для текстового поля
child_layout = cmds.columnLayout(parent=main_layout, adjustableColumn=True, columnAttach=('both', 10))

cmds.text(parent=main_layout, label=' ', height=10) #offset

# Создаем поле для имени объета
myTextField = cmds.textField("ID01", parent=child_layout, placeholderText="Object Name")

# Лэйаут для радиокнопок
obj_type_layout = cmds.columnLayout(parent=main_layout, adjustableColumn=True, columnAttach=('both', 10))

# Создаем группу радиокнопок с тремя опциями: Sphere, Cube, Cone

radio_grp = cmds.radioButtonGrp(parent=obj_type_layout, labelArray3=['Sphere', 'Cube', 'Cone'], numberOfRadioButtons=3, select=1)

cmds.text(parent=obj_type_layout, label=' ', height=10) #offset

# создаем лэйаут для чекбоксов
options_layout = cmds.rowLayout(parent=main_layout, numberOfColumns=2, cw2=(150,150), columnAttach2=("left", "right"))

obj_options_layout_01  = cmds.columnLayout(parent=options_layout, columnOffset=("left", 10))

check01 = cmds.checkBox(parent=obj_options_layout_01, label='Put into a group', height = 25)
check02 = cmds.checkBox(parent=obj_options_layout_01, label='Move X by 10 units', height = 25)
check03 = cmds.checkBox(parent=obj_options_layout_01, label='Display Layer/Template', height = 25)

obj_options_layout_02  = cmds.columnLayout(parent=options_layout)

check04 = cmds.checkBox(parent=obj_options_layout_02, label='Harden Edge', height = 25)
check05 = cmds.checkBox(parent=obj_options_layout_02, label='Soften Edge', height = 25)
check06 = cmds.checkBox(parent=obj_options_layout_02, label='Create UVs', height = 25, value=True)

# Создаем лэйаут для слайдера
slider_layout = cmds.columnLayout(parent = main_layout, columnOffset=("both", 10))

cmds.text(parent=slider_layout, label=' ', height=10) #offset

# Создаем слайдер и текстовое поле для отображения значения слайдера
slider = cmds.floatSliderGrp(parent = slider_layout, label='Scale:', field=True, columnAlign=(1, "left"), minValue=1, maxValue=10, value=1, changeCommand="update_scale_x")

cmds.text(parent=slider_layout, label=' ', height=20) #offset

# Получаем значение выбранной радиокнопки, чекбоксов и слайдера
def createObj():
    def objType():
        selected_index = cmds.radioButtonGrp(radio_grp, query=True, select=True)
        if selected_index == 1:
            print("Creating a sphere")
            n = cmds.textField("ID01", query=1, text = True)
            obj = cmds.polySphere(name=n)[0]
        elif selected_index == 2:
            print("Creating a cube")
            n = cmds.textField("ID01", query=1, text = True)
            obj = cmds.polyCube(name=n)[0]
        elif selected_index == 3:
            print("Creating a cone")
            n = cmds.textField("ID01", query=1, text = True)
            obj = cmds.polyCone(name=n)[0]
        return obj
    
    def obj_options():
        obj = objType()
    
        create_grp = cmds.checkBox(check01, q=1, value=True)
        move_obj = cmds.checkBox(check02, q=1, value=True)
        display_layer = cmds.checkBox(check03, q=1, value=True)
        harden_edge = cmds.checkBox(check04, q=1, value=True)
        soften_edge = cmds.checkBox(check05, q=1, value=True)
        delete_uvs = cmds.checkBox(check06, q=1, value=True)

        if create_grp == True:
            cmds.group(obj, name = obj + "_GRP")
        if move_obj == True:
            cmds.move(10, 0, 0, obj)
        if display_layer == True:
            cmds.createDisplayLayer(name="Obj_Layer")
        if harden_edge == True:
            cmds.polySoftEdge(a=0)
        if soften_edge == True:
            cmds.polySoftEdge(a=180)
        if soften_edge and harden_edge == True:
            cmds.polySoftEdge(a=30)
        if delete_uvs == False:
            cmds.polyMapDel(obj)
        
        def query_slider_value():
            slider_value = cmds.floatSliderGrp(slider, query=True, value=True)
            cmds.setAttr(obj + '.scaleX', slider_value)
            cmds.setAttr(obj + '.scaleY', slider_value)
            cmds.setAttr(obj + '.scaleZ', slider_value)

        query_slider_value()
            
    obj_options()

#создание formLayout для кнопок
button_layout = cmds.formLayout(parent=main_layout, h=30, numberOfDivisions=100)

button01 = cmds.button("MyBtn01ID", label="Create", parent=button_layout, command = "createObj()", statusBarMessage = "Create Object")
button02 = cmds.button("MyBtn02ID", label="Cancel", parent=button_layout, command = "closeWindow()", statusBarMessage = "Close Window")

cmds.formLayout(button_layout, e=1, attachPosition = [ (button01, 'left', 4, 0), (button01, 'right', 2, 50), (button02, 'left', 2, 50), (button02, 'right', 4, 100) ])

cmds.showWindow("MyWindow")