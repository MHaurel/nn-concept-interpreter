from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QXYLegendMarker

from visualizer.src.backend.sample_booster import SampleBooster
from visualizer.src.utils.utils import clean_s


class BoostChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.sample = None
        self.category = None
        self.sample_booster = None
        self.layer_index = None

        # Series for the sample
        self.sample_series = QLineSeries()
        self.sample_series.append(0, 6)
        self.sample_series.append(2, 4)
        self.sample_series.append(3, 8)
        self.sample_series.append(7, 4)
        self.sample_series.append(10, 5)

        # Series for the mean of the category
        self.category_series = QLineSeries()
        self.category_series.append(0, 2)
        self.category_series.append(2, 6)
        self.category_series.append(3, 1)
        self.category_series.append(7, 3)
        self.category_series.append(10, 8)

        # Chart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Legend
        markers = self.chart.legend().markers()
        #QLegendMarker


        self.chart.addSeries(self.sample_series)
        self.chart.addSeries(self.category_series)

        self.chart.createDefaultAxes()
        self.chart.setTitle("sample {sample_index} vs concept {category}")

        # Chart view
        self.chart_view = QChartView(self.chart)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.chart_view)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def set_sample(self, sample):
        self.sample = sample
        self.sample_series.setName(clean_s(self.sample.index[0]))
        self.update_title(self.sample, self.category)

    def set_layer(self, layer_index):
        self.layer_index = layer_index

    def set_category(self, category):
        self.category = category
        self.category_series.setName(clean_s(self.category))
        self.update_title(self.sample, self.category)

    def update_title(self, sample, category):
        if sample is not None and category is not None:
            sample_index = clean_s(sample.index[0])
            category = clean_s(category)
            self.chart.setTitle(f"sample {sample_index} vs concept {category}")