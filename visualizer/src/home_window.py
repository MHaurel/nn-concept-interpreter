from PySide6.QtWidgets import QMainWindow

from page_window import PageWindow


class HomeWindow(PageWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Home")
        self.setCentralWidget(widget)

    def make_handleButton(self, button):
        def handleButton():
            if button == "sampleButton":
                self.goto("sample", None)  # Dataloader is None
            elif button == "categoriesButton":
                self.goto("categories", None)  # Dataloader is None

        return handleButton
