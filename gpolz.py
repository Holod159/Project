# Form implementation generated from reading ui file 'C:\Tools\a\Git\Project\gpolz.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(516, 392)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parameterSelection = QtWidgets.QComboBox(parent=Form)
        self.parameterSelection.setObjectName("parameterSelection")
        self.verticalLayout.addWidget(self.parameterSelection)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.queryButton = QtWidgets.QPushButton(parent=Form)
        self.queryButton.setObjectName("queryButton")
        self.horizontalLayout.addWidget(self.queryButton)
        self.buttonsave = QtWidgets.QPushButton(parent=Form)
        self.buttonsave.setObjectName("buttonsave")
        self.horizontalLayout.addWidget(self.buttonsave)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn = QtWidgets.QPushButton(parent=Form)
        self.btn.setObjectName("btn")
        self.verticalLayout.addWidget(self.btn)
        self.tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.queryButton.setText(_translate("Form", "Поиск"))
        self.buttonsave.setText(_translate("Form", "Заказать"))
        self.btn.setText(_translate("Form", "Выход"))
