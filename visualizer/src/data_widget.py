from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from categories_list import CategoriesList
from visualizer.src.widgets.heatmap_widget import HeatmapWidget


class DataWidget(QWidget):
    def __init__(self, data_cat, data):
        QWidget.__init__(self)

        # Creating a QListWidget
        self.list_widget = CategoriesList(data=data_cat)
        self.list_widget.clicked.connect(self.clicked)

        """# Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        # Creating LayerSelector
        self.layer_selector = LayerSelector()

        # Creating QListView to display heatmaps
        self.list_view = HeatmapList(data)

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)"""

        self.heatmap_widget = HeatmapWidget(data)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left Layout
        size.setHorizontalStretch(1)
        self.list_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.list_widget)

        # Adding layer selector to the layout
        #self.main_layout.addWidget(self.layer_selector)

        # Right Layout
        size.setHorizontalStretch(4)
        self.main_layout.addWidget(self.heatmap_widget)
        self.heatmap_widget.setSizePolicy(size)
        #self.list_view.setSizePolicy(size)
        #self.main_layout.addWidget(self.list_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        
    def clicked(self, qmodelindex):
        item = self.list_widget.currentItem()
        print(item.text())