from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox


class HeaderBoostWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.sample = None
        self.category = None

        # Home button
        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.go_to_home)

        # Layer combobox
        self.layer_combobox = QComboBox()
        self.layer_combobox.currentIndexChanged.connect(self.on_item_changed)
        self.populate_combobox()

        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.btn_home)
        self.main_layout.addWidget(self.layer_combobox)

        # Setting layout
        self.setLayout(self.main_layout)

    def on_item_changed(self, value):
        """
        Overrided event to see if an item has changed.
        :param value: the new value of the combobox (the index of the layer)
        :return: None
        """
        self.parent().update_layer_index(value)

    def set_datalaoder(self, dataloader):
        """
        Updates dataloader in this class and populates combobox
        :param dataloader: the dataloader to set.
        :return: None
        """
        self.dataloader = dataloader
        self.populate_combobox()

    def set_sample(self, sample):
        """
        Update sample in this class.
        :param sample: the sample to set
        :return: None
        """
        self.sample = sample

    def set_category(self, category):
        """
        Updates category in this class
        :param category: the category to set
        :return: None
        """
        self.category = category

    def go_to_home(self):
        """
        Go to home page
        :return: None
        """
        self.parent().go_to_home()

    def populate_combobox(self):
        """
        Clears the combobox and then fill it with the layers of the model.
        :return: None
        """
        self.layer_combobox.clear()
        if self.dataloader is not None:
            for layer in self.dataloader.model.get_layers():
                self.layer_combobox.addItem(layer.name)