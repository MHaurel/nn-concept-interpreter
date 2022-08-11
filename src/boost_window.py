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
        Updates the dataloader in this class and in the child widget.
        :param dataloader: the dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.widget.set_dataloader(self.dataloader)

    def set_sample(self, sample):
        """
        Updates the samples in this class and in the child widget
        :param sample: the sample to set
        :return: None
        """
        self.sample = sample
        self.widget.set_sample(self.sample)

    def set_category(self, category):
        """
        Updates the category in this class and in the child widget
        :param category: the category to set
        :return: None
        """
        self.category = category
        self.widget.set_category(self.category)