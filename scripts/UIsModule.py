"""
File Created By BERGE Liam & REEVES Guillaume
Created on 2023-12-05
Last Update on 2024-01-25
"""
import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout

from scripts.utility import selData


class promptMenu(QMainWindow, QWidget):
    """
    Shows a User Interface (commonly known as a UI) where the user
    is prompted to activate checks and to choose across many options
    what kind of request do they want.
    Overall, the code is mostly hardcoded T-T.
    """
    def __init__(self, sport):
        """

        :param sport: str
        Initialises most of the variables for the request-making and UI showing
        """
        super().__init__()
        uic.loadUi("./data/UIs/RequestOptionsFR.ui", self)
        self.results_displayer = None

        self.setWindowTitle(sport)

        self.limit = None
        self.sortBy = None
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

    def updEnables(self):
        """
        On a cycle of 100ms, basically a timer, loops through what's activated
        with the .isChecked() function from PyQT5, that returns true when checked.
        After checking what's checked, it enables or disables QWidgets in the UI to
        make the application overall more readable.
        """
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
            self.sortBy = f" {self.sortByCB.currentText()}"

            if self.ascendingRatio.isChecked():
                self.sortBy += ""
            elif self.descendingRatio.isChecked():
                self.sortBy += " DESC"
        else:
            self.sortingGroup.setEnabled(False)
            self.sortBy = None

    def refreshRequest(self):
        """
        Refresh the SQL request sorted inside the SQLRequestText element of the PyQT5 Window,
        all through what's been checked and activated.
        """
        medalFilter = self.checkMedal()
        WHERE = self.updateWHERE(medalFilter)
        self.setSQLRequestText(f"SELECT Name, Team, Sport, Games, Medal FROM olympicsdb WHERE Sport LIKE '{self.sport}'{WHERE}")

    def updateWHERE(self, a0: str):
        """
        Method being used when the request is being refreshed
        Overall hardcoded, it checks what was chosen within the options possible.
        :param a0: Str (medalFilter)
        """
        if a0 is not None and self.timeFilter is not None and self.teamFilter is not None:
            return f" AND {a0} AND {self.timeFilter} AND {self.teamFilter}"

        elif a0 is not None and self.timeFilter is not None:
            return f" AND {a0} AND {self.timeFilter}"
        elif a0 is not None and self.teamFilter is not None:
            return f" AND {a0} AND {self.teamFilter}"
        elif self.timeFilter is not None and self.teamFilter is not None:
            return f" AND {self.timeFilter} AND {self.teamFilter}"

        elif a0 is not None:
            return f" AND {a0}"
        elif self.timeFilter is not None:
            return f" AND {self.timeFilter}"
        elif self.teamFilter is not None:
            return f" AND {self.teamFilter}"

    def checkMedal(self):
        """
        Checks what medal is selected.
        Hardcoded too.
        :return: Str
        """
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
        """
        Updates the text displayed on the UI
        :param text: Str
        :return: None
        """
        self.sqlRequestQT.setPlainText(text)

    def confirmButton_clicked(self):
        """
        Complex but overall simple.
        Finis
        """
        global app
        string = str(self.sqlRequestQT.toPlainText())
        string += " ORDER BY"

        # Sorting the data by else
        if self.sortBy is not None:
            string += f"{self.sortBy}"
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
        self.scroll_area.setGeometry(10, 10, 500, 400)

        widget = QWidget()
        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        if data is not None and data[1]:
            headers = data[0]
            lenghtHeader = len(headers)

            grid_layout = QGridLayout()
            widget_layout.addLayout(grid_layout)

            for positionHeader in range(lenghtHeader):
                headerLabel = QLabel(headers[positionHeader])
                grid_layout.addWidget(headerLabel, 0, positionHeader)

            for index in range(0, len(data[1]), 5):
                startingIndex = index
                afterIndex = index + lenghtHeader
                row_data = data[1][startingIndex:afterIndex]

                for item in range(len(row_data)):
                    valueLabel = QLabel(row_data[item])
                    grid_layout.addWidget(valueLabel, index + 1, item)

        else:
            label_empty = QLabel("The data fetched is empty")
            widget_layout.addWidget(label_empty)

        self.scroll_area.setWidget(widget)
        self.layout.addWidget(self.scroll_area)


class cMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./data/UIs/cMenu.ui", self)
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