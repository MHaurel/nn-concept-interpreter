from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

from visualizer.src.widgets.heatmap_list import HeatmapList


class HeatmapsSampleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.go_to_home)

        self.heatmap_list = HeatmapList()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.btn_home)
        self.main_layout.addWidget(self.heatmap_list)

        self.setLayout(self.main_layout)

    def go_to_home(self):
        self.parent().go_to_home()