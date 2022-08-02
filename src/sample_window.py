from page_window import PageWindow


class SampleWindow(PageWindow):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

        self.dataloader = None

        self.setWindowTitle("Explore sample")
        self.setCentralWidget(self.widget)

    def set_dataloader(self, dataloader):
        """
        Set the dataloader in parameter to this class
        :param dataloader: The dataloader to set to this class
        :return: None
        """
        self.dataloader = dataloader
        self.widget.set_dataloader(self.dataloader)