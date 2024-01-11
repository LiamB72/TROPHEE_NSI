import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from scripts.utility import selData


class promptMenu(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("../data/UIs/RequestOptions.ui", self)
        self.sqlRequestText = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updEnables)
        self.timer.start(100)

        self.updButton.clicked.connect(self.refreshRequest)
        self.confirmButton.clicked.connect(self.confirmButton_clicked)
        self.sqlRequestQT.setPlaceholderText("[This is where the request is displayed]\nCan be edited directly")

        data = selData("SELECT Team FROM olympicsdb GROUP BY Team")
        for i in range(len(data[1])):
            self.teamFilterCombo.addItem(data[1][i])

    def updEnables(self):
        if self.activateTime.isChecked():
            if self.activateUnder.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(False)

            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)

            elif self.activateBoth.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(True)
        else:
            self.minTime.setEnabled(False)
            self.maxTime.setEnabled(False)

        if self.teamActivate.isChecked():
            self.teamFilterCombo.setEnabled(True)
        else:
            self.teamFilterCombo.setEnabled(False)

        if self.enableLimit.isChecked():
            self.limitSpin.setEnabled(True)
        else:
            self.limitSpin.setEnabled(False)

    def refreshRequest(self):
        ###### Activation Buttons ######

        # This is obnoxious...
        if self.activateTime.isChecked():
            if self.activateUnder.isChecked():
                timeFilter = f"Games < '{self.minTime.value()}%"

            elif self.activateUpper.isChecked():
                timeFilter = f"Games > '{self.maxTime.value()}%"

            elif self.activateBoth.isChecked():
                timeFilter = f"Games < {self.maxTime.value()} AND Games > {self.minTime.value()}"
        else:
            timeFilter = None

        if self.teamActivate.isChecked():
            teamFilter = f"Team LIKE '{str(self.teamFilterCombo.currentText())}'"
        else:
            teamFilter = None

        if self.enableLimit.isChecked():
            limit = f"LIMIT {self.limitSpin.value()}"
        else:
            limit = None

        ###### ################## ######
        medalFilter = self.checkMedal()
        WHERE = self.updateWHERE(medalFilter, timeFilter, teamFilter, limit)
        self.setSQLRequestText(f"SELECT Name, Team, Sport, Games, Medal FROM olympicsdb{WHERE}")

    def updateWHERE(self, a0: str, a1: str, a2: str, a3: str):
        if a0 is not None and a1 is not None \
                and a2 is not None and a3 is not None:
            request = f" WHERE {a0} AND {a1} AND {a2} {a3}"

        elif a0 is not None and a1 is not None:
            request = f" WHERE {a0} AND {a1}"
        elif a0 is not None and a2 is not None:
            request = f" WHERE {a0} AND {a2}"
        elif a0 is not None and a3 is not None:
            request = f" WHERE {a0} {a3}"

        elif a1 is not None and a2 is not None:
            request = f" WHERE {a1} AND {a2}"
        elif a1 is not None and a3 is not None:
            request = f" WHERE {a1} {a3}"

        elif a2 is not None and a3 is not None:
            request = f" WHERE {a2} {a3}"

        elif a0 is not None:
            request = f" WHERE {a0}"
        elif a1 is not None:
            request = f" WHERE {a1}"
        elif a2 is not None:
            request = f" WHERE {a2}"
        elif a3 is not None:
            request = f" {a3}"

        else:
            request = ""

        return request

    def checkMedal(self):
        if self.goldCB.isChecked() and self.silverCB.isChecked() and self.bronzeCB.isChecked():
            return None
        elif self.goldCB.isChecked() and self.silverCB.isChecked():
            return 'Medal != "Bronze"'
        elif self.goldCB.isChecked() and self.bronzeCB.isChecked():
            return 'Medal != "Silver"'
        elif self.bronzeCB.isChecked() and self.silverCB.isChecked():
            return 'Medal != "Gold"'
        elif self.goldCB.isChecked():
            return 'Medal = "Gold"'
        elif self.silverCB.isChecked():
            return 'Medal = "Silver"'
        elif self.bronzeCB.isChecked():
            return 'Medal = "Bronze"'

    def setSQLRequestText(self, text):
        self.sqlRequestQT.setText(text)

    def confirmButton_clicked(self):
        string = str(self.sqlRequestQT.text())
        string += ";"
        data = selData(string)
        print(data)



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
        return widget.sqlRequestText


openUI(promptMenu)
