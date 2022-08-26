from PySide6.QtWidgets import QPushButton, QLabel, QMessageBox, QWidget, QHBoxLayout


class SampleLoaderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()

        self.label = QLabel('Do you want to load all the samples ?')

        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.load_all_samples)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_ok)

        self.setLayout(self.main_layout)

    def load_all_samples(self):
        self.parent().load_all_samples()