"""PySide6 port of the linechart example from Qt v6.x"""

import sys
import json

import pandas as pd

from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow


class TestChart(QMainWindow):
    def __init__(self):
        super().__init__()

        with open('../../activations/painters_ds/popular_categories.json', 'r') as f:
            data = json.load(f)

        df = pd.DataFrame({
            'number': data,
        })
        print(df)

        self.sets = [QBarSet(x) for x in df.index]

        self.set_0 = QBarSet("France")
        self.set_1 = QBarSet("Italy")
        self.set_2 = QBarSet("Netherlands")
        self.set_3 = QBarSet("Russia")
        self.set_4 = QBarSet("United_Kingdom")
        self.set_5 = QBarSet("United_States")
        self.set_6 = QBarSet("Germany")

        self.set_0.append([512, 0, 0, 0, 0, 0, 0])
        self.set_1.append([0, 493, 0, 0, 0, 0, 0])
        self.set_2.append([0, 0, 306, 0, 0, 0, 0])
        self.set_3.append([0, 0, 0, 298, 0, 0, 0])
        self.set_4.append([0, 0, 0, 0, 607, 0, 0])
        self.set_5.append([0, 0, 0, 0, 0, 980, 0])
        self.set_6.append([0, 0, 0, 0, 0, 0, 289])

        self.series = QBarSeries()
        self.series.append(self.set_0)
        self.series.append(self.set_1)
        self.series.append(self.set_2)
        self.series.append(self.set_3)
        self.series.append(self.set_4)
        self.series.append(self.set_5)
        self.series.append(self.set_6)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Simple barchart example")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.categories = [self.clean_category(x) for x in df.index]  #["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        print(self.categories)
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.number = df.number
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, self.number.max() + 5)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)

    def clean_category(self, category):
        return category.split('/')[-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(420, 300)
    sys.exit(app.exec())