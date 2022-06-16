from PySide6.QtWidgets import QMainWindow, QApplication

from page_window import PageWindow


class GridWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Grid Visualization")
        self.setCentralWidget(widget)
        self.setFixedSize(800, 600)

    def set_dataloader(self, dataloader):
        self.widget.set_dataloader(dataloader)

if __name__ == '__main__':
    import sys
    from visualizer.src.widgets.table_categories_widget import TableCategoriesWidget

    app = QApplication(sys.argv)
    w = GridWindow(TableCategoriesWidget())
    w.show()
    sys.exit(app.exec())