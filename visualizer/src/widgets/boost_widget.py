from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from visualizer.src.backend.sample_booster import SampleBooster
from visualizer.src.widgets.charts.boost_chart_widget import BoostChartWidget
from visualizer.src.widgets.header_boost_widget import HeaderBoostWidget


class BoostWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sample = None
        self.dataloader = None
        self.category = None
        self.sample_booster = None #SampleBooster()

        # Home button & layer combobox
        self.header_boost_widget = HeaderBoostWidget()

        # Chart widget
        self.boost_chart_widget = BoostChartWidget()

        # Boost button
        self.btn_boost = QPushButton("Boost sample")
        self.btn_boost.clicked.connect(self.boost_sample)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.header_boost_widget)
        self.main_layout.addWidget(self.boost_chart_widget)
        self.main_layout.addWidget(self.btn_boost)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader
        self.header_boost_widget.set_datalaoder(self.dataloader)
        self.boost_chart_widget.set_dataloader(self.dataloader)

    def set_sample(self, sample):
        self.sample = sample
        self.header_boost_widget.set_sample(self.sample)
        self.boost_chart_widget.set_sample(self.sample)

    def set_category(self, category):
        self.category = category
        self.header_boost_widget.set_category(self.category)
        self.boost_chart_widget.set_category(self.category)

    def boost_sample(self):
        print("Asking to boost sample")

    def go_to_home(self):
        self.parent().goto("home", self.dataloader)