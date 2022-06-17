from PySide6.QtWidgets import QMainWindow, QHBoxLayout
from PySide6.QtCore import Signal


class PageWindow(QMainWindow):
    gotoSignal = Signal(str, object, str)  # Name of the window and dataloader
    layout = QHBoxLayout()

    def goto(self, name, dataloader=None, category=None):
        self.gotoSignal.emit(name, dataloader, category)
