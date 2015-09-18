# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picomotor_form.ui'
#
# Created: Tue Mar 26 11:27:53 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(539, 189)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Picomotor", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(QtGui.QApplication.translate("Dialog", "Motor 1 (Horisontal)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Left_m1_pushButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Left_m1_pushButton.sizePolicy().hasHeightForWidth())
        self.Left_m1_pushButton.setSizePolicy(sizePolicy)
        self.Left_m1_pushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/left.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Left_m1_pushButton.setIcon(icon)
        self.Left_m1_pushButton.setObjectName(_fromUtf8("Left_m1_pushButton"))
        self.horizontalLayout_2.addWidget(self.Left_m1_pushButton)
        self.Pos_m1_SpinBox = QtGui.QDoubleSpinBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Pos_m1_SpinBox.sizePolicy().hasHeightForWidth())
        self.Pos_m1_SpinBox.setSizePolicy(sizePolicy)
        self.Pos_m1_SpinBox.setMinimumSize(QtCore.QSize(120, 0))
        self.Pos_m1_SpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Pos_m1_SpinBox.setFont(font)
        self.Pos_m1_SpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " steps", None, QtGui.QApplication.UnicodeUTF8))
        self.Pos_m1_SpinBox.setDecimals(0)
        self.Pos_m1_SpinBox.setMinimum(-200000.0)
        self.Pos_m1_SpinBox.setMaximum(200000.0)
        self.Pos_m1_SpinBox.setObjectName(_fromUtf8("Pos_m1_SpinBox"))
        self.horizontalLayout_2.addWidget(self.Pos_m1_SpinBox)
        self.Right_m1_pushButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Right_m1_pushButton.sizePolicy().hasHeightForWidth())
        self.Right_m1_pushButton.setSizePolicy(sizePolicy)
        self.Right_m1_pushButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/right.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/right.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/right.png")), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/right.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.Right_m1_pushButton.setIcon(icon1)
        self.Right_m1_pushButton.setObjectName(_fromUtf8("Right_m1_pushButton"))
        self.horizontalLayout_2.addWidget(self.Right_m1_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Step:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.Step_m1_SpinBox = QtGui.QDoubleSpinBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Step_m1_SpinBox.sizePolicy().hasHeightForWidth())
        self.Step_m1_SpinBox.setSizePolicy(sizePolicy)
        self.Step_m1_SpinBox.setMinimumSize(QtCore.QSize(90, 0))
        self.Step_m1_SpinBox.setMaximumSize(QtCore.QSize(70, 16777215))
        self.Step_m1_SpinBox.setBaseSize(QtCore.QSize(70, 0))
        self.Step_m1_SpinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Step_m1_SpinBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Step_m1_SpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " step", None, QtGui.QApplication.UnicodeUTF8))
        self.Step_m1_SpinBox.setDecimals(0)
        self.Step_m1_SpinBox.setMaximum(10000.0)
        self.Step_m1_SpinBox.setSingleStep(1.0)
        self.Step_m1_SpinBox.setProperty("value", 1.0)
        self.Step_m1_SpinBox.setObjectName(_fromUtf8("Step_m1_SpinBox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.Step_m1_SpinBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.line_3 = QtGui.QFrame(Dialog)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Motor 2 (Vertical)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.Left_m2_pushButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Left_m2_pushButton.sizePolicy().hasHeightForWidth())
        self.Left_m2_pushButton.setSizePolicy(sizePolicy)
        self.Left_m2_pushButton.setText(_fromUtf8(""))
        self.Left_m2_pushButton.setIcon(icon)
        self.Left_m2_pushButton.setObjectName(_fromUtf8("Left_m2_pushButton"))
        self.horizontalLayout_3.addWidget(self.Left_m2_pushButton)
        self.Pos_m2_SpinBox = QtGui.QDoubleSpinBox(Dialog)
        self.Pos_m2_SpinBox.setMinimumSize(QtCore.QSize(120, 0))
        self.Pos_m2_SpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Pos_m2_SpinBox.setFont(font)
        self.Pos_m2_SpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " steps", None, QtGui.QApplication.UnicodeUTF8))
        self.Pos_m2_SpinBox.setDecimals(0)
        self.Pos_m2_SpinBox.setMinimum(-200000.0)
        self.Pos_m2_SpinBox.setMaximum(200000.0)
        self.Pos_m2_SpinBox.setObjectName(_fromUtf8("Pos_m2_SpinBox"))
        self.horizontalLayout_3.addWidget(self.Pos_m2_SpinBox)
        self.Right_m2_pushButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Right_m2_pushButton.sizePolicy().hasHeightForWidth())
        self.Right_m2_pushButton.setSizePolicy(sizePolicy)
        self.Right_m2_pushButton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/right.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Right_m2_pushButton.setIcon(icon2)
        self.Right_m2_pushButton.setObjectName(_fromUtf8("Right_m2_pushButton"))
        self.horizontalLayout_3.addWidget(self.Right_m2_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Step:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.Step_m2_SpinBox = QtGui.QDoubleSpinBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Step_m2_SpinBox.sizePolicy().hasHeightForWidth())
        self.Step_m2_SpinBox.setSizePolicy(sizePolicy)
        self.Step_m2_SpinBox.setMinimumSize(QtCore.QSize(90, 0))
        self.Step_m2_SpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " step", None, QtGui.QApplication.UnicodeUTF8))
        self.Step_m2_SpinBox.setDecimals(0)
        self.Step_m2_SpinBox.setMaximum(10000.0)
        self.Step_m2_SpinBox.setSingleStep(1.0)
        self.Step_m2_SpinBox.setProperty("value", 1.0)
        self.Step_m2_SpinBox.setObjectName(_fromUtf8("Step_m2_SpinBox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.Step_m2_SpinBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout_3.setItem(1, QtGui.QFormLayout.FieldRole, spacerItem)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setVerticalSpacing(6)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.manual_Command_lineEdit = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_Command_lineEdit.sizePolicy().hasHeightForWidth())
        self.manual_Command_lineEdit.setSizePolicy(sizePolicy)
        self.manual_Command_lineEdit.setMinimumSize(QtCore.QSize(100, 23))
        self.manual_Command_lineEdit.setMaximumSize(QtCore.QSize(115, 16777215))
        self.manual_Command_lineEdit.setObjectName(_fromUtf8("manual_Command_lineEdit"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.manual_Command_lineEdit)
        self.verticalLayout_2.addLayout(self.formLayout_4)
        self.line_4 = QtGui.QFrame(Dialog)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout_2.addWidget(self.line_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.reset_pushButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_pushButton.sizePolicy().hasHeightForWidth())
        self.reset_pushButton.setSizePolicy(sizePolicy)
        self.reset_pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.reset_pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.reset_pushButton.setText(QtGui.QApplication.translate("Dialog", "Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_pushButton.setObjectName(_fromUtf8("reset_pushButton"))
        self.horizontalLayout_5.addWidget(self.reset_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.line_5 = QtGui.QFrame(Dialog)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.verticalLayout_2.addWidget(self.line_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.radioButtonSteps = QtGui.QRadioButton(Dialog)
        self.radioButtonSteps.setText(QtGui.QApplication.translate("Dialog", "steps", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonSteps.setChecked(True)
        self.radioButtonSteps.setObjectName(_fromUtf8("radioButtonSteps"))
        self.horizontalLayout_4.addWidget(self.radioButtonSteps)
        self.radioButtonMm = QtGui.QRadioButton(Dialog)
        self.radioButtonMm.setText(QtGui.QApplication.translate("Dialog", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonMm.setChecked(False)
        self.radioButtonMm.setObjectName(_fromUtf8("radioButtonMm"))
        self.horizontalLayout_4.addWidget(self.radioButtonMm)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.speedSpinBox = QtGui.QDoubleSpinBox(Dialog)
        self.speedSpinBox.setSuffix(QtGui.QApplication.translate("Dialog", " steps/s", None, QtGui.QApplication.UnicodeUTF8))
        self.speedSpinBox.setDecimals(0)
        self.speedSpinBox.setMaximum(2000.0)
        self.speedSpinBox.setProperty("value", 250.0)
        self.speedSpinBox.setObjectName(_fromUtf8("speedSpinBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.speedSpinBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.Left_m1_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.m1_step_left)
        QtCore.QObject.connect(self.Right_m1_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.m1_step_right)
        QtCore.QObject.connect(self.Left_m2_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.m2_step_left)
        QtCore.QObject.connect(self.Right_m2_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.m2_step_right)
        QtCore.QObject.connect(self.Pos_m1_SpinBox, QtCore.SIGNAL(_fromUtf8("editingFinished()")), Dialog.m1_move)
        QtCore.QObject.connect(self.Pos_m2_SpinBox, QtCore.SIGNAL(_fromUtf8("editingFinished()")), Dialog.m2_move)
        QtCore.QObject.connect(self.Step_m1_SpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.m1_changeStep)
        QtCore.QObject.connect(self.Step_m2_SpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.m2_changeStep)
        QtCore.QObject.connect(self.manual_Command_lineEdit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), Dialog.manual_Command)
        QtCore.QObject.connect(self.reset_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reset_positions)
        QtCore.QObject.connect(self.radioButtonSteps, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.selectUnit)
        QtCore.QObject.connect(self.radioButtonMm, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.selectUnit)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.stopMotors)
        QtCore.QObject.connect(self.speedSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Dialog.speedChanged)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

import pico_images_rc
