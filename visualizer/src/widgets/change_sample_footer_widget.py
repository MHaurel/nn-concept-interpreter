from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ChangeSampleFooterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.category = None

        self.is_filtered_pvalue = False

        self.main_layout = QHBoxLayout()

        self.btn_previous_sample = QPushButton("<")
        self.btn_previous_sample.clicked.connect(self.display_previous_sample)

        self.btn_next_sample = QPushButton(">")
        self.btn_next_sample.clicked.connect(self.display_next_sample)

        self.main_layout.addWidget(self.btn_previous_sample)
        self.main_layout.addWidget(self.btn_next_sample)

        self.setLayout(self.main_layout)

    def display_previous_sample(self):
        print("Asking to display previous sample")

    def display_next_sample(self):
        print("Asking to display next sample")