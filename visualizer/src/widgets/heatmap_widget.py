from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from visualizer.src.widgets.layer_selector import LayerSelector
from visualizer.src.widgets.heatmap_list import HeatmapList


class HeatmapWidget(QWidget):
    def __init__(self, dataloader):
        QWidget.__init__(self)

        self.dataloader = dataloader

        self.main_layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Layer Selector
        self.layer_selector = LayerSelector(self.dataloader)
        self.main_layout.addWidget(self.layer_selector)

        # Heatmap List
        size.setVerticalStretch(4)
        self.heatmap_list = HeatmapList(paths=None)
        self.main_layout.addWidget(self.heatmap_list)

        self.setLayout(self.main_layout)

    def update(self, paths):
        self.heatmap_list.update(paths)

    def get_selected_layer(self):
        return self.layer_selector.currentText()