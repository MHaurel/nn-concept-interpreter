from PySide6.QtWidgets import QWidget, QListView, QHBoxLayout, QSizePolicy, QListWidget
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QPainter

from categories_list import CategoriesList
from heatmap_list import HeatmapList


class DataWidget(QWidget):
    def __init__(self, data_cat, data):
        QWidget.__init__(self)

        # Creating a QListWidget
        self.list_widget = CategoriesList(data=data_cat)
        self.list_widget.clicked.connect(self.clicked)

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        # Creating QListView to display heatmaps
        self.list_view = HeatmapList(data)

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
        self.list_view.setSizePolicy(size)
        self.main_layout.addWidget(self.list_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        
    def clicked(self, qmodelindex):
        item = self.list_widget.currentItem()
        print(item.text())