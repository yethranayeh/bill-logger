import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import icons

class Logger(qtw.QWidget):
    log_data = qtc.pyqtSignal(int, int, int, str)
    # current_year = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qtw.QFormLayout())
        self.setMinimumSize(450, 300)

        self.management_edit = qtw.QLineEdit()
        self.electricity_edit = qtw.QLineEdit()
        self.rent_edit = qtw.QLineEdit()
        self.rent_edit.setPlaceholderText("1150")
        self.add_button = qtw.QPushButton("Add", clicked=self.add_emit)
        self.select_month = qtw.QComboBox()
        self.select_month.addItem("January")
        self.select_month.addItem("February")
        self.select_month.addItem("March")
        self.select_month.addItem("April")
        self.select_month.addItem("May")
        self.select_month.addItem("June")
        self.select_month.addItem("July")
        self.select_month.addItem("August")
        self.select_month.addItem("September")
        self.select_month.addItem("October")
        self.select_month.addItem("November")
        self.select_month.addItem("December")
        self.select_year = qtw.QComboBox()
        self.select_year.addItem("2019")
        self.select_year.addItem("2020")
        self.select_year.setStatusTip("tst")

        self.log_table = qtw.QTableWidget(0, 5)
        self.log_table.setHorizontalHeaderLabels(["Month", "Total", "Management", "Electricty", "Rent"])

        self.layout().addRow("Management", self.management_edit)
        self.layout().addRow("Electricity", self.electricity_edit)
        self.layout().addRow("Rent", self.rent_edit)
        self.layout().addRow(self.select_year, self.select_month)
        self.layout().addRow(self.add_button)
        self.layout().addRow(self.log_table)

    def add_emit(self):
        mngmt = int("0"+self.management_edit.text())
        electricity = int("0"+self.electricity_edit.text())
        rent = int("0"+self.rent_edit.text())
        month = self.select_month.currentText()
        self.log_data.emit(mngmt, electricity, rent, month)


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #define anything here (widgets etc.)
        appIcon = qtg.QIcon(qtg.QPixmap(":/appIcon"))
        self.setWindowIcon(appIcon)
        self.setWindowTitle("Bill Logger")
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Save", self.save)
        file_menu.addAction("Save As", self.save_as)
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

        self.logger_widget = Logger()
        self.setCentralWidget(self.logger_widget)
        self.logger_widget.log_data.connect(self.add_to_table)

        #end of code
        self.show() #can be called after creating an instance if it is not meant to show right after init


    def save(self):
        pass

    def save_as(self):
        pass

    @qtc.pyqtSlot(int, int, int, str)
    def add_to_table(self, management, electricity, rent, month):
        row = self.logger_widget.log_table.rowCount()
        self.logger_widget.log_table.insertRow(row)
        self.logger_widget.log_table.setItem(row, 0, qtw.QTableWidgetItem(month))
        self.logger_widget.log_table.setItem(row, 1, qtw.QTableWidgetItem(str(management+electricity+rent)))
        self.logger_widget.log_table.setItem(row, 2, qtw.QTableWidgetItem(str(management)))
        self.logger_widget.log_table.setItem(row, 3, qtw.QTableWidgetItem(str(electricity)))
        self.logger_widget.log_table.setItem(row, 4, qtw.QTableWidgetItem(str(rent)))
        # print(management, electricity, rent)


stylesheet = """
"""

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())