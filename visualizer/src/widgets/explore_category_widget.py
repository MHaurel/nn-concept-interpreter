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

    def update_both_lists(self, with_pv=False):
        """
        Update both lists with pvalue heatmaps if checked, differences heatmaps else.
        :param with_pv: If true will pass pvalue heatmaps paths to lists
        :return: None
        """
        heatmaps_category = self.heatmaps_category_widget.get_category()
        comparison_category = self.comparison_category_widget.get_category()

        print(f"Category of heatmaps_category is {heatmaps_category}")
        print(f"Category of comparison_category is {comparison_category}")

        if with_pv:
            paths_heatmaps_category = self.dataloader.get_pv_heatmaps_for_cat(heatmaps_category)
            paths_comparison_category = self.dataloader.get_pv_heatmaps_for_cat(comparison_category)
            self.heatmaps_category_widget.set_filtered_pvalue(True)
            self.comparison_category_widget.set_filtered_pvalue(True)
        else:
            paths_heatmaps_category = self.dataloader.get_diff_heatmaps_for_cat(heatmaps_category)
            paths_comparison_category = self.dataloader.get_diff_heatmaps_for_cat(comparison_category)
            self.heatmaps_category_widget.set_filtered_pvalue(False)
            self.comparison_category_widget.set_filtered_pvalue(False)

        self.heatmaps_category_widget.update_heatmap_list(paths_heatmaps_category)
        self.comparison_category_widget.update_heatmap_list(paths_comparison_category)

