from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal


class PageWindow(QMainWindow):
    gotoSignal = Signal(str)
    layout = QHBoxLayout()

    def goto(self, name):
        self.gotoSignal.emit(name)