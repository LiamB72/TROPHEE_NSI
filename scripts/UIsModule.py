import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from scripts.utility import selData



class promptMenu(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./data/UIs/RequestOptions.ui", self)
        self.sqlRequest = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshRequest)
        self.timer.start(100)

    def refreshRequest(self):

        # This is obnoxious...
        if self.activateTime.isChecked():
            if self.activateUnder.isChecked():
                self.maxTime.setEnabled(False)
                self.minTime.setEnabled(True)

            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)

            elif self.activateBoth.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(True)
        else:
            self.minTime.setEnabled(False)
            self.maxTime.setEnabled(False)

        if self.countryActivate.isChecked():
            self.countryComboBox.setEnabled(True)
        else:
            self.countryComboBox.setEnabled(False)


    def on_button_click(self):
        input_text = self.line_edit.text()
        self.simulate_sql_request(input_text)

        # Close the application
        self.close()

    def simulate_sql_request(self, words):
        # Simulate SQL request logic based on the words
        # This is a placeholder, you should replace it with your actual SQL logic
        self.sqlRequest = words


class dynamicUI(QMainWindow):
    def __init__(self, request):
        super().__init__()
        selData(request)


class cMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/UIs/cMenu.ui", self)
        self.result_text = None
        self.lineEdit.returnPressed.connect(self.closeUI)
        self.pushButton.clicked.connect(self.closeUI)

    def closeUI(self):
        self.result_text = self.lineEdit.text()
        self.close()

def openUI(className):
    app = QApplication(sys.argv)
    widget = className()
    widget.show()
    app.exec_()
    if className == cMenu:
        return widget.result_text
    elif className == promptMenu:
        return widget.sqlRequest
