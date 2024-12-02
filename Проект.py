import sys
import sqlite3
import io
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, QStyledItemDelegate
from glawok import Ui_MainWindow
from password import Ui_Form
from wibrab import Ui_Form1
from gpolz import Ui_Form2
from pokup import Ui_Form3
from uwtow import Ui_Form4
from dobtow import Ui_Form5


imagePath = 'Стул.jpg'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pol_button.clicked.connect(self.mover)
        self.rab_button.clicked.connect(self.mover2)

    def mover(self):
        valid = QMessageBox.question(
            self, 'Вход', "Действительно зайти как пользователь?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if valid == QMessageBox.StandardButton.Yes:
            self.wp = MyWidget()
            self.wp.show()
            self.close()

    def mover2(self):
        valid = QMessageBox.question(
            self, 'Вход', "Действительно зайти как работник?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if valid == QMessageBox.StandardButton.Yes:
            self.wp = MyWidget1()
            self.wp.show()
            self.close()


class MyWidget1(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn.clicked.connect(self.mover)
        self.vp.clicked.connect(self.mover2)
        self.w = MyWidget4()

    def mover(self):
        self.close()

    def mover2(self):
        if self.le.text() == '12345':
            self.w.show()
            self.close()

        else:
            self.lbl.setText('Неверный пароль')


class MyWidget(QWidget, Ui_Form2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.con = sqlite3.connect('Proekt.sql')
        self.cur = self.con.cursor()
        cur = self.con.cursor()
        sql = """SELECT * FROM type"""
        result = cur.execute(sql).fetchall()
        self.programs = {}

        for e in result:
            self.programs[e[0]] = e[1]

        self.d = {}
        self.picture = QLabel()

        for key, value in self.programs.items():
            self.d[value] = key

        self.buttonsave.clicked.connect(self.save)
        self.parameterSelection.addItems(self.programs.values())
        self.queryButton.clicked.connect(self.search)

    def initUI(self):
        self.btn.clicked.connect(self.mover)
        self.lable = QLabel(self)
        self.lable.setText("Данный товар отсутствует")
        self.lable.resize(200, 30)
        self.lable.move(10, 10)
        self.lable.hide()
        self.w3 = MyWidget3()

    def mover(self):
        self.close()

    def search(self):
        type_id = self.d[self.parameterSelection.currentText()]
        try:
            self.lable.hide()
            cur = self.con.cursor()
            sql = """SELECT predmet.id, predmet.name, type.name, predmet.year, quality.quality, predmet.kolvo, predmet.izo 
            FROM predmet
            JOIN type ON type.id = predmet.type
            JOIN quality ON quality.id = predmet.quality
            WHERE type.id = ?"""
            result = cur.execute(sql, (type_id,)).fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(7)
            self.titles = ["id товара", "имя товара", "тип товара", "год выпуска", "качество", "кол-во", "изображение товара"]
            self.tableWidget.setHorizontalHeaderLabels(self.titles)

            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(elem[1])))
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[2])))
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(elem[3])))
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(elem[4])))
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(elem[5])))
            for i, elem in enumerate(result):
                self.picture.setPixmap(QPixmap(elem[6] + '.jpg'))
                self.tableWidget.setCellWidget(i, 6, self.picture)

            self.modified = {}
        except Exception as e:
            self.lable.show()

    def save(self):
        self.w3.show()


class MyWidget3(QWidget, Ui_Form3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.btn.clicked.connect(self.mover)
        self.op.clicked.connect(self.save)
        self.pushButton.clicked.connect(self.summ)
        self.itlabel = QLabel(self)
        self.itlabel.resize(300, 30)
        self.itlabel.move(10, 245)
        self.itlabel.hide()
        self.con = sqlite3.connect('Proekt.sql')
        self.cur = self.con.cursor()

    def mover(self):
        self.close()

    def save(self):
        a = self.le2.text()
        if len(a) != 16 or a == int(a):
            self.itlabel.setText('Неправильные данные карты')
        else:
            cur = self.con.cursor()
            sql = (f"SELECT * FROM predmet")
            result = cur.execute(sql).fetchall()
            a = self.le1.text()
            b = self.le.text()

            if int(b) <= len(result):
                if int(result[int(b) - 1][5]) >= int(a):
                    print(result[int(b) - 1][5], a)
                    self.itlabel.setText('Покупка совершена!')
                    up = (f"UPDATE predmet SET kolvo = ? WHERE id = ?")
                    cur.execute(up, (result[int(b) - 1][5] - int(a), b))
                    self.con.commit()
                else:
                    self.itlabel.setText('Большое или неправильное кол-во товара')
            else:
                self.itlabel.setText('Неправильный id товара')

        self.itlabel.show()

    def summ(self):
        self.itlabel.show()

        try:
            self.itlabel.setText('Итого: ' + str(int(self.le1.text()) * 1000) + 'р')
        except Exception as e:
            self.itlabel.setText('Неправильное кол-во товара')


class MyWidget4(QWidget, Ui_Form1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.mover)
        self.pushButton2.clicked.connect(self.mover2)
        self.w1 = MyWidget5()
        self.w2 = MyWidget6()

    def mover(self):
        self.w2.show()
        self.close()

    def mover2(self):
        self.w1.show()
        self.close()


class MyWidget5(QWidget, Ui_Form4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.mover)
        self.it = QLabel(self)
        self.it.resize(300, 30)
        self.it.move(15, 255)
        self.it.hide()
        self.con = sqlite3.connect('Proekt.sql')
        self.cur = self.con.cursor()
        cur = self.con.cursor()
        sql = (f"SELECT * FROM predmet")
        self.result = cur.execute(sql).fetchall()

    def mover(self):
        a = self.le.text()
        b = self.le1.text()

        if int(a) <= len(self.result):
            cur = self.con.cursor()
            up = (f"UPDATE predmet SET kolvo = ? WHERE id = ?")
            cur.execute(up, (self.result[int(a) - 1][5] + int(b), a))
            self.it.setText('Товар успешно добавлен')
            self.con.commit()
        else:
            self.it.setText('Товар с таким id не найден')

        self.it.show()


class MyWidget6(QWidget, Ui_Form5):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.mover)
        self.it = QLabel(self)
        self.it.resize(300, 30)
        self.it.move(15, 255)
        self.it.hide()
        self.con = sqlite3.connect('Proekt.sql')
        self.cur = self.con.cursor()
        cur = self.con.cursor()
        sql = (f"SELECT * FROM predmet")
        self.result = cur.execute(sql).fetchall()

    def mover(self):
        a = self.le.text()
        b = self.le1.text()
        c = self.le2.text()
        d = self.le3.text()
        e = self.le4.text()
        f = self.le5.text()

        try:
            if int(b) // 2 == int(c) // 2 == int(d) // 2 == int(e) // 2:
                pass
            cur = self.con.cursor()
            ins = (f"INSERT INTO predmet(name, type, year, quality, kolvo, izo) VALUES(?, ?, ?, ?, ?, ?)")
            cur.execute(ins, (a, b, c, d, e, f))
            self.it.setText('Товар успешно добавлен')
            self.con.commit()
        except ValueError:
            self.it.setText('Введите корректные данные')

        self.it.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())