import sys
import sqlite3

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.load_table()

    def load_table(self):
        self.tableWidget.clear()
        cur = self.con.cursor()
        result = cur.execute("""
          SELECT * FROM coffee
          ORDER BY id
        """, ).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())