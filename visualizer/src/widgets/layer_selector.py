from PySide6.QtWidgets import QComboBox


class LayerSelector(QComboBox):
    def __init__(self, dataloader):
        QComboBox.__init__(self)

        self.dataloader = dataloader

        self.layers = [
            'embedding',
            'lstm_3',
            'dense'
        ]

        self.populate_box()

        self.currentIndexChanged.connect(self.on_item_changed)

    def on_item_changed(self, value):
        """
        Accessing CategoriesWidget to modify the heatmaps on screen
        :param value: The value of the element selected
        :return: Nothing
        """
        self.parent().parent().updateHeatmapList(qmodelindex=None)

    def populate_box(self):
        for layer in self.layers:
            self.addItem(layer)