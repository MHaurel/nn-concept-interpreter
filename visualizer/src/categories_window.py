from PySide6.QtWidgets import QMainWindow, QPushButton

from page_window import PageWindow


class CategoriesWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Categories")
        self.setCentralWidget(widget)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")
