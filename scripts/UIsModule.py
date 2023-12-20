import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

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
        print(widget.result_text)
        return widget.result_text

