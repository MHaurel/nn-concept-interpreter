from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton


class SampleSimilarityButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()

        self.btn_sample = QPushButton("Explore samples")
        self.btn_sample.clicked.connect(self.go_to_sample)

        self.main_layout.addWidget(self.btn_sample)

        self.setLayout(self.main_layout)

    def go_to_sample(self):
        self.parent().go_to_sample()