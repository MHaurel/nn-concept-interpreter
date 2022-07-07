from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from visualizer.src.widgets.heatmap_list import HeatmapList
from visualizer.src.widgets.bb_checkbox_widget import BBCheckBoxWidget
from visualizer.src.widgets.category_selector import CategorySelector
from visualizer.src.widgets.change_sample_footer_widget import ChangeSampleFooterWidget


class HeatmapsSampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sample = None
        self.sample_index = None
        self.category = None
        self.dataloader = None
        self.paths_dict = None

        self.is_filtered_pvalue = False

        self.bb_checkbox = BBCheckBoxWidget()

        self.category_selector = CategorySelector()

        self.label_sample_index = QLabel('')

        self.heatmap_list = HeatmapList()

        self.change_sample_footer_widget = ChangeSampleFooterWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.bb_checkbox)
        self.main_layout.addWidget(self.category_selector)
        self.main_layout.addWidget(self.label_sample_index)
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

    def set_sample(self, sample):
        self.sample = sample
        self.parent().set_sample(self.sample)

    def update_heatmap_list(self, paths):
        self.paths_dict = paths
        self.heatmap_list.update(paths)

    def update_heatmap_list_with_category(self, category, same=False):
        """

        :param category:
        :param same:
        :return:
        """
        if category != self.category or same:
            self.sample_index, self.sample = None, None
        self.category = category
        if self.dataloader is not None:
            if self.is_filtered_pvalue:

                # Get a sample from category with pvalue filter
                self.sample, paths = self.dataloader.get_pv_heatmaps_sample_for_cat(category, self.sample_index)
                self.heatmap_list.update(paths)

            else:
                # Get a sample from category without pvalue filter
                self.sample, paths = self.dataloader.get_diff_heatmaps_sample_for_cat(category, self.sample_index)
                self.heatmap_list.update(paths)

            self.sample_index = self.sample.index[0]
            self.label_sample_index.setText(self.sample_index)
            self.change_sample_footer_widget.set_sample(self.sample)

    def display_next_sample(self):
        print("Asking to display next sample")
        self.update_heatmap_list_with_category(self.category, same=True)
        #self.parent().update_both_lists(index=None, with_pv=self.is_filtered_pvalue)

    def update_heatmap_list_with_pv(self, with_pv):
        """

        :param with_pv:
        :return:
        """
        self.parent().update_both_lists(self.sample_index, with_pv)

    def get_avg_similarity(self):
        sims = self.parent().get_similarities()

        avg_sim = round(sum([sims[sim] for sim in sims]) / len(sims), 2)

        return avg_sim

    def update_avg_similarity(self):
        self.change_sample_footer_widget.set_sample(self.sample)

    def go_to_home(self):
        self.sample_index = None
        self.parent().go_to_home()