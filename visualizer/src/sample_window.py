from page_window import PageWindow


class SampleWindow(PageWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Explore samples")
        self.setCentralWidget(widget)

