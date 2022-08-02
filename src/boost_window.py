from page_window import PageWindow


class BoostWindow(PageWindow):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

        self.dataloader = None
        self.sample = None
        self.category = None

        self.setWindowTitle("Boost Sample")
        self.setCentralWidget(self.widget)

    def set_dataloader(self, dataloader):
        """

        :param dataloader:
        :return:
        """
        self.dataloader = dataloader
        self.widget.set_dataloader(self.dataloader)

    def set_sample(self, sample):
        """

        :param sample:
        :return:
        """
        self.sample = sample
        self.widget.set_sample(self.sample)

    def set_category(self, category):
        """

        :param category:
        :return:
        """
        self.category = category
        self.widget.set_category(self.category)