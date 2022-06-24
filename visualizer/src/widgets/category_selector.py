from PySide6.QtWidgets import QComboBox


class CategorySelector(QComboBox):
    def __init__(self, dataloader=None):
        QComboBox.__init__(self)

        self.dataloader = dataloader
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
        if self.categories_tuple is not None:
            for c, n in self.categories_tuple:
                self.addItem(f"{c} - {n}")

    def set_categories(self, categories):
        self.categories = categories
        self.clear()
        self.populate_selector()

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        self.categories_tuple = self.dataloader.get_popular_categories(thresh=200) #Will be dynamic
        self.populate_selector()