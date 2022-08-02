from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QComboBox


class ChooseLayerPopup(QDialog):
    def __init__(self, refwindow, dataloader):
        super().__init__()

        self.refwindow = refwindow
        self.dataloader = dataloader

        self.layer_combo_box = QComboBox()
        self.populate_combo_box()

        self.ok_btn = QPushButton("Confirm")
        self.ok_btn.clicked.connect(self.test)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.layer_combo_box)
        self.main_layout.addWidget(self.ok_btn)

        self.setLayout(self.main_layout)

    def populate_combo_box(self):
        if self.dataloader is not None:
            for layer in self.dataloader.model.get_layers():
                self.layer_combo_box.addItem(layer.name)

    def test(self):
        chosen_layer_index = self.layer_combo_box.currentIndex()
        layer_name = self.dataloader.model.get_layers()[chosen_layer_index].name
        self.refwindow.boost_sample(layer_name)
        self.close()
