from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QRect

from page_window import PageWindow


class SampleWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Search for something")
        self.UiComponents()

    def go_to_home(self):
        self.goto("home", None)  # Dataloader is None

    def UiComponents(self):
        self.backButton = QPushButton("BackButton", self)
        self.backButton.setGeometry(QRect(5, 5, 100, 20))
        self.backButton.clicked.connect(self.go_to_home)

