import pandas as pd
import numpy as np

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChartView, QChart, QLineSeries, QXYLegendMarker
from PySide6.QtCore import QPointF

from keras.layers import Embedding

from src.backend.sample_booster import SampleBooster
from src.utils.utils import clean_s


class BoostChartWidget(QWidget):
    def __init__(self, layer_index=0):
        super().__init__()

        self.dataloader = None
        self.sample = None
        self.category = None
        self.sample_booster = None
        self.layer_index = layer_index

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
        """
        Add a series to the chart
        :param elts: the elements of which the series is composed
        :param name: the name of this series
        :return: None
        """
        for x in self.chart.series():
            if x.name() == name:
                self.chart.removeSeries(x)
        series = QLineSeries()
        series.setName(name)
        for i, elt in enumerate(elts):
            series.append(QPointF(i, elt))
        self.chart.addSeries(series)

    def set_dataloader(self, dataloader):
        """
        Updates the dataloader in this class
        :param dataloader: the dataloader to set
        :return: None
        """
        if dataloader is not None:
            self.dataloader = dataloader

    def set_sample(self, sample):
        """
        Updates the sample in this class. Also add series for it
        :param sample: the sample to set
        :return: None
        """
        if sample is not None:
            self.sample = sample

            sample_act = self.dataloader.get_activation_for_sample(sample, self.dataloader.get_dfs()[self.layer_index])
            sample_act = sample_act.to_numpy().tolist()[0]

            # When the layer is an Embedding one
            if isinstance(self.dataloader.model.get_layers()[self.layer_index], Embedding):
                output_dim = self.dataloader.model.get_layers()[self.layer_index].output_shape[-1]
                arr = np.array(sample_act).reshape(-1, output_dim)
                sample_act = self.dataloader.get_mean_df_per_neuron(pd.DataFrame(arr))
                sample_act = sample_act.to_numpy().tolist()[0]

            self.add_series(sample_act, clean_s(sample.index[0]))
            self.update_title(self.sample, self.category)

    def set_layer(self, layer_index):
        """
        Updates the current layer for which data is displayed
        :param layer_index: the index of the new layer to display the data for
        :return: None
        """
        self.layer_index = layer_index

    def set_category(self, category):
        """
        Updates the category in this class and reload data according to it.
        :param category: The category to set
        :return: None
        """
        if category is not None:
            self.category = category

            category_act = self.dataloader.get_mean_activation_for_cat(self.category,
                                                                       self.dataloader.get_dfs()[self.layer_index],
                                                                       self.layer_index)
            category_act = category_act.to_numpy().tolist()[0]

            self.add_series(category_act, clean_s(self.category))
            self.update_title(self.sample, self.category)

    def update_title(self, sample, category):
        """
        Updates the title of the chart according to the sample and the category displayed
        :param sample: The sample displayed
        :param category: The category displayed
        :return: None
        """
        if sample is not None and category is not None:
            sample_index = clean_s(sample.index[0])
            category = clean_s(category)
            self.chart.setTitle(f"sample: {sample_index} VS concept: {category}")

    def update_layer_index(self, layer_index):
        """
        Updates the layer index in this class.
        :param layer_index: the layer index to update
        :return:
        """
        self.layer_index = layer_index
        self.clear_chart()

    def clear_chart(self):
        """
        Clears the chart to display some new data
        :return: None
        """
        for series in self.chart.series():
            self.chart.removeSeries(series)
