from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QListWidget, \
    QSizePolicy

from visualizer.src.widgets.category_selector import CategorySelector
from visualizer.src.widgets.heatmap_list import HeatmapList


class ComparisonCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.category_selector = CategorySelector()
        self.main_layout.addWidget(self.category_selector)

        size.setVerticalStretch(4)
        self.heatmap_list = HeatmapList()
        self.heatmap_list.setSizePolicy(size)
        self.main_layout.addWidget(self.heatmap_list)

        self.setMaximumWidth(self.screen().geometry().width() * 0.5)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        self.category_selector.set_dataloader(self.dataloader)

    def update_heatmap_list(self, category):
        if self.dataloader is not None:
            self.heatmap_list.update(self.dataloader.get_heatmaps_for_cat(category))