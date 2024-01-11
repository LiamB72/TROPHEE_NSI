import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from scripts.utility import selData



class promptMenu(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("../data/UIs/RequestOptions.ui", self)
        self.sqlRequest = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshRequest)
        self.timer.start(100)
        self.confirmButton.clicked.connect(self.on_button_click)
        self.setSQLRequestText("SELECT * FROM olympicsdb")
        self.optionString = "WHERE "

        data = selData("SELECT Sport FROM olympicsdb GROUP BY Sport")
        for i in range(len(data[1])):
            self.teamFilterCombo.addItem(data[1][i])

    def refreshRequest(self):
        ###### Activation Buttons ######

        # This is obnoxious...
        if self.activateTime.isChecked():
            timeFilter = None
            if self.activateUnder.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(False)
                timeFilter = f"Games LIKE '{self.minTime.value()}%"

            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)
                timeFilter = f"Games LIKE '{self.maxTime.value()}%"

            elif self.activateBoth.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(True)
                timeFilter = f"Games < {self.maxTime.value()} AND Games > {self.minTime.value()}"
        else:
            self.minTime.setEnabled(False)
            self.maxTime.setEnabled(False)
            timeFilter = None

        if self.teamActivate.isChecked():
            self.teamFilterCombo.setEnabled(True)
            teamFilter = f"Team LIKE '{str(self.teamFilterCombo.currentText())}'"
        else:
            self.teamFilterCombo.setEnabled(False)
            teamFilter = None

        ###### ################## ######
        medalFilter = self.checkMedal()
        if timeFilter is not None:
            print(timeFilter)

    def checkMedal(self):
        stringReturned = ""
        if self.goldCB.isChecked() and self.silverCB.isChecked() and self.bronzeCB.isChecked():
            return None
        elif self.goldCB.isChecked() and self.silverCB.isChecked():
            stringReturned = "!=bronze"
            return stringReturned
        elif self.goldCB.isChecked() and self.bronzeCB.isChecked():
            stringReturned = "!=silver"
            return stringReturned
        elif self.bronzeCB.isChecked() and self.silverCB.isChecked():
            stringReturned = "!=gold"
            return stringReturned

    def setSQLRequestText(self, text):
        self.sqlRequestBox.setText(text)

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

openUI(promptMenu)
