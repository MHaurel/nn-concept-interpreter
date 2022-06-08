from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal


class PageWindow(QMainWindow):
    gotoSignal = Signal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)