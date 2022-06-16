import sys
import time

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout, \
    QWidget, QPushButton, QApplication


def print_every_3_seconds():
    print(0)
    for i in range(1, 4):
        time.sleep(1)
        print(i)

class WorkerThread(QThread):
    def run(self):
        print_every_3_seconds()


class RunFunctionDialog(QDialog):
    def __init__(self, function, parent=None):
        super(RunFunctionDialog, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setText("Wait 3 seconds")
        self.layout.addWidget(self.textBrowser)
        self.function = function

        self.thread = WorkerThread()
        self.thread.finished.connect(self.close)
        self.thread.start()


def show_dialog():
    dialog = RunFunctionDialog(print_every_3_seconds)
    dialog.exec()


app = QApplication(sys.argv)

widget = QWidget(None)
button = QPushButton("Show Dialog", widget)
button.clicked.connect(show_dialog)

widget.show()

app.exec()