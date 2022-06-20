from PySide6.QtWidgets import QWidget, QHBoxLayout

from visualizer.src.widgets.heatmaps_category_widget import HeatmapsCategoryWidget
from visualizer.src.widgets.sample_category_widget import SampleCategoryWidget


class ExploreCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QHBoxLayout()

        self.category = None
        self.dataloader = None

        # Widget Heatmaps and back button (Left layout)
        self.heatmaps_category_widget = HeatmapsCategoryWidget()
        self.main_layout.addWidget(self.heatmaps_category_widget)

        # Widget Sample (Right layout)
        self.sample_category_widget = SampleCategoryWidget()
        self.main_layout.addWidget(self.sample_category_widget)

        self.setLayout(self.main_layout)

    def set_category(self, category):
        """
        Set the category variable to HeatmapCategoryWidget
        :param category: The category to set to the widget
        :return: None
        """
        self.category = category
        self.heatmaps_category_widget.set_category(self.category)

    def set_dataloader(self, dataloader):
        """
        Set the dataloader variable to HeatmapCategoryWidget
        :param dataloader: The dataloader to set to the widget
        :return: None
        """
        self.dataloader = dataloader
        self.heatmaps_category_widget.set_dataloader(self.dataloader)

    def go_to_home(self):
        """
        Back to home
        :return: None
        """
        self.parent().goto("home", None, None)