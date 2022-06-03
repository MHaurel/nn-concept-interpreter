import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget)


class Visualizer(QWidget):
    def __init__(self):
        """
        Initialize the class. Display the frame and the sub-elements.
        """
        super(Visualizer).__init__()
        QWidget.__init__(self)
        self.setFixedSize(1440, 800)
        
        self.model = None
        self.data = []
        self.layout = self.init_sidebar()

    def init_sidebar(self):
        layout = QVBoxLayout(self)
        layout.setObjectName("sidebar")

        t = QLabel('test')
        t.setObjectName('test')
        layout.addWidget(t)

        return layout






if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Visualizer()
    widget.show()

    with open('./css/styles.qss', "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
