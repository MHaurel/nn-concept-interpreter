from PySide6.QtWidgets import QComboBox


class LayerSelector(QComboBox):
    def __init__(self):
        QComboBox.__init__(self)

        self.layers = [
            'embedding',
            'lstm_3',
            'dense'
        ]

        self.populate_box()

        self.currentIndexChanged.connect(self.on_item_changed)

    def on_item_changed(self, value):
        print(f"Current layer is : {self.layers[value]}")

    def populate_box(self):
        for layer in self.layers:
            self.addItem(layer)