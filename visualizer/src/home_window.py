from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow
from PySide6.QtCore import Qt

from page_window import PageWindow


class HomeWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Home")
        self.setCentralWidget(widget)
        """
        super().__init__()
        self.setWindowTitle("Home")

        print(self.layout)
        self.setLayout(self.layout)

        # Test search button
        self.sampleButton = QPushButton("Sample", self)
        self.sampleButton.clicked.connect(
            self.make_handleButton("sampleButton")
        )

        # Categories button
        self.categoriesButton = QPushButton("Categories", self)
        self.categoriesButton.clicked.connect(
            self.make_handleButton("categoriesButton")
        )

        
        # Layout
        self.layout.addWidget(self.sampleButton)
        self.layout.addWidget(self.categoriesButton)
        """

    def make_handleButton(self, button):
        def handleButton():
            if button == "sampleButton":
                self.goto("sample")
            elif button == "categoriesButton":
                self.goto("categories")

        return handleButton
