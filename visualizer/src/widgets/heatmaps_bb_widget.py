from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QSizePolicy

from visualizer.src.widgets.heatmap_list import HeatmapList


class HeatmapsBBWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.category = None

        self.main_layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Back to Home button
        self.btn_back = QPushButton("Back Home")
        self.btn_back.clicked.connect(self.go_to_home)
        self.main_layout.addWidget(self.btn_back)

        # Heatmaps
        size.setVerticalStretch(4)
        self.heatmap_list = HeatmapList(paths=None)
        self.main_layout.addWidget(self.heatmap_list)

        self.setLayout(self.main_layout)

    def set_category(self, category):
        self.category = category

    def go_to_home(self):
        print(self.__class__, "Asking to go home...")
        self.parent().go_to_home()