import time

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser

from visualizer.src.backend.dataloader import DataLoader
from visualizer.src.backend.model import Model

import sys


class DataloaderInitThread(QThread):
    def run(self):
        init_dataloader()

def init_dataloader():
    model = Model('../../../models/bycountry_model')
    data_path = ('../../../data/bycountry_ds.json')
    dataloader = DataLoader(data_path, model, compute_data=False)
    print(dataloader.path)

class RunFunctionDialog(QDialog):
    def __init__(self, function, parent=None):
        super(RunFunctionDialog, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setText("Please Wait...")
        self.layout.addWidget(self.textBrowser)
        self.function = function

        self.thread = DataloaderInitThread()
        self.thread.finished.connect(self.close)
        self.thread.start()

def show_dialog():
    dialog = RunFunctionDialog(init_dataloader)
    dialog.exec()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QWidget, QPushButton
    from visualizer.src.widgets.dialogs.run_function_dialog import TestWidget
    app = QApplication(sys.argv)

    widget = TestWidget()

    widget.show()

    app.exec()