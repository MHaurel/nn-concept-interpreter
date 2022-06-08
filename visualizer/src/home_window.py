from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout

from page_window import PageWindow


class HomeWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")

        # Test search button
        self.searchButton = QPushButton('', self)
        self.searchButton.clicked.connect(
            self.make_handleButton("searchButton")
        )

        # Categories button
        self.categoriesButton = QPushButton("Categories", self)
        self.categoriesButton.clicked.connect(
            self.make_handleButton("categoriesButton")
        )

        # Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.searchButton)
        self.main_layout.addSpacing(100)

    def make_handleButton(self, button):
        def handleButton():
            if button == "searchButton":
                self.goto("search")
            elif button == "categoriesButton":
                self.goto("categories")

        return handleButton
