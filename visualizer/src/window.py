from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence

import numpy as np

from home_window import HomeWindow
from page_window import PageWindow
from sample_window import SampleWindow
from categories_window import CategoriesWindow
from grid_window import GridWindow
from explore_category_window import ExploreCategoryWindow

from widgets.categories_widget import CategoriesWidget
from widgets.home_widget import HomeWidget
from widgets.table_categories_widget import TableCategoriesWidget
from widgets.explore_category_widget import ExploreCategoryWidget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(HomeWindow(HomeWidget()), "home")
        self.register(ExploreCategoryWindow(ExploreCategoryWidget()), "explore_category")
        self.register(SampleWindow(), "sample")

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
        self.setFixedSize(geometry.width() * 0.6, geometry.height() * 0.6)

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @Slot(str, object, str)
    def goto(self, name, dataloader, category):
        print(self.__class__, "goto", name)
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
