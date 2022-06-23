from PySide6.QtWidgets import QMainWindow, QApplication

from visualizer.src.page_window import PageWindow


class ExploreCategoryWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Explore category")

        self.widget = widget

        self.category = None
        self.dataloader = None

        self.setCentralWidget(self.widget)

    def set_category(self, category):
        """
        Set the category in parameter to this class
        :param category: The category to set to this class
        :return: None
        """
        self.category = category
        self.setWindowTitle(self.category)
        self.widget.set_category(self.category)

    def set_dataloader(self, dataloader):
        """
        Set the dataloader in parameter to this class
        :param dataloader: The dataloader to set to this class
        :return: None
        """
        self.dataloader = dataloader
        self.widget.set_dataloader(self.dataloader)

if __name__ == '__main__':
    import sys
    from visualizer.src.widgets.explore_category_widget import ExploreCategoryWidget

    app = QApplication(sys.argv)

    widget = ExploreCategoryWidget()

    w = ExploreCategoryWindow(widget)
    w.show()
    sys.exit(app.exec())