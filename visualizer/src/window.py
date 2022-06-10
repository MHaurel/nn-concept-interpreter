from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence

import numpy as np

from home_window import HomeWindow
from page_window import PageWindow
from sample_window import SampleWindow
from categories_window import CategoriesWindow

from visualizer.src.widgets.data_widget import DataWidget
from visualizer.src.widgets.home_widget import HomeWidget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(HomeWindow(HomeWidget()), "home")
        self.register(SampleWindow(), "sample")

        # Static data importation for the moment
        data_cat = [  # Will be changed to JSON loaded files
            "French_films", "American_black_and_white_films"
        ]
        data = [
            np.random.randn(10, 12),
            np.random.randn(9, 3),
            np.random.randn(17, 4),
        ]
        widget = DataWidget(data_cat, data)
        self.register(CategoriesWindow(widget), "categories")

        # Default page
        self.goto("home", None, None)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.6, geometry.height() * 0.6)

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @Slot(str, object, object)
    def goto(self, name, model, data_path):
        print(f"model : {model}")  # DEBUG
        print(f"data_path : {data_path}")

        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())

            
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
