import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore

class MyWindow(QtWidgets.QDialog):

    def __init__(self):

        super(MyWindow, self).__init__()

        self.setup_UI()

    def setup_UI(self):

        # Создём окно
        self.setWindowTitle("Create Poly Objects")
        self.setMinimumSize(500,200)
        self.setMaximumSize(700,300)
        self.resize(700,300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Инициализация переменной для хранения имени объекта
        self.poly_object = None

        # Создаём основной Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        # self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.main_layout)

        # Создаем QLineEdit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText("Enter object name")

        # Добавляем QLineEdit в главный Layout
        self.main_layout.addWidget(self.line_edit)

        self.create_radio_buttons()
        self.create_slider()
        self.create_buttons()

    def create_radio_buttons(self):
        # Создаём Layout для радиокнопок 01
        self.radio_buttons_layout_01 = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.radio_buttons_layout_01)
        # Создаём радиокнопки
        self.rbutton_Sphere = QtWidgets.QRadioButton("Sphere")
        self.rbutton_Sphere.setChecked(True)
        self.rbutton_Cube = QtWidgets.QRadioButton("Cube")
        self.rbutton_Cone = QtWidgets.QRadioButton("Cone")
        # Добавляем радикноки в Layout
        self.radio_buttons_layout_01.addWidget(self.rbutton_Sphere)
        self.radio_buttons_layout_01.addWidget(self.rbutton_Cube)
        self.radio_buttons_layout_01.addWidget(self.rbutton_Cone)

        # Создаём Layout для радиокнопок 02
        self.radio_buttons_layout_02 = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.radio_buttons_layout_02)
        # Создаём радиокнопки
        self.rbutton_Cylinder = QtWidgets.QRadioButton("Cylinder")
        self.rbutton_Torus = QtWidgets.QRadioButton("Torus")
        self.rbutton_Plane = QtWidgets.QRadioButton("Plane")
        # Добавляем радикноки в Layout
        self.radio_buttons_layout_02.addWidget(self.rbutton_Cylinder)
        self.radio_buttons_layout_02.addWidget(self.rbutton_Torus)
        self.radio_buttons_layout_02.addWidget(self.rbutton_Plane)

    def create_slider(self):
        # Создаём Layout для слайдера
        self.slider_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.slider_layout)
        # Создаем слайдер
        self.slider_label = QtWidgets.QLabel("Translate X: ")
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_line_edit)

        # Создаем QLineEdit для отображения значения слайдера
        self.line_edit_slider_value = QtWidgets.QLineEdit()
        self.line_edit_slider_value.setFixedWidth(80)
        self.line_edit_slider_value.setAlignment(QtCore.Qt.AlignHCenter)
        self.line_edit_slider_value.setReadOnly(False)
        self.line_edit_slider_value.setText("%d" % self.slider.value())
        self.line_edit_slider_value.editingFinished.connect(self.update_slider_from_line_edit)

        # Добавляем слайдер в layout
        self.slider_layout.addWidget(self.slider_label)
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.line_edit_slider_value)

    def create_buttons(self):
        # Создаём Layout для кнопок
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)
        # Создаём кнопки
        self.button_Create = QtWidgets.QPushButton("Create")
        self.button_Create.clicked.connect(self.on_button_create_clicked)

        self.button_Apply = QtWidgets.QPushButton("Apply")
        self.button_Apply.clicked.connect(self.on_button_apply_clicked)

        self.button_Cancel = QtWidgets.QPushButton("Cancel")
        self.button_Cancel.clicked.connect(self.close)

        # Добавялем кнопки в Layout
        self.buttons_layout.addWidget(self.button_Create)
        self.buttons_layout.addWidget(self.button_Apply)
        self.buttons_layout.addWidget(self.button_Cancel)

    # Создание связи слайдера с текстовым окном
    def update_line_edit(self, value):
        self.line_edit_slider_value.setText("%d" % value)

    # Создание обтраной связи текстового окна со слайдером
    def update_slider_from_line_edit(self):
        try:
            value = int(self.line_edit_slider_value.text())
            if 0 <= value <= 10:
                self.slider.setValue(value)
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid Value", "Please enter a value between 0 and 10.")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Invalid Value", "Please enter a valid integer.")

    def on_button_create_clicked(self):
        self.on_button_apply_clicked()
        self.close()

    def on_button_apply_clicked(self):

        object_name = self.line_edit.text()  # Получаем текст из QLineEdit
        if not object_name:
            object_name = None  # Если имя пустое, Maya создаст объект с именем по умолчанию
        elif object_name.isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid Name", "The object name cannot be only digits.") # Запрет на ввод чисел
            return

        if self.rbutton_Sphere.isChecked():
            self.poly_object = cmds.polySphere(name=object_name)[0]
        elif self.rbutton_Cube.isChecked():
            self.poly_object = cmds.polyCube(name=object_name)[0]
        elif self.rbutton_Cone.isChecked():
            self.poly_object = cmds.polyCone(name=object_name)[0]
        elif self.rbutton_Cylinder.isChecked():
            self.poly_object = cmds.polyCylinder(name=object_name)[0]
        elif self.rbutton_Torus.isChecked():
            self.poly_object = cmds.polyTorus(name=object_name)[0]
        elif self.rbutton_Plane.isChecked():
            self.poly_object = cmds.polyPlane(name=object_name)[0]

        # Установим начальное положение объекта по оси X в соответствии со значением слайдера
        cmds.setAttr("{}.translateX".format(self.poly_object), self.slider.value())

        
if cmds.window("MyTestUI", query=True, exists=True):
    cmds.deleteUI("MyTestUI")

if cmds.windowPref("MyTestUI", exists=True):
    cmds.windowPref("MyTestUI", remove=1)

a = MyWindow()
a.show()