from PySide6.QtWidgets import QWidget, QListView, QHBoxLayout, QSizePolicy
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QPainter

from categories_list_model import CategoriesListModel


class DataWidget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        self.model = CategoriesListModel(data)

        # Creating a QListView
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        # QTableView Headers ?????

        # Creating QChart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        # self.add_series("Magnitude (Column 1)", [0,1])

        # Creating QChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left Layout
        size.setHorizontalStretch(1)
        self.list_view.setSizePolicy(size)
        self.main_layout.addWidget(self.list_view)

        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)