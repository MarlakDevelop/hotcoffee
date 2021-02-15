import sys
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from release.main_ui import Ui_MainWindow as MainUI
from release.add_edit_coffee_form_ui import Ui_MainWindow as AddEditCoffeeFormUI


class MainWindow(QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('../data/coffee.sqlite')
        self.load_table()
        self.tableWidget.cellDoubleClicked.connect(self.open_film)
        self.pushButton.clicked.connect(self.create_film)

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

    def open_film(self, row, column):
        pk = int(self.tableWidget.item(row, 0).text())
        coffee_form = EditCoffeeForm(self)
        coffee_form.pk = pk
        coffee_form.load_coffee()
        coffee_form.show()

    def create_film(self):
        coffee_form = AddCoffeeForm(self)
        coffee_form.show()


class AddCoffeeForm(QMainWindow, AddEditCoffeeFormUI):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.setupUi(self)
        self.root = root
        self.pushButton.clicked.connect(self.create_coffee)

    def create_coffee(self):
        try:
            cur = self.root.con.cursor()
            cur.execute(f"""
                        INSERT INTO coffee(sort_name, roasting, type, taste, price, volume)
                        VALUES(
                            "{self.lineEdit.text().strip()}",
                            "{self.spinBox.value()}",
                            "{self.lineEdit_2.text().strip()}",
                            "{self.textEdit.toPlainText()}",
                            "{self.spinBox_2.value()}",
                            "{self.spinBox_3.value()}"
                        )""")
            self.root.con.commit()
            self.root.load_table()
            self.close()
        except Exception:
            return None


class EditCoffeeForm(QMainWindow, AddEditCoffeeFormUI):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.setupUi(self)
        self.root = root
        self.pk = 0
        self.pushButton.setText('Обновить')
        self.spinBox_2.setMaximum(10000)
        self.pushButton.clicked.connect(self.update_coffee)

    def load_coffee(self):
        try:
            cur = self.root.con.cursor()
            result = cur.execute(f"""
              SELECT * FROM coffee
              WHERE id = "{self.pk}"
            """, ).fetchone()
            self.lineEdit.setText(str(result[1]))
            self.lineEdit_2.setText(str(result[3]))
            self.spinBox.setValue(int(result[2]))
            self.spinBox_2.setValue(int(result[5]))
            self.spinBox_3.setValue(int(result[6]))
            self.textEdit.setPlainText(str(result[4]))
        except Exception:
            self.close()

    def update_coffee(self):
        try:
            cur = self.root.con.cursor()
            cur.execute(f"""
                        UPDATE coffee
                        SET sort_name = "{self.lineEdit.text().strip()}",
                            roasting = "{self.spinBox.value()}",
                            type = "{self.lineEdit_2.text().strip()}",
                            taste = "{self.textEdit.toPlainText()}",
                            price = "{self.spinBox_2.value()}",
                            volume = "{self.spinBox_3.value()}"
                        WHERE id = {self.pk}
                        """)
            self.root.con.commit()
            self.root.load_table()
            self.close()
        except Exception:
            return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
