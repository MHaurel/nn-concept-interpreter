from PySide6.QtWidgets import QWidget, QListView, QHBoxLayout, QSizePolicy, QListWidget
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QPainter

from categories_list_model import CategoriesListModel
from categories_list import CategoriesList
from heatmap_list import HeatmapList
from heatmap_list_model import HeatmapListModel


class DataWidget(QWidget):
    def __init__(self, data_cat, data):
        QWidget.__init__(self)

        # Getting the Model
        #self.model = CategoriesListModel(data) # USELESS

        # Creating a QListWidget
        self.list_widget = CategoriesList(data=data_cat)
        # self.list_widget.itemSelectionChanged.connect(print("Changed"))  # ISSUE : print only at start
        self.list_widget.clicked.connect(self.clicked)

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        # self.add_series("Magnitude (Column 1)", [0,1])

        # Getting the model
        #self.heatmap_list_model = HeatmapListModel(data)

        # Creating QListView to display heatmaps
        self.list_view = HeatmapList(data)
        #self.list_view.setModel(model=self.heatmap_list_model)

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left Layout
        size.setHorizontalStretch(1)
        self.list_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.list_widget)

        # Right Layout
        size.setHorizontalStretch(4)
        #self.chart_view.setSizePolicy(size)
        #self.main_layout.addWidget(self.chart_view)
        self.list_view.setSizePolicy(size)
        self.main_layout.addWidget(self.list_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        
    def clicked(self, qmodelindex):
        item = self.list_widget.currentItem()
        print(item.text())