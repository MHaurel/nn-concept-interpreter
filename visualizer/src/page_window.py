from PySide6.QtWidgets import QMainWindow, QHBoxLayout
from PySide6.QtCore import Signal


class PageWindow(QMainWindow):
    gotoSignal = Signal(str, object, str)
    layout = QHBoxLayout()

    def goto(self, name, dataloader=None, category=None):
        """
        A method emitting a signal to change current page in the QStackedWidget defined in window.py
        :param name: the name of the window we want to go to
        :param dataloader: the dataloader we want to transfer to the next window
        :param category: the category we want to transfer to the next window
        :return: None
        """
        self.gotoSignal.emit(name, dataloader, category)
