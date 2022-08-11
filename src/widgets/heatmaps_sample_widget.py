from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.widgets.heatmap_list import HeatmapList
from src.widgets.bb_checkbox_widget import BBCheckBoxWidget
from src.widgets.category_selector import CategorySelector
from src.widgets.change_sample_footer_widget import ChangeSampleFooterWidget


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

        self.setMaximumWidth(self.screen().geometry().width() * 0.5)

        self.setLayout(self.main_layout)

    def get_category(self):
        """
        Returns the category
        :return: the category
        """
        return self.category

    def get_index(self):
        """
        Returns the index of the sample
        :return: the index of the sample
        """
        return self.sample_index

    def set_dataloader(self, dataloader):
        """
        Updates dataloader in this class and in child elements.
        :param dataloader: the dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.category_selector.set_dataloader(self.dataloader)

    def set_filtered_pvalue(self, is_filtered_pvalue):
        """
        Updates the p-value-filter boolean value
        :param is_filtered_pvalue: the new boolean value to assign
        :return: None
        """
        self.is_filtered_pvalue = is_filtered_pvalue

    def set_sample(self, sample):
        """
        Updates sample in this class and in the parent element.
        :param sample: the sample to set
        :return: None
        """
        self.sample = sample
        self.parent().set_sample(self.sample)

    def update_heatmap_list(self, paths):
        """
        Updates the heatmaps of the heatmap list
        :param paths: the paths of the heatmaps
        :return: None
        """
        self.paths_dict = paths
        self.heatmap_list.update(paths)

    def update_heatmap_list_with_category(self, category, same=False, misclassified=False):
        """
        Update heatmap list with another category
        :param category: the category of tne next sample to display
        :param same: whether we want the same category
        :param misclassified: whether we want a misclassified sample
        :return: None
        """
        if category != self.category or same:
            self.sample_index, self.sample = None, None
        self.category = category
        comparison_category = self.parent().get_comparison_category()
        if self.dataloader is not None:
            if self.is_filtered_pvalue:

                # Get a sample from category with pvalue filter
                self.sample, paths = self.dataloader. \
                    get_pv_heatmaps_sample_for_cat(category, comparison_category=comparison_category,
                                                   index=None, misclassified=misclassified)
                self.heatmap_list.update(paths)

            else:
                # Get a sample from category without pvalue filter
                self.sample, paths = self.dataloader. \
                    get_diff_heatmaps_sample_for_cat(category, comparison_category=comparison_category,
                                                     index=None, misclassified=misclassified)
                self.heatmap_list.update(paths)

            self.sample_index = self.sample.index[0]
            self.label_sample_index.setText(self.sample_index)
            self.change_sample_footer_widget.set_sample(self.sample)

    def display_misclassified_sample(self):
        """
        Update heatmap list with a misclassified sample
        :return: None
        """
        self.update_heatmap_list_with_category(self.category, same=False, misclassified=True)

    def display_next_sample(self):
        """
        Update heatmap list with next sample
        :return: None
        """
        self.update_heatmap_list_with_category(self.category, same=True)

    def update_heatmap_list_with_pv(self, with_pv):
        """
        Update heatmap list with pvalue-filter heatmaps
        :param with_pv: whether we want to filter by pvalue
        :return: None
        """
        self.parent().update_both_lists(self.sample_index, with_pv)

    def get_avg_similarity(self):
        """
        Computer the average similarity among the heatmap displayed
        :return: the average similarity
        """
        sims = self.parent().get_similarities()

        avg_sim = round(sum([sims[sim] for sim in sims]) / len(sims), 2)

        return avg_sim

    def update_avg_similarity(self):
        """
        Updates the average similarity in the footer
        :return: None
        """
        self.change_sample_footer_widget.set_sample(self.sample)

    def go_to_home(self):
        """
        Go to home page
        :return: None
        """
        self.sample_index = None
        self.parent().go_to_home()

    def go_to_boost(self, sample):
        """
        Go to boost page passing the sample and the category
        :param sample: the sample for which we want to go to the boost page
        :return: None
        """
        self.parent().go_to_boost(sample, self.category)
