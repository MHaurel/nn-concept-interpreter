import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap

from DataLoader import DataLoader

from tensorflow import keras


class Visualizer(QWidget):
    def __init__(self):
        """
        Initialize the class. Display the frame and the sub-elements.
        """
        super(Visualizer).__init__()
        QWidget.__init__(self)

        self.setFixedSize(1080, 600)

        self.layout = QHBoxLayout(self)

        model_img = QLabel()
        model_pixmap = QPixmap('./src/img/model_ill.png')
        model_img.setPixmap(model_pixmap)
        model_img.setMask(model_pixmap.mask())

        self.layout.addWidget(model_img)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Visualizer()
    widget.show()

    with open('./css/styles.qss', "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
