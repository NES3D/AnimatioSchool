import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

class SelectWidget(QtWidgets.QWidget):
    def __init__(self, set_name):
        super(SelectWidget, self).__init__()

        self.set_name = set_name
        
        self.popMenu = None

        self.setup_ui()

    def setup_ui(self):

        self.setMinimumSize(250, 50)
        self.setMaximumHeight(50)

        self.setAutoFillBackground(True)

        self.set_background()

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QtWidgets.QLabel(self.set_name)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

    def set_background(self, r=50, g=50, b=50):
        # set background
        self.p = QtGui.QPalette()
        self.color = QtGui.QColor(r,g,b)
        self.p.setColor(self.backgroundRole(), self.color) 
        self.setPalette(self.p)

    '''
        # Стиль для закругленных углов виджета
        self.setStyleSheet(f"""
            background-color: rgb({r}, {g}, {b});
            border-radius: 15px;
        """)
        '''

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.set_background(75,75,75)

    def leaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.set_background()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # Выделение объектов в selection set
            cmds.select(self.set_name)
            self.set_background(r=95, g=95, b=95)

        elif event.buttons() == QtCore.Qt.RightButton:
            self.set_background(r=95, g=95, b=95)

            self.create_contex_menu()
            self.popMenu.exec_(self.mapToGlobal(event.pos()))

    def mouseReleaseEvent(self, event):
        self.set_background(75,75,75)

    def create_contex_menu(self):

        self.popMenu = QtWidgets.QMenu(self)

        self.popMenuRename = QtWidgets.QAction('Rename set', self)
        self.popMenu.addAction(self.popMenuRename)
        self.popMenuRename.triggered.connect(self.rename_widget)

        self.popMenuAdd = QtWidgets.QAction('Add object', self)
        self.popMenu.addAction(self.popMenuAdd)
        self.popMenuAdd.triggered.connect(self.addObj)

        self.popMenuDel = QtWidgets.QAction('Delete object', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.delObj)

        self.popMenuDel = QtWidgets.QAction('Select All', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.selectAll)

        self.popMenuDel = QtWidgets.QAction('Delete Set', self)
        self.popMenu.addAction(self.popMenuDel)
        self.popMenuDel.triggered.connect(self.deleteSet)
    
    # Функция пекреименования сета
    def rename_widget(self):
        new_name, ok = QtWidgets.QInputDialog.getText(self, 'Rename set', 'Enter new name:')
        if ok and new_name:
            old_set_name = self.set_name
            self.set_name = new_name
            self.label.setText(new_name)
            cmds.rename(old_set_name, new_name)
    
    def addObj(self):
        cmds.sets(add = self.set_name)

    def delObj(self):
        cmds.sets(remove = self.set_name)

    def selectAll(self):
        cmds.select(self.set_name)

    def deleteSet(self):
        cmds.delete(self.set_name)
        self.deleteLater()
 

class MyCustomWidget(QtWidgets.QDialog):
    def __init__(self):
        super(MyCustomWidget, self).__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Selection Sets")
        self.setObjectName("MyCustomWidgetUIId")
        self.setMinimumSize(450, 700)
        self.resize(450,700)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(5,5,5,5)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)

        # Создаем область прокрутки
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.main_layout.addWidget(self.scroll_area)

        # Создаем контейнер для виджетов внутри области прокрутки
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        # Создаем компоновочный блок для виджетов внутри контейнера
        self.widgets_layout = QtWidgets.QVBoxLayout(self.scroll_widget)

        # Добавляем Stretch к компоновочному блоку виджетов, чтобы виджеты добавлялись сверху
        self.widgets_layout.addStretch(1)
                
        self.create_set_btn = QtWidgets.QPushButton("Create Selection Set")
        self.create_set_btn.setMinimumSize(250, 50)
        self.create_set_btn.setMaximumHeight(50)
        self.create_set_btn.clicked.connect(self.on_button_create_set_clicked)
        self.create_set_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.create_set_btn)

        #Создаём горизонтальный layout для кнопок_01
        self.btn_hor_layout_01 = QtWidgets.QHBoxLayout()
        self.btn_hor_layout_01.setContentsMargins(0,0,0,0)
        self.btn_hor_layout_01.setSpacing(3)
        self.main_layout.addLayout(self.btn_hor_layout_01)

        #Создаём горизонтальный layout для кнопок_02
        self.btn_hor_layout_02 = QtWidgets.QHBoxLayout()
        self.btn_hor_layout_02.setContentsMargins(0,0,0,0)
        self.btn_hor_layout_02.setSpacing(3)
        self.main_layout.addLayout(self.btn_hor_layout_02)

        self.select_all_btn = QtWidgets.QPushButton("Select All")
        self.select_all_btn.setMinimumHeight(50)
        self.select_all_btn.setMaximumHeight(50)
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_all_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_hor_layout_01.addWidget(self.select_all_btn)
        
        self.select_all_geo_btn = QtWidgets.QPushButton("Select All Geo")
        self.select_all_geo_btn.setMinimumHeight(50)
        self.select_all_geo_btn.setMaximumHeight(50)
        self.select_all_geo_btn.clicked.connect(self.select_all_geo)
        self.select_all_geo_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_hor_layout_01.addWidget(self.select_all_geo_btn)

        self.select_all_curves_btn = QtWidgets.QPushButton("Select All Curves")
        self.select_all_curves_btn.setMinimumHeight(50)
        self.select_all_curves_btn.setMaximumHeight(50)
        self.select_all_curves_btn.clicked.connect(self.select_all_curves)
        self.select_all_curves_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_hor_layout_02.addWidget(self.select_all_curves_btn)

        self.select_all_joints_btn = QtWidgets.QPushButton("Select All Joints")
        self.select_all_joints_btn.setMinimumHeight(50)
        self.select_all_joints_btn.setMaximumHeight(50)
        self.select_all_joints_btn.clicked.connect(self.select_all_joints)
        self.select_all_joints_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_hor_layout_02.addWidget(self.select_all_joints_btn)

        self.delete_all_sets_btn = QtWidgets.QPushButton("Delete All Sets")
        self.delete_all_sets_btn.setMinimumSize(250, 50)
        self.delete_all_sets_btn.setMaximumHeight(50)
        self.delete_all_sets_btn.clicked.connect(self.delete_all_sets)
        self.delete_all_sets_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.delete_all_sets_btn)

    def on_button_create_set_clicked(self):
        self.set_name = cmds.sets(name="Selection Set #")
        self.selection_widget = SelectWidget(self.set_name)
        self.widgets_layout.insertWidget(self.widgets_layout.count() - 1, self.selection_widget)

    def select_all(self):
        # Выделение всех полигональных объектов в сцене
        cmds.select(cmds.ls())

    def select_all_geo(self):
        # Выделение всех полигональных объектов в сцене
        cmds.select(cmds.ls(type='mesh'))

    def select_all_curves(self):
        cmds.select(cmds.ls(type='nurbsCurve'))

    def select_all_joints(self):
        cmds.select(cmds.ls(type='joint'))

    def delete_all_sets(self):
         # Удаление всех виджетов и selection sets
        children = self.scroll_widget.findChildren(QtWidgets.QWidget)
        for child in children:
            if isinstance(child, SelectWidget):
                cmds.delete(child.set_name)
                child.deleteLater()

def main():

    if cmds.window("MyCustomWidgetUIId", exists=1):
         cmds.deleteUI("MyCustomWidgetUIId")

    if cmds.windowPref("MyCustomWidgetUIId", exists=1):
         cmds.windowPref("MyCustomWidgetUIId", remove=1)

    global myUI
    myUI = MyCustomWidget()
    myUI.show()

if __name__ == "__main__":
    main()