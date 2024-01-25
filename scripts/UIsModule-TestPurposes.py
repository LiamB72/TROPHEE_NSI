import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout

from scripts.utilityTest import selData


class promptMenu(QMainWindow, QWidget):
    def __init__(self, sport):
        super().__init__()
        uic.loadUi("../data/UIs/RequestOptionsFR.ui", self)
        self.results_displayer = None

        self.limit = None
        self.groupBy = None
        self.medalFilter = None
        self.timeFilter = None
        self.teamFilter = None
        self.sqlRequestText = None
        self.sport = sport

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updEnables)
        self.timer.start(100)

        self.updButton.clicked.connect(self.refreshRequest)
        self.confirmButton.clicked.connect(self.confirmButton_clicked)
        self.sqlRequestQT.setPlaceholderText("[Requête SQL est affichée **ici**]")

        teamData = selData(f"SELECT Team FROM olympicsdb WHERE sport LIKE '{self.sport}' GROUP BY Team;")
        for i in range(len(teamData[1])):
            self.teamFilterCombo.addItem(teamData[1][i])

        headers = selData(f"SELECT Name, Team, Sport, Games, Medal FROM olympicsdb WHERE sport LIKE 'NULL';")
        for i in range(len(headers[0])):
            self.sortByCB.addItem(headers[0][i])

    def updEnables(self): # This is hidious LOL
        if self.activateTime.isChecked():
            self.timeGroup.setEnabled(True)
            if self.activateUnder.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(False)
                self.timeFilter = f"Games < '{self.minTime.value()}%'"

            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)
                self.timeFilter = f"Games > '{self.maxTime.value()}%'"

            elif self.activateBoth.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(True)
                self.timeFilter = f"Games < '{self.maxTime.value()}' AND Games > '{self.minTime.value()}'"
        else:
            self.timeGroup.setEnabled(False)
            self.timeFilter = None

        if self.teamActivate.isChecked():
            self.teamFilterCombo.setEnabled(True)
            self.teamFilter = f"Team LIKE '{str(self.teamFilterCombo.currentText())}'"
        else:
            self.teamFilterCombo.setEnabled(False)
            self.teamFilter = None

        if self.enableLimit.isChecked():
            self.limitGroup.setEnabled(True)
            self.limit = f"LIMIT {self.limitSpin.value()}"
        else:
            self.limitGroup.setEnabled(False)
            self.limit = None

        if self.enableSortBy.isChecked():
            self.sortingGroup.setEnabled(True)
            self.groupBy = f" {self.sortByCB.currentText()}"
        else:
            self.sortingGroup.setEnabled(False)
            self.groupBy = None

    def refreshRequest(self):
        ###### ################## ######
        medalFilter = self.checkMedal()
        WHERE = self.updateWHERE(medalFilter, self.timeFilter, self.teamFilter)
        self.setSQLRequestText(f"SELECT Name, Team, Sport, Games, Medal FROM olympicsdb WHERE Sport LIKE '{self.sport}'{WHERE}")

    def updateWHERE(self, a0: str, a1: str, a2: str):
        if a0 is not None and a1 is not None and a2 is not None:
            request = f" AND {a0} AND {a1} AND {a2}"

        elif a0 is not None and a1 is not None:
            request = f" AND {a0} AND {a1}"
        elif a0 is not None and a2 is not None:
            request = f" AND {a0} AND {a2}"
        elif a1 is not None and a2 is not None:
            request = f" AND {a1} AND {a2}"

        elif a0 is not None:
            request = f" AND {a0}"
        elif a1 is not None:
            request = f" AND {a1}"
        elif a2 is not None:
            request = f" AND {a2}"

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
        self.sqlRequestQT.setPlainText(text)

    def confirmButton_clicked(self):
        global app
        string = str(self.sqlRequestQT.toPlainText())
        string += " ORDER BY"

        # Sorting the data by...
        if self.groupBy is not None:
            string += f"{self.groupBy}"
        else:
            string += " Name"

        # Defining the limit
        if self.limit is not None:
            string += f" {self.limit}"
        string += ";"
        # Fetching the data
        data = selData(string)

        # Printing the data fetched
        if self.printResultCB.isChecked():
            print(data)
            print("########## NEW REQUEST ##########")
            if data[1]:
                i = 0
                for i in range(0, len(data[1]), 5):
                    print(f"{data[0][0]}: {data[1][i]:50}| {data[0][1]}: {data[1][i + 1]:40}| {data[0][2]}: {data[1][i + 2]:12}| {data[0][3]}: {data[1][i + 3]:12}| {data[0][4]}: {data[1][i + 4]}")
            else:
                print("Data Fletched is empty. SQL Request may be done wrongfully. Please try again.")

        self.close()

        self.results_displayer = ResultsDisplayer(data)
        self.results_displayer.show()
        if app is None:
            app = QApplication(sys.argv)
        app.exec_()


class ResultsDisplayer(QWidget):
    def __init__(self, data):
        super().__init__()

        widthWin, heightWin = 750, 500

        self.setWindowTitle("Test UI")
        self.setFixedSize(widthWin, heightWin)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setGeometry(10, 10 ,500, 420)

        widget = QWidget()
        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        if data is not None and data[1]:
            headers = data[0]
            lenghtHeader = len(headers)

            grid_layout = QGridLayout()
            widget_layout.addLayout(grid_layout)

            for posHeader in range(lenghtHeader):
                headerLabel = QLabel(headers[posHeader])
                grid_layout.addWidget(headerLabel, 0, posHeader)

            # Placing the data in a grid so everythig's aligned
            for index in range(0, len(data[1]), 5):
                startingIndex = index
                afterIndex = index + lenghtHeader
                row_data = data[1][startingIndex:afterIndex]

                # Spacing on the right
                for j in range(len(row_data)):
                    valueLabel = QLabel(row_data[j])
                    print(row_data[j])
                    grid_layout.addWidget(valueLabel, index + 1, j)

        else:
            label_empty = QLabel("The data fetched is empty")
            widget_layout.addWidget(label_empty)

        self.scroll_area.setWidget(widget)
        self.layout.addWidget(self.scroll_area)


class cMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../data/UIs/cMenu.ui", self)
        self.result_text = None
        self.lineEdit.returnPressed.connect(self.closeUI)
        self.pushButton.clicked.connect(self.closeUI)

    def closeUI(self):
        self.result_text = self.lineEdit.text()
        self.close()


app = QApplication(sys.argv)


def openUI(className, option01=None):
    global app
    widget = None

    if app is None:
        app = QApplication(sys.argv)

    if className == cMenu:
        widget = cMenu()

    elif className == promptMenu:
        widget = promptMenu(option01)

    widget.show()
    app.exec_()

    if className == cMenu:
        return widget.result_text

openUI(promptMenu, "Gymnastics")
