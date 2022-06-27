from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, QIcon

import numpy as np

from home_window import HomeWindow
from sample_window import SampleWindow
from explore_category_window import ExploreCategoryWindow

from widgets.home_widget import HomeWidget
from widgets.explore_category_widget import ExploreCategoryWidget
from widgets.sample_widget import SampleWidget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setWindowIcon(QIcon('icon.png'))

        self.m_pages = {}

        self.register(HomeWindow(HomeWidget()), "home")

        explore_category_widget = ExploreCategoryWidget()
        self.register(ExploreCategoryWindow(explore_category_widget), "explore_category")

        sample_widget = SampleWidget()
        self.register(SampleWindow(sample_widget), "sample")

        # Default page
        self.goto("home", None, None)  # Dataloader is None

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
        self.setMinimumSize(geometry.width() * 0.6, geometry.height() * 0.6)
        #self.setFixedSize(geometry.width() * 0.6, geometry.height() * 0.6)

    def register(self, window, name):
        """
        Register the window and its name in QStackedWidget in order to associate both and change window when passing its
        name in goto.
        :param window: the window to register
        :param name: the name to register
        :return: None
        """
        self.m_pages[name] = window
        self.stacked_widget.addWidget(window)

        window.gotoSignal.connect(self.goto)

    @Slot(str, object, str)
    def goto(self, name, dataloader, category):
        """
        Change the QStackedWidget current window to display the one with the name in parameter
        :param name: The name of the window to display
        :param dataloader: The dataloader to pass into the new current window
        :param category: The category to pass into the new current window
        :return: None
        """
        if name in self.m_pages:
            window = self.m_pages[name]
            if name == "categories":
                window.set_dataloader(dataloader)

            if name == "explore_category":
                window.set_dataloader(dataloader)
                window.set_category(category)

            self.stacked_widget.setCurrentWidget(window)
            self.setWindowTitle(window.windowTitle())

            
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
