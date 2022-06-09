from PySide6.QtWidgets import QMainWindow, QHBoxLayout
from PySide6.QtCore import Signal


class PageWindow(QMainWindow):
    gotoSignal = Signal(str, object, object)
    layout = QHBoxLayout()

    def goto(self, name, model=None, data_path=None):
        print(f"model : {model}")
        print(f"data_path : {data_path}")
        self.gotoSignal.emit(name, model, data_path)