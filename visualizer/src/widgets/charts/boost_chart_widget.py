from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QXYLegendMarker
from PySide6.QtCore import QPointF

from visualizer.src.backend.sample_booster import SampleBooster
from visualizer.src.utils.utils import clean_s


class BoostChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.sample = None
        self.category = None
        self.sample_booster = None
        self.layer_index = 0 # By default

        # Chart
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.createDefaultAxes()
        self.chart.setTitle("sample {sample_index} vs concept {category}")

        # Chart view
        self.chart_view = QChartView(self.chart)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.chart_view)

        self.setLayout(self.main_layout)

    def add_series(self, elts, name):
        series = QLineSeries()
        series.setName(name)
        for i, elt in enumerate(elts):
            series.append(QPointF(i, elt))
        self.chart.addSeries(series)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def set_sample(self, sample):
        self.sample = sample

        sample_act = self.dataloader.get_activation_for_sample(sample, self.dataloader.get_dfs()[self.layer_index])
        sample_act = sample_act.to_numpy().tolist()[0]

        self.add_series(sample_act, clean_s(sample.index[0]))
        self.update_title(self.sample, self.category)

    def set_layer(self, layer_index):
        self.layer_index = layer_index

    def set_category(self, category):
        self.category = category

        category_act = self.dataloader.get_mean_activation_for_cat(self.category,
                                                                   self.dataloader.get_dfs()[self.layer_index],
                                                                   self.layer_index)
        category_act = category_act.to_numpy().tolist()[0]

        self.add_series(category_act, clean_s(self.category))
        self.update_title(self.sample, self.category)

    def update_title(self, sample, category):
        if sample is not None and category is not None:
            sample_index = clean_s(sample.index[0])
            category = clean_s(category)
            self.chart.setTitle(f"sample {sample_index} vs concept {category}")