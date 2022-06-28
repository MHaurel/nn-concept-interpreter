"""PySide6 port of the linechart example from Qt v6.x"""

import sys
import json

import pandas as pd

from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QApplication, QMainWindow


class TestChart(QMainWindow):
    def __init__(self):
        super().__init__()

        with open('../../activations/painters_ds/popular_categories.json', 'r') as f:
            data = json.load(f)

        df = pd.DataFrame({
            'number': data,
        })

        self.categories = [self.clean_category(x) for x in df.index]
        self.number = df.number
        self.data_list = []
        for i in range(len(self.categories)):
            l = (self.categories[i], self.number[i])
            self.data_list.append(l)
        print(self.data_list)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)

        font = QFont()
        font.setPixelSize(20)
        self.chart.setTitleFont(font)
        self.chart.setTitle("Categories repartition")

        # data to series and put to chart
        cases_max = []
        i = 0

        for data in self.data_list:
            series = QBarSeries()
            curr_set = "set" + str(i)
            curr_set = QBarSet(str(data[0]))
            print(data[0])
            curr_set << int(data[1])
            print(data[1])
            series.append(curr_set)
            series.setLabelsVisible(True)
            series.labelsPosition()
            self.chart.addSeries(series)
            cases_max.append(int(data[1]))

            i += 1

        # create axis
        self.axisX = QBarCategoryAxis()
        self.axisX.setLabelsVisible(True)
        self.axisX.append(self.categories)

        self.axisY = QValueAxis()
        self.axisY.setLabelsVisible(True)
        self.axisY.setMin(0)
        self.axisY.setMax(max(self.number))
        self.axisY.setLabelFormat("%.0f")
        self.axisY.setTitleText("Samples")

        # bild the chart
        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.axisX)
        self.chart.setAxisY(self.axisY)

        # create view
        self.chartview = QChartView(self.chart)

        # put view to qt grid layout
        self.setCentralWidget(self.chartview)

    def clean_category(self, category):
        return category.split('/')[-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(420, 300)
    sys.exit(app.exec())