from PySide6.QtWidgets import QWidget, QHBoxLayout

from src.widgets.heatmaps_sample_widget import HeatmapsSampleWidget
from src.widgets.comparison_category_widget import ComparisonCategoryWidget


class SampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.sample = None
        self.index = None

        # Left widget (sample)
        self.heatmaps_sample = HeatmapsSampleWidget()

        # Right widget (category)
        self.comparison_category_widget = ComparisonCategoryWidget()

        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.heatmaps_sample)
        self.main_layout.addWidget(self.comparison_category_widget)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        # must be initialized in this order, otherwise the category won't be loaded
        # and the similarties will be nan
        self.comparison_category_widget.set_dataloader(self.dataloader)
        self.heatmaps_sample.set_dataloader(self.dataloader)

    def set_sample(self, sample):
        self.sample = sample

    def update_both_lists(self, index, with_pv=False):
        """
        Update both lists with pvalue heatmaps if checked, differences heatmaps else.
        :param index:
        :param with_pv: If true will pass pvalue heatmaps paths to lists
        :return: None
        """

        heatmaps_category = self.heatmaps_sample.get_category()
        comparison_category = self.comparison_category_widget.get_category()

        if with_pv:
            self.sample, paths_heatmaps_sample = self.dataloader\
                .get_pv_heatmaps_sample_for_cat(heatmaps_category, comparison_category, index)

            paths_comparison_category = self.dataloader.get_pv_heatmaps_for_cat(comparison_category)
            self.heatmaps_sample.set_filtered_pvalue(True)
            self.comparison_category_widget.set_filtered_pvalue(True)
        else:
            self.sample, paths_heatmaps_sample = self.dataloader\
                .get_diff_heatmaps_sample_for_cat(heatmaps_category, comparison_category, index)

            paths_comparison_category = self.dataloader.get_diff_heatmaps_for_cat(comparison_category)
            self.heatmaps_sample.set_filtered_pvalue(False)
            self.comparison_category_widget.set_filtered_pvalue(False)

        self.heatmaps_sample.update_heatmap_list(paths_heatmaps_sample)

        self.comparison_category_widget.update_heatmap_list(paths_comparison_category)

    def get_similarities(self):
        """
        Get the similarities between sample and concept
        :return: similarities in the shape of a dict
        """
        category = self.comparison_category_widget.get_category()
        sims = self.dataloader.get_similarities_sample_cat(self.sample, category)

        return sims

    def update_similarities(self, with_pv):
        """
        Update similarities with pvalue filter or not
        :param with_pv: whether we filter by pvalues
        :return: None
        """
        index = self.heatmaps_sample.get_index()
        self.update_both_lists(index=index, with_pv=with_pv) #Must deal with "with_pv" now

    def get_comparison_category(self):
        """
        Returns the category of the comparison category widget
        :return: the category of the comparison category widget
        """
        return self.comparison_category_widget.get_category()

    def update_avg_similarity(self):
        """
        Updates the average similarity
        :return: None
        """
        self.heatmaps_sample.update_avg_similarity()

    def go_to_home(self):
        """
        Asks the parent widget to go to home page.
        :return: None
        """
        self.parent().goto("home", self.dataloader)

    def go_to_boost(self, sample, category):
        """
        Asks the parend widget to go to boost page
        :param sample: the sample to boost
        :param category: the category of the sample
        :return: None
        """
        self.parent().goto('boost', self.dataloader, category, sample)