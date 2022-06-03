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

        self.hello = [
            "Hallo Welt",
            "ä½ å¥½ï¼Œä¸–ç•Œ",
            "Hei maailma",
            "Hola Mundo",
            "ÐŸÑ€Ð¸Ð²ÐµÑ‚ Ð¼Ð¸Ñ€",
        ]

        self.button = QPushButton("Click me!")
        self.message = QLabel("Hello World")
        self.message.alignment = Qt.AlignCenter

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.button)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.message.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Visualizer()
    widget.show()

    sys.exit(app.exec())
