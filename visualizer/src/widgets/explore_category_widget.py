from PySide6.QtWidgets import QWidget, QHBoxLayout

from visualizer.src.widgets.heatmaps_bb_widget import HeatmapsBBWidget
from visualizer.src.widgets.sample_category_widget import SampleCategoryWidget


class ExploreCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QHBoxLayout()

        self.category = None
        self.dataloader = None

        # Widget Heatmaps and back button (Left layout)
        self.heatmaps_back_button_widget = HeatmapsBBWidget()
        self.main_layout.addWidget(self.heatmaps_back_button_widget)

        # Widget Sample (Right layout)
        self.sample_category_widget = SampleCategoryWidget()
        self.main_layout.addWidget(self.sample_category_widget)

        self.setLayout(self.main_layout)

    def set_category(self, category):
        self.category = category
        self.heatmaps_back_button_widget.set_category(self.category)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def go_to_home(self):
        print(self.__class__, "go_to_home")
        self.parent().goto("home", None, None)