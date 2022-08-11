from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from src.widgets.category_selector import CategorySelector
from src.widgets.heatmap_list import HeatmapList


class ComparisonCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.category = None
        self.dataloader = None

        self.is_filtered_pvalue = False

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

    def get_category(self):
        """
        Returns the category of the class
        :return: the current category
        """
        return self.category

    def set_dataloader(self, dataloader):
        """
        Update the dataloader in this class and in child elements.
        :param dataloader: The dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.category_selector.set_dataloader(self.dataloader)

    def set_filtered_pvalue(self, is_filtered_pvalue):
        """
        Update boolean value
        :param is_filtered_pvalue: the new bool value to set
        :return: None
        """
        self.is_filtered_pvalue = is_filtered_pvalue

    def update_heatmap_list(self, paths):
        """
        Update the heatmap list of the widget with new heatmaps which paths are contained in paths.
        :param paths: The paths of the new heatmaps to update
        :return: None
        """
        self.heatmap_list.update(paths)

    def update_heatmap_list_with_category(self, category):
        """
        Updates the heatmaps list with a category
        :param category: The category for which we iupdate the heatmap list
        :return: None
        """
        self.category = category
        if self.dataloader is not None:
            if self.is_filtered_pvalue:
                self.heatmap_list.update(self.dataloader.get_pv_heatmaps_for_cat(category))
            else:
                self.heatmap_list.update(self.dataloader.get_diff_heatmaps_for_cat(category))

            self.parent().update_avg_similarity()
            self.parent().update_similarities(with_pv=self.is_filtered_pvalue)
