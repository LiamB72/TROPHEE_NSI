import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from scripts.utility import selData



class promptMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.sqlRequest = None
        screen_geometry = QApplication.desktop().screenGeometry()

        # Access screen width and height
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        app_width, app_height = 400, 100

        # Set window properties
        self.setWindowTitle("SQL Request Simulator")
        self.setGeometry((screen_width // 2) - app_width // 2,
                         (screen_height // 2) - app_height // 2,
                         app_width,
                         app_height)

        # Widgets
        self.line_edit = QLineEdit()
        self.result_label = QLabel("Info will be displayed here.")
        self.button = QPushButton("Submit")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.result_label)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        input_text = self.line_edit.text()
        words = input_text.split()
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

print(openUI(promptMenu))
