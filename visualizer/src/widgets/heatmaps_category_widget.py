from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QSizePolicy

from visualizer.src.widgets.heatmap_list import HeatmapList
from visualizer.src.widgets.bb_checkbox_widget import BBCheckBoxWidget


class HeatmapsCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.category = None
        self.dataloader = None

        self.is_filtered_pvalue = False

        # Back to Home button and checkbox for p-value filter
        self.bb_checkbox_widget = BBCheckBoxWidget()

        # Heatmaps
        self.heatmap_list = HeatmapList(paths_dict=None)

        # Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.bb_checkbox_widget)
        self.main_layout.addWidget(self.heatmap_list)

        self.setMaximumWidth(self.screen().geometry().width()*0.5)

        self.setLayout(self.main_layout)

    def get_category(self):
        return self.category

    def set_category(self, category):
        """
        Set the category in parameter to this class
        :param category: The category to set
        :return: None
        """
        self.category = category
        self.init_heatmaps()

    def set_dataloader(self, dataloader):
        """
        Set the dataloader in parameter to this class
        :param dataloader: The dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.init_heatmaps()

    def init_heatmaps(self):
        """
        Get the dict of heatmaps if self.category and self.dataloader are not equal to None
        :return: None
        """
        if self.category is not None and self.dataloader is not None:
            # Fetch heatmaps for this category through dataloader
            if self.is_filtered_pvalue:
                paths = self.dataloader.get_pv_heatmaps_for_cat(self.category)
            else:
                paths = self.dataloader.get_diff_heatmaps_for_cat(self.category)
            self.heatmap_list.update(paths)

    def update_heatmap_list(self, paths):
        print(paths)
        self.heatmap_list.update(paths)

    def go_to_home(self):
        """
        Go back home
        :return: None
        """
        self.parent().go_to_home()

    def update_heatmap_list_with_pv(self, with_pv):
        """

        :param with_pv:
        :return:
        """
        self.parent().update_both_lists(with_pv)

    def set_filtered_pvalue(self, is_filtered_pvalue):
        self.is_filtered_pvalue = is_filtered_pvalue

