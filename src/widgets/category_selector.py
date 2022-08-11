from PySide6.QtWidgets import QComboBox


class CategorySelector(QComboBox):
    def __init__(self, dataloader=None):
        QComboBox.__init__(self)

        self.dataloader = dataloader
        self.categories = None
        self.categories_tuple = None

        if self.dataloader is not None:
            self.categories_tuple = dataloader.get_popular_categories(thresh=200) #Will be dynamic

        self.populate_selector()

        self.currentIndexChanged.connect(self.on_item_changed)

    def on_item_changed(self, value):
        """
        Accessing CategoriesWidget to modify the heatmaps on screen
        :param value: The value of the element selected
        :return: None
        """
        self.parent().update_heatmap_list_with_category(self.categories_tuple[value][0])

    def populate_selector(self):
        """
        Fill the selector with each layer name
        :return: None
        """
        self.clear()
        if self.categories_tuple is not None:
            for c, n in self.categories_tuple:
                self.addItem(f"{c} - {n}")

    def set_categories(self, categories):
        """
        Update the categories in the combo box.
        :param categories: The categories to update
        :return: None
        """
        self.categories = categories
        self.populate_selector()

    def set_dataloader(self, dataloader):
        """
        Update the dataloader in the class. Also populate the selector.
        :param dataloader: the dataloader to set.
        :return: None
        """
        self.dataloader = dataloader
        self.categories_tuple = self.dataloader.get_popular_categories(self.dataloader.thresh)
        self.populate_selector()