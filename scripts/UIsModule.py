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
        self.confirmButton.clicked.connect(self.confirmButton_clicked)
        self.setSQLRequestText("SELECT * FROM olympicsdb;")

        data = selData("SELECT Team FROM olympicsdb GROUP BY Team")
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
                timeFilter = f"Games < '{self.minTime.value()}%"

            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)
                timeFilter = f"Games > '{self.maxTime.value()}%"

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
        WHERE = self.updateWHERE(medalFilter, timeFilter, teamFilter)
        self.setSQLRequestText(f"SELECT * FROM olympicsdb{WHERE}")

    def updateWHERE(self, a0: str, a1: str, a2: str):
        if a0 is not None \
        and a1 is not None \
        and a2 is not None:
            request = f" WHERE {a0} AND {a1} AND {a2}"
        elif a0 is not None \
        and a1 is not None:
            request = f" WHERE {a0} AND {a1}"
        elif a0 is not None \
        and a2 is not None:
            request = f" WHERE {a0} AND {a2}"
        elif a1 is not None \
        and a2 is not None:
            request = f" WHERE {a1} AND {a2}"
        elif a0 is not None:
            request = f" WHERE {a0}"
        elif a1 is not None:
            request = f" WHERE {a1}"
        elif a2 is not None:
            request = f" WHERE {a2}"

        else:
            request = ";"

        return request

    def checkMedal(self):
        if self.goldCB.isChecked() and self.silverCB.isChecked() and self.bronzeCB.isChecked():
            return None
        elif self.goldCB.isChecked() and self.silverCB.isChecked():
            return "Medal != 'bronze'"
        elif self.goldCB.isChecked() and self.bronzeCB.isChecked():
            return "Medal != 'silver'"
        elif self.bronzeCB.isChecked() and self.silverCB.isChecked():
            return "Medal != 'gold'"
        elif self.goldCB.isChecked():
            return "Medal = 'gold'"
        elif self.silverCB.isChecked():
            return "Medal = 'silver'"
        elif self.bronzeCB.isChecked():
            return "Medal = 'bronze'"



    def setSQLRequestText(self, text):
        self.sqlRequestBox.setText(text)

    def confirmButton_clicked(self):
        selData(self.sqlRequestBox.text().strip() + ";")


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
