from PySide6.QtWidgets import QMainWindow

from page_window import PageWindow


class HomeWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Home")
        self.setCentralWidget(widget)
