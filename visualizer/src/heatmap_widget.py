from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from layer_selector import LayerSelector
from heatmap_list import HeatmapList


class HeatmapWidget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        self.data = data

        self.main_layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Layer Selector
        self.layer_selector = LayerSelector()
        self.main_layout.addWidget(self.layer_selector)

        # Heatmap List
        size.setVerticalStretch(4)
        self.heatmap_list = HeatmapList(self.data)
        self.main_layout.addWidget(self.heatmap_list)

        self.setLayout(self.main_layout)
