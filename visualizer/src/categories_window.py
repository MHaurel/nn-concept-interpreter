from PySide6.QtWidgets import QMainWindow

from page_window import PageWindow


class CategoriesWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Categories")

        self.widget = widget
        self.setCentralWidget(self.widget)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

    def set_dataloader(self, dataloader):
        self.widget.set_dataloader(dataloader)
