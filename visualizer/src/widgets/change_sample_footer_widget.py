from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel


class ChangeSampleFooterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.category = None
        self.sample = None

        self.is_filtered_pvalue = False

        self.main_layout = QHBoxLayout()

        self.btn_previous_sample = QPushButton("<")
        self.btn_previous_sample.clicked.connect(self.display_previous_sample)

        self.label_true = QLabel("true:")
        self.label_pred = QLabel("pred:")

        self.label_similarity = QLabel("similarity:")

        self.btn_next_sample = QPushButton(">")
        self.btn_next_sample.clicked.connect(self.display_next_sample)

        self.main_layout.addWidget(self.btn_previous_sample)
        self.main_layout.addWidget(self.label_true)
        self.main_layout.addWidget(self.label_pred)
        self.main_layout.addWidget(self.label_similarity)
        self.main_layout.addWidget(self.btn_next_sample)

        self.setLayout(self.main_layout)

    def display_previous_sample(self):
        print("Asking to display previous sample")

    def display_next_sample(self):
        print("Asking to display next sample")

    def set_sample(self, sample):
        """
        Set the sample to the class and update info about preds and real
        :param sample: a df of 1 row with the sample
        :return: None
        """
        self.sample = sample

        self.label_true.setText(f"true : {str(sample.true[0])}")
        self.label_pred.setText(f"pred : {str(sample.pred[0])}")
        if self.label_true.text().split(':')[-1] == self.label_pred.text().split(':')[-1]:
            self.label_pred.setObjectName('good_pred_label')
            self.label_pred.setStyleSheet('QLabel#good_pred_label {color: green}')
        else:
            self.label_pred.setObjectName('bad_pred_label')
            self.label_pred.setStyleSheet('QLabel#bad_pred_label {color: red}')