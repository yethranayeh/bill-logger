import sys
import os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import csv
import icons

# print(qtw.QStyleFactory.keys())

class Logger(qtw.QWidget):
    log_data = qtc.pyqtSignal(float, float, float, str)
    current_year = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qtw.QFormLayout())

        float_validator = qtg.QDoubleValidator()
        self.management_edit = qtw.QLineEdit()
        self.management_edit.setValidator(float_validator)
        self.electricity_edit = qtw.QLineEdit()
        self.electricity_edit.setValidator(float_validator)
        self.rent_edit = qtw.QLineEdit()
        self.rent_edit.setValidator(float_validator)
        self.rent_edit.setPlaceholderText("1150")
        self.rent_edit.setText("1150")
        # self.rent_edit.setInputMask("0")
        self.add_button = qtw.QPushButton("Add", clicked=self.add_data_emit)

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
        self.select_year.currentIndexChanged.connect(self.change_year_emit)

        self.log_table = qtw.QTableWidget(0, 5)
        self.log_table.setHorizontalHeaderLabels(["Month", "Total", "Management", "Electricty", "Rent"])
        # self.log_table.setColumnWidth(0, 70)
        # self.log_table.setColumnWidth(1, 50)
        # self.log_table.resizeColumnToContents(2)
        # self.log_table.resizeColumnToContents(3)
        # self.log_table.setColumnWidth(4, 50)
        self.log_table.resizeRowsToContents()
        # self.log_table.

        self.layout().addRow("Management", self.management_edit)
        self.layout().addRow("Electricity", self.electricity_edit)
        self.layout().addRow("Rent", self.rent_edit)
        self.layout().addRow(self.select_year, self.select_month)
        self.layout().addRow(self.add_button)
        self.layout().addRow(self.log_table)

    def add_data_emit(self):
        mngmt = float("0"+self.management_edit.text())
        electricity = float("0"+self.electricity_edit.text())
        rent = float("0"+self.rent_edit.text())
        month = self.select_month.currentText()
        self.log_data.emit(mngmt, electricity, rent, month)

    def change_year_emit(self):
        self.current_year.emit(self.select_year.currentIndex())

class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #define anything here (widgets etc.)
        appIcon = qtg.QIcon(qtg.QPixmap(":/appIcon"))
        self.setWindowIcon(appIcon)
        self.setWindowTitle("Bill Logger")
        self.setMinimumSize(400, 330)

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Save", self.save)
        file_menu.addAction("Save As...", self.save_as)
        # file_menu.addSeparator()
        file_menu.addAction("Import...", self.import_data)
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

        self.logger_widget = Logger()
        self.setCentralWidget(self.logger_widget)
        self.logger_widget.log_data.connect(self.add_to_table)
        self.logger_widget.current_year.connect(self.change_current_table)

        #end of code
        self.show() #can be called after creating an instance if it is not meant to show right after init

    def save(self):
        if self.logger_widget.select_year.currentIndex() == 0:
            year = "2019"
        elif self.logger_widget.select_year.currentIndex() == 1:
            year = "2020"

        with open(f"{year}.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, dialect="excel")
            for row in range(self.logger_widget.log_table.rowCount()):
                row_data = []
                for column in range(self.logger_widget.log_table.columnCount()):
                    item = self.logger_widget.log_table.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                # print(row_data)
                writer.writerow(row_data)

    def save_as(self):
        path = qtw.QFileDialog.getSaveFileName(self, os.getenv("HOME"), "", "CSV(*.csv)")
        if path[0] != "":
            with open(path[0], "w", newline="") as csv_file:
                writer = csv.writer(csv_file, dialect="excel")
                # writer.writerow(["Month","Total","Management","Electricity","Rent"])
                for row in range(self.logger_widget.log_table.rowCount()):
                    row_data = []
                    for column in range(self.logger_widget.log_table.columnCount()):
                        item = self.logger_widget.log_table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    # print(row_data)
                    writer.writerow(row_data)

    def import_data(self):
        path = qtw.QFileDialog.getOpenFileName(self, os.getenv("HOME"), "", "CSV(*.csv)")
        if path[0] != "":
            with open(path[0], newline="") as csv_file:
                self.logger_widget.log_table.clearContents()
                self.logger_widget.log_table.setRowCount(0)
                my_file = csv.reader(csv_file, dialect="excel")
                for row_data in my_file:
                    row = self.logger_widget.log_table.rowCount()
                    self.logger_widget.log_table.insertRow(row)
                    # if len(row_data) > 5:
                    #     self.logger_widget.log_table.setColumnCount(len(row_data))
                    for column, content in enumerate(row_data):
                        # print(f"Colum {column}", f"Content: {content}")
                        item = qtw.QTableWidgetItem(content)
                        self.logger_widget.log_table.setItem(row, column, item)

    @qtc.pyqtSlot(float, float, float, str)
    def add_to_table(self, management, electricity, rent, month):
        if management <= 0 or electricity <= 0 or rent <= 0:
            pass
        else:
            row = self.logger_widget.log_table.rowCount()
            self.logger_widget.log_table.insertRow(row)
            self.logger_widget.log_table.setItem(row, 0, qtw.QTableWidgetItem(month))
            self.logger_widget.log_table.setItem(row, 1, qtw.QTableWidgetItem(str(management+electricity+rent)))
            self.logger_widget.log_table.setItem(row, 2, qtw.QTableWidgetItem(str(management)))
            self.logger_widget.log_table.setItem(row, 3, qtw.QTableWidgetItem(str(electricity)))
            self.logger_widget.log_table.setItem(row, 4, qtw.QTableWidgetItem(str(rent)))
        # print(management, electricity, rent)

    @qtc.pyqtSlot(int)
    def change_current_table(self, year):
        print(year)
        # self.logger_widget.log_table.clearContents()
        # self.logger_widget.log_table.setRowCount(0)


stylesheet = """
"""

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    sys.exit(app.exec_())