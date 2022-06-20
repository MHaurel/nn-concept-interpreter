from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QSizePolicy

from visualizer.src.widgets.heatmap_list import HeatmapList
from visualizer.src.widgets.bb_checkbox_widget import BBCheckBoxWidget


class HeatmapsCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.category = None
        self.dataloader = None

        # Size
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Back to Home button and checkbox for p-value filter
        self.bb_checkbox_widget = BBCheckBoxWidget()

        # Heatmaps
        size.setVerticalStretch(4)
        self.heatmap_list = HeatmapList(paths_dict=None)

        # Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.bb_checkbox_widget)
        self.main_layout.addWidget(self.heatmap_list)

        self.setLayout(self.main_layout)

    def set_category(self, category):
        """
        Set the category in parameter to this class
        :param category: The category to set
        :return: None
        """
        self.category = category
        self.fetch_heatmaps()

    def set_dataloader(self, dataloader):
        """
        Set the dataloader in parameter to this class
        :param dataloader: The dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.fetch_heatmaps()

    def fetch_heatmaps(self):
        """
        Get the dict of heatmaps if self.category and self.dataloader are not equal to None
        :return: None
        """
        if self.category is not None and self.dataloader is not None:
            # Fetch heatmaps for this category through dataloader
            paths = self.dataloader.get_heatmaps_for_cat(self.category)
            print(paths)
            self.heatmap_list.update(paths)

    def go_to_home(self):
        """
        Go back home
        :return: None
        """
        self.parent().go_to_home()