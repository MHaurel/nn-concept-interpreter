from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton


class SampleSimilarityButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()

        self.btn_sample = QPushButton("Explore samples")
        self.btn_sample.clicked.connect(self.go_to_sample)

        self.btn_similarity = QPushButton("See similarities")
        self.btn_similarity.clicked.connect(self.go_to_similarity)

        self.main_layout.addWidget(self.btn_sample)
        self.main_layout.addWidget(self.btn_similarity)

        self.setLayout(self.main_layout)

    def go_to_sample(self):
        self.parent().go_to_sample()

    def go_to_similarity(self):
        self.parent().go_to_similarity()