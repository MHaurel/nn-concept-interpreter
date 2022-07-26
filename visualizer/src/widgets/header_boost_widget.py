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

        :param value:
        :return:
        """
        print(f"Selecting {self.dataloader.model.get_layers()[value].name}")
        self.parent().update_layer_index(value)

    def set_datalaoder(self, dataloader):
        self.dataloader = dataloader
        self.populate_combobox()

    def set_sample(self, sample):
        self.sample = sample

    def set_category(self, category):
        self.category = category

    def go_to_home(self):
        self.parent().go_to_home()

    def populate_combobox(self):
        self.layer_combobox.clear()
        if self.dataloader is not None:
            for layer in self.dataloader.model.get_layers():
                self.layer_combobox.addItem(layer.name)