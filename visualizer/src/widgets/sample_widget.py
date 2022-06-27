from PySide6.QtWidgets import QWidget, QHBoxLayout

from visualizer.src.widgets.heatmaps_sample_widget import HeatmapsSampleWidget
from visualizer.src.widgets.comparison_category_widget import ComparisonCategoryWidget


class SampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None

        # Left widget (sample)
        self.heatmaps_sample = HeatmapsSampleWidget()

        # Right widget (category)
        self.comparison_category = ComparisonCategoryWidget()

        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.heatmaps_sample)
        self.main_layout.addWidget(self.comparison_category)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def go_to_home(self):
        self.parent().goto("home", self.dataloader)