from PySide6.QtWidgets import \
    QWidget, QHBoxLayout, QSizePolicy, QPushButton

from visualizer.src.widgets.categories_list import CategoriesList
from visualizer.src.widgets.heatmap_list import HeatmapList
from visualizer.src.widgets.sidebar import Sidebar


class CategoriesWidget(QWidget):
    def __init__(self, data_cat, data):
        QWidget.__init__(self)

        self.model = None
        self.data_path = None
        self.data = None

        # Creating a QListWidget
        self.list_widget = CategoriesList(data=data_cat)
        self.list_widget.clicked.connect(self.updateHeatmapList)

        # Creating QListView to display heatmaps
        self.list_view = HeatmapList(data)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # Left Layout
        size.setHorizontalStretch(1)
        self.list_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.list_widget)

        # Right Layout
        size.setHorizontalStretch(4)
        self.list_view.setSizePolicy(size)
        self.main_layout.addWidget(self.list_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def updateHeatmapList(self, qmodelindex):
        item = self.list_widget.currentItem()
        print(f"Updating heatmap list widget with category: {item.text()}")

    # These functions may need to be implemented in an abstract function
    # and pages window to override them
    def goToHome(self):
        self.parent().goto("home", self.model, self.data_path)

    def goToSample(self):
        self.parent().goto("sample", self.model, self.data_path)

    def goToCategories(self):
        pass  # Because already on this page