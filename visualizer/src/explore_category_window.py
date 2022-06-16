from PySide6.QtWidgets import QMainWindow, QApplication

from visualizer.src.page_window import PageWindow


class ExploreCategoryWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.widget = widget

        self.category = None
        self.dataloader = None

        self.setCentralWidget(self.widget)

    def set_category(self, category):
        self.category = category
        self.setWindowTitle(self.category)
        self.widget.set_category(self.category)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        self.widget.set_dataloader(self.dataloader)

    """def go_to_home(self):
        print(self.__class__, "go_to_home")"""



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    from widgets.explore_category_widget import ExploreCategoryWidget

    widget = ExploreCategoryWidget()

    w = ExploreCategoryWindow(widget)
    w.show()
    sys.exit(app.exec())