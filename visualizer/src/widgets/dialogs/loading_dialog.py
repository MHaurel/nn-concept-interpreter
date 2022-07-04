import sys
import time

from PySide6.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QLabel
from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QMovie

from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader


def print_every_3_seconds():
    print(0)
    for i in range(1, 4):
        time.sleep(1)
        print(i)


class DataLoaderIntializingThread(QThread):
    def run(self) -> None:
        # print every 3 seconds
        model = Model('../../../models/painter_model')
        dataloader = DataLoader('../../../data/painters_ds.json', model=model)


class RunFunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        #self.function = function

        print("[INFO] Loading screen initialized")

        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)

        self.movie = QMovie('loading.gif')
        self.label_animation.setMovie(self.movie)

        self.startAnimation()

        self.thread = DataLoaderIntializingThread()
        self.thread.finished.connect(self.end)
        self.thread.start()

    def startAnimation(self):
        self.movie.start()

    def end(self):
        print("[INFO] Loading screen closed")
        self.movie.stop()
        self.close()


def show_dialog():
    dialog = RunFunctionDialog()
    dialog.exec()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    widget = QWidget(None)

    button = QPushButton("Show dialog", widget)
    button.clicked.connect(show_dialog)

    widget.show()

    sys.exit(app.exec())