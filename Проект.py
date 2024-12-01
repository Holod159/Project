import sys
import sqlite3
import io
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem

desing = """"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Мебель')

        self.pol_button = QPushButton('Я пользователь', self)
        self.pol_button.resize(150, 80)
        self.pol_button.move(100, 40)
        self.pol_button.clicked.connect(self.mover)

        self.rab_button = QPushButton('Я работник', self)
        self.rab_button.resize(150, 80)
        self.rab_button.move(100, 150)
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


class MyWidget1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Мебель-П')
        self.lbl = QLabel(self)
        self.lbl.setText('Введите пароль:')
        self.lbl.resize(200, 30)
        self.lbl.move(100, 100)
        self.btn = QPushButton('Выход', self)
        self.btn.move(200, 200)
        self.btn.clicked.connect(self.mover)
        self.vp = QPushButton('Вход', self)
        self.vp.move(100, 200)
        self.vp.clicked.connect(self.mover2)
        self.le = QLineEdit(self)
        self.le.resize(100, 30)
        self.le.move(100, 150)
        self.w = MyWidget4()

    def mover(self):
        self.close()

    def mover2(self):
        if self.le.text() == '12345':
            self.w.show()
            self.close()
        else:
            self.lbl.setText('Неверный пароль')


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.programs = {1: 'Стул', 2: 'Стол', 3: 'Диван', 4: 'Шкаф', 5: 'Вешалка', 6: 'Тумбочка'}
        self.kash = {1: 'Плачевное', 2: 'Плохое', 3: 'Среднее', 4: 'Нормальное', 5: 'Отличное'}
        self.d = {}
        for key, value in self.programs.items():
            self.d[value] = key
        self.parameterSelection = QComboBox(self)
        self.queryButton = QPushButton('Поиск', self)
        self.queryButton.resize(100, 30)
        self.queryButton.move(100, 100)
        self.buttonsave = QPushButton('Заказать', self)
        self.buttonsave.resize(100, 30)
        self.buttonsave.move(250, 100)
        self.buttonsave.clicked.connect(self.save)
        self.parameterSelection.resize(100, 30)
        self.parameterSelection.move(100, 50)
        self.parameterSelection.addItems(self.programs.values())
        self.queryButton.clicked.connect(self.search)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(700, 300)
        self.tableWidget.move(100, 200)
        self.con = sqlite3.connect('Proekt.sql')
        self.cur = self.con.cursor()

    def initUI(self):
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Мебель-П')
        self.lbl = QLabel(self)
        self.lbl.move(100, 100)
        self.btn = QPushButton('Выход', self)
        self.btn.move(100, 150)
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
            print(result)
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
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(elem[6])))
            self.modified = {}
        except Exception as e:
            self.lable.show()

    def save(self):
        self.w3.show()


class MyWidget3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Покупка')
        self.label = QLabel(self)
        self.label.setText('Введите id нужного товара')
        self.label.resize(200, 30)
        self.label.move(10, 10)
        self.btn = QPushButton('Выход', self)
        self.btn.move(240, 200)
        self.btn.resize(100, 50)
        self.btn.clicked.connect(self.mover)
        self.le = QLineEdit(self)
        self.le.resize(100, 30)
        self.le.move(15, 50)
        self.label1 = QLabel(self)
        self.label1.setText('Введите количество товара')
        self.label1.resize(200, 30)
        self.label1.move(170, 10)
        self.le1 = QLineEdit(self)
        self.le1.resize(100, 30)
        self.le1.move(170, 50)
        self.label2 = QLabel(self)
        self.label2.setText('Введите номер карты(только 16 цифр, без тире)')
        self.label2.resize(300, 30)
        self.label2.move(15, 100)
        self.op = QPushButton('Заказать', self)
        self.op.move(120, 200)
        self.op.resize(100, 50)
        self.le2 = QLineEdit(self)
        self.le2.resize(200, 30)
        self.le2.move(60, 150)
        self.pushButton = QPushButton('Узнать сумму', self)
        self.pushButton.move(10, 200)
        self.pushButton.resize(100, 50)
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


class MyWidget4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Мебель-П')
        self.l = QLabel(self)
        self.l.resize(300, 30)
        self.l.move(15, 10)
        self.l.setText('Выберете действие:')
        self.pushButton = QPushButton('Добавить новый товар', self)
        self.pushButton.resize(300, 100)
        self.pushButton.move(20, 60)
        self.pushButton.clicked.connect(self.mover)
        self.pushButton2 = QPushButton('Увеличить кол-во товара', self)
        self.pushButton2.resize(300, 100)
        self.pushButton2.move(20, 180)
        self.pushButton2.clicked.connect(self.mover2)
        self.w1 = MyWidget5()
        self.w2 = MyWidget6()

    def mover(self):
        self.w2.show()
        self.close()

    def mover2(self):
        self.w1.show()
        self.close()


class MyWidget5(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Мебель-П')
        self.l = QLabel(self)
        self.l.resize(300, 30)
        self.l.move(15, 10)
        self.l.setText('Введите id товара:')
        self.le = QLineEdit(self)
        self.le.resize(100, 30)
        self.le.move(15, 50)
        self.l1 = QLabel(self)
        self.l1.resize(300, 30)
        self.l1.move(15, 100)
        self.l1.setText('Введите кол-во товара:')
        self.le1 = QLineEdit(self)
        self.le1.resize(100, 30)
        self.le1.move(15, 140)
        self.pushButton = QPushButton('Добавить', self)
        self.pushButton.resize(300, 80)
        self.pushButton.move(15, 180)
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


class MyWidget6(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('Мебель-П')
        self.l = QLabel(self)
        self.l.resize(300, 30)
        self.l.move(15, 10)
        self.l.setText('Введите имя товара:')
        self.le = QLineEdit(self)
        self.le.resize(100, 30)
        self.le.move(15, 50)
        self.l1 = QLabel(self)
        self.l1.resize(300, 30)
        self.l1.move(15, 100)
        self.l1.setText('Введите тип товара:')
        self.le1 = QLineEdit(self)
        self.le1.resize(100, 30)
        self.le1.move(15, 140)
        self.l2 = QLabel(self)
        self.l2.resize(300, 30)
        self.l2.move(15, 180)
        self.l2.setText('Введите год выпуска:')
        self.le2 = QLineEdit(self)
        self.le2.resize(100, 30)
        self.le2.move(15, 210)
        self.l3 = QLabel(self)
        self.l3.resize(300, 30)
        self.l3.move(150, 10)
        self.l3.setText('Введите качество:')
        self.le3 = QLineEdit(self)
        self.le3.resize(100, 30)
        self.le3.move(150, 50)
        self.l4 = QLabel(self)
        self.l4.resize(300, 30)
        self.l4.move(150, 100)
        self.l4.setText('Введите количество:')
        self.le4 = QLineEdit(self)
        self.le4.resize(100, 30)
        self.le4.move(150, 140)
        self.l5 = QLabel(self)
        self.l5.resize(300, 30)
        self.l5.move(150, 180)
        self.l5.setText('Введите название изображения:')
        self.le5 = QLineEdit(self)
        self.le5.resize(100, 30)
        self.le5.move(150, 210)
        self.pushButton = QPushButton('Добавить', self)
        self.pushButton.resize(300, 80)
        self.pushButton.move(15, 290)
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
        if type(b) == int and type(c) == int and type(d) == int and type(e) == int:
            cur = self.con.cursor()
            ins = (f"INSERT INTO predmet(name, type, year, quality, kolvo, izo) VALUES(?, ?, ?, ?, ?, ?)")
            cur.execute(ins, (a, b, c, d, e, f))
            self.it.setText('Товар успешно добавлен')
            self.con.commit()
        else:
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