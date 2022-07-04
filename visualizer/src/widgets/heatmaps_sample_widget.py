from PySide6.QtWidgets import QWidget, QVBoxLayout

from visualizer.src.widgets.heatmap_list import HeatmapList
from visualizer.src.widgets.bb_checkbox_widget import BBCheckBoxWidget
from visualizer.src.widgets.category_selector import CategorySelector
from visualizer.src.widgets.change_sample_footer_widget import ChangeSampleFooterWidget


class HeatmapsSampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sample_index = None
        self.category = None
        self.dataloader = None

        self.is_filtered_pvalue = False

        self.bb_checkbox = BBCheckBoxWidget()

        self.category_selector = CategorySelector()

        self.heatmap_list = HeatmapList()

        self.change_sample_footer_widget = ChangeSampleFooterWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.bb_checkbox)
        self.main_layout.addWidget(self.category_selector)
        self.main_layout.addWidget(self.heatmap_list)
        self.main_layout.addWidget(self.change_sample_footer_widget)

        self.setMaximumWidth(self.screen().geometry().width()*0.5)

        self.setLayout(self.main_layout)

    def get_category(self):
        return self.category

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        self.category_selector.set_dataloader(self.dataloader)

    def set_filtered_pvalue(self, is_filtered_pvalue):
        self.is_filtered_pvalue = is_filtered_pvalue

    def update_heatmap_list(self, paths):
        self.heatmap_list.update(paths)

    def update_heatmap_list_with_category(self, category):
        print(f"{category}")
        self.category = category
        if self.dataloader is not None:

            if self.is_filtered_pvalue:
                # Get a sample from category with pvalue filter
                sample_index, paths = self.dataloader.get_pv_heatmaps_sample_for_cat(category)
                self.heatmap_list.update(paths)
                self.change_sample_footer_widget.set_sample_index(self.sample_index)

            else:
                # Get a sample from category without pvalue filter
                sample_index, paths = self.dataloader.get_diff_heatmaps_sample_for_cat(category)
                self.heatmap_list.update(paths)
                self.change_sample_footer_widget.set_sample_index(self.sample_index)

    def update_heatmap_list_with_pv(self, with_pv):
        """

        :param with_pv:
        :return:
        """
        self.parent().update_both_lists(with_pv)

    def go_to_home(self):
        self.parent().go_to_home()