from PySide6.QtWidgets import QMainWindow, QApplication

from page_window import PageWindow


class GridWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Grid Visualization")
        self.setCentralWidget(widget)

    def set_dataloader(self, dataloader):
        self.widget.set_dataloader(dataloader)

if __name__ == '__main__':
    import sys
    from visualizer.src.widgets.grid_widget import GridWidget

    app = QApplication(sys.argv)
    w = GridWindow(GridWidget())
    w.show()
    sys.exit(app.exec())