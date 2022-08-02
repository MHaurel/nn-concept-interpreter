from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout
from PySide6.QtCharts import QLineSeries, QChart, QChartView
from PySide6.QtCore import QPointF


class HistoryBoostingPopup(QDialog):
    def __init__(self, history):
        super().__init__()
        self.history = history # list of predictions over iterations

        self.setWindowTitle("Boosting history")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        # Init components
        # Chart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.createDefaultAxes()
        self.chart.setTitle("History of the predictions with boosting")

        self.fill_chart()

        # Chart View
        self.chart_view = QChartView(self.chart)

        # Button close
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close_popup)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.chart_view)
        self.main_layout.addWidget(self.btn_close)

        # Set layout
        self.setLayout(self.main_layout)

    def fill_chart(self):
        series = QLineSeries()
        series.setName('predictions')
        for i, x in enumerate(self.history):
            print(i, x)
            series.append(QPointF(i, x))
        self.chart.addSeries(series)

    def close_popup(self):
        self.close()