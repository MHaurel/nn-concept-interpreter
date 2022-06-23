from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication

from visualizer.src.widgets.heatmaps_category_widget import HeatmapsCategoryWidget
from visualizer.src.widgets.comparison_category_widget import ComparisonCategoryWidget


class ExploreCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QHBoxLayout()
        #size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.category = None
        self.dataloader = None

        # Widget Heatmaps and back button (Left layout)
        self.heatmaps_category_widget = HeatmapsCategoryWidget()
        #self.heatmaps_category_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.heatmaps_category_widget)

        # Widget Sample (Right layout)
        self.comparison_category_widget = ComparisonCategoryWidget()
        #self.heatmaps_category_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.comparison_category_widget)


        #self.sizePolicy().setHeightForWidth(True)

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
        self.comparison_category_widget.set_dataloader(self.dataloader)

    def go_to_home(self):
        """
        Back to home
        :return: None
        """
        self.parent().goto("home", None, None)

