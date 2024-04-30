"""
File Created By BERGE Liam & REEVES Guillaume
Created on 2023-12-05
Last Update on 2024-04-29
"""
import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QGridLayout

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
        Initialises most of the variables for the request-making and UI showing
        """
        super().__init__()
        uic.loadUi("./data/UIs/RequestOptionsFR.ui", self)
        self.results_displayer = None

        self.setWindowTitle(f"{sport} - Requête SQL Créateur")

        self.request = None
        self.limit = None
        self.sortBy = None
        self.medalFilter = None
        self.timeFilter = None
        self.teamFilter = None
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

    ########### Update Method ##########
    def updEnables(self):
        """
        On a cycle of 100ms, basically a timer, loops through what's activated
        with the .isChecked() function from PyQT5, that returns true when checked.
        After checking what's checked, it enables or disables QWidgets in the UI to
        make the application overall more readable.
        """
        ############### Activating The Time Frames ##############
        if self.activateTime.isChecked():
            self.timeGroup.setEnabled(True)

            ############### Activating the before time spinBox ##############
            if self.activateUnder.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(False)
                self.timeFilter = f"Games < '{self.minTime.value()}%'"

            ###############  Activating the after time spinBox ##############
            elif self.activateUpper.isChecked():
                self.minTime.setEnabled(False)
                self.maxTime.setEnabled(True)
                self.timeFilter = f"Games > '{self.maxTime.value()}%'"

            ###############  Activating both times spinBox to make an interval ##############
            elif self.activateBoth.isChecked():
                self.minTime.setEnabled(True)
                self.maxTime.setEnabled(True)
                self.timeFilter = f"Games > '{self.maxTime.value()}%' AND Games < '{self.minTime.value()}%'"
        else:
            self.timeGroup.setEnabled(False)
            self.timeFilter = None

        ###############  Activating Team filter ##############
        if self.teamActivate.isChecked():
            self.teamFilterCombo.setEnabled(True)
            self.teamFilter = f"Team LIKE '{str(self.teamFilterCombo.currentText())}'"
        else:
            self.teamFilterCombo.setEnabled(False)
            self.teamFilter = None

        ##############  Activating a prompt/fetch output limit ##############
        if self.enableLimit.isChecked():
            self.limitGroup.setEnabled(True)
            self.limit = f"LIMIT {self.limitSpin.value()}"
        else:
            self.limitGroup.setEnabled(False)
            self.limit = None

        ##############  Activating a sorting by category ##############
        if self.enableSortBy.isChecked():
            self.sortingGroup.setEnabled(True)
            self.sortBy = f" {self.sortByCB.currentText()}"

            ################  Setting the sort by ascending ##############
            if self.ascendingRatio.isChecked():
                self.sortBy += ""
            ################  Setting the sort by descending ##############
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
        self.confirmButton.setEnabled(True)
        self.medalFilter = self.checkMedal()
        whereConditionFiller = self.updateWHERE()
        self.setSQLRequestText(f"SELECT DISTINCT Name, Team, Sport, Games, Medal FROM olympicsdb WHERE Sport LIKE '{self.sport}'{whereConditionFiller}")
    def updateWHERE(self):
        """
        Method being used when the request is being refreshed
        Overall hardcoded, it checks what was chosen within the options possible.
        """
        # No need to hardcode, just add segments, depending on whenever
        # the self-variables are None or not, to the final string, with some ifs.
        # Put the a0 component as a self-variable.
        # There is no need to put any args else than self, as everything, including the final string, is supposed
        # to be self-variables.
        fillter = ""
        if self.medalFilter is not None:
            fillter += f" AND {self.medalFilter}"
        if self.timeFilter is not None:
            fillter += f" AND {self.timeFilter}"
        if self.teamFilter is not None:
            fillter += f" AND {self.teamFilter}"

        return fillter


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
        self.request = str(text)
        self.request += " ORDER BY"

        # Sorting the data by else
        if self.sortBy is not None:
            self.request += f"{self.sortBy}"
        else:
            self.request += " Name"

        # Defining the limit
        if self.limit is not None:
            self.request += f" {self.limit}"
        self.request += ";"
        self.sqlRequestQT.setPlainText(self.request)

    def confirmButton_clicked(self):
        """
        Complex but overall simple.
        Gets the string of the SQLrequest text Box
        Then fetch the data.
        Finally, it closes itself and opens another window to display the result in a formatted way.
        """
        global app

        # Fetching the data
        data = selData(self.request)

        # Printing the data fetched if "print result" is checked
        if self.printResultCB.isChecked():
            print(data)
            print("########## NEW REQUEST ##########")
            if data[1]:
                for i in range(0, len(data[1]), 5):
                    print(f"{data[0][0]}: {data[1][i]:50}| {data[0][1]}: {data[1][i + 1]:40}| {data[0][2]}: {data[1][i + 2]:12}| {data[0][3]}: {data[1][i + 3]:12}| {data[0][4]}: {data[1][i + 4]}")
            else:
                print("Data Fletched is empty. SQL Request may be done wrongfully. Please try again.")

        self.close()
        ############## opening a new pyqt5 window. ##############
        self.results_displayer = ResultsDisplayer(data, self.request)
        self.results_displayer.show()
        if app is None:
            app = QApplication(sys.argv)
        app.exec_()


class ResultsDisplayer(QWidget):
    def __init__(self, data: list, request: str):
        super().__init__()
        self.request = request
        self.data = data

        self.sport = data[1][2]
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Result Displayer: {self.sport}")
        self.setFixedSize(800, 500)

        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        ############## SCROLL AREA CODE ##############

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setFixedSize(500, 400)
        scroll_area.setWidgetResizable(True)

        # Define Variables for later usage
        scroll_area_insides = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_insides)
        scroll_area_insides.setLayout(scroll_area_layout)

        scroll_area.setWidget(scroll_area_insides)
        scroll_area_grid = QGridLayout()

        ## Code In-Between ##
        if self.data is not None and self.data[1]:
            headers = self.data[0]
            lengthHeader = len(headers)

            for positionHeader in range(lengthHeader):
                headerLabel = QLabel(headers[positionHeader])
                scroll_area_grid.addWidget(headerLabel, 0, positionHeader)

            for i in range(0, len(self.data[1]), lengthHeader):
                startingIndex = i
                afterIndex = i + lengthHeader
                row_data = self.data[1][startingIndex:afterIndex]

                for j in range(len(row_data)):
                    valueLabel = QLabel(row_data[j])
                    scroll_area_grid.addWidget(valueLabel, i + 1, j)
        else:
            label_empty = QLabel("The data fetched is empty")
            scroll_area_layout.addWidget(label_empty)
        #####################

        scroll_area_layout.addLayout(scroll_area_grid)
        scroll_area_insides.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_insides)

        ##############################################

        top_layout.addWidget(scroll_area)

        ############## IMAGE CODE ##############

        image = QLabel()
        image.setFixedSize(0, 0)

        pixmap = QPixmap(f"./data/images/QTImages/pixmaps/{self.sport}.png")
        image.setPixmap(pixmap)
        image.setMaximumSize(pixmap.size())
        image.setMinimumSize(pixmap.size())

        top_layout.addSpacing(5)
        top_layout.addWidget(image)

        #########################################

        main_layout.addLayout(top_layout)
        main_layout.addSpacing(10)

        ############## LINE EDIT CODE ##############

        plainTextEdit = QPlainTextEdit(self.request)
        plainTextEdit.setReadOnly(True)
        if self.request == "":
            plainTextEdit.setPlaceholderText("SQL Request hasn't loaded correctly")

        bottom_layout.addWidget(plainTextEdit)

        ############################################

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)


class cMenu(QMainWindow):
    """
    Creates a debug window that lets you input a line of command
    such as "tp x y" or "db True/False", which in order lets
    the player teleport an x and y coordinates, or change the debug mode to True or False.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi("./data/UIs/cMenu.ui", self) # Loads the ui element
        self.result_text = None
        self.lineEdit.returnPressed.connect(self.closeUI)
        self.pushButton.clicked.connect(self.closeUI)

    def closeUI(self):
        self.result_text = self.lineEdit.text() # Gets the text from the line edit to return it
        self.close()    # Closes the ui.


app = QApplication(sys.argv)

def openHelpWindow(string: str):
    ## Opens a help window
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon("./data/QTImages/information.png"))
    msg.setText(string)
    msg.setWindowTitle("Aide")
    msg.exec_()


def openUI(className, option01=None):
    """
    Opens a new UI depending on the className and option01 if there are any required.
    """
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