from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel


class ChangeSampleFooterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.dataloader = None
        self.category = None
        self.sample = None

        self.is_filtered_pvalue = False

        self.main_layout = QHBoxLayout()

        self.label_true = QLabel("true:")
        self.label_pred = QLabel("pred:")

        self.label_similarity = QLabel("avg similarity:")

        self.btn_next_sample = QPushButton("Next")
        self.btn_next_sample.clicked.connect(self.display_next_sample)

        self.main_layout.addWidget(self.label_true)
        self.main_layout.addWidget(self.label_pred)
        self.main_layout.addWidget(self.label_similarity)
        self.main_layout.addWidget(self.btn_next_sample)

        self.setLayout(self.main_layout)

    def display_next_sample(self):
        self.parent().display_next_sample()

    def set_sample(self, sample):
        """
        Set the sample to the class and update info about preds and real
        :param sample: a df of 1 row with the sample
        :return: None
        """
        self.sample = sample
        self.parent().set_sample(self.sample)

        if self.sample is not None:

            self.label_true.setText(f"true : {str(sample.true[0])}")
            self.label_pred.setText(f"pred : {str(sample.pred[0])}")
            if self.label_true.text().split(':')[-1] == self.label_pred.text().split(':')[-1]:
                self.label_pred.setObjectName('good_pred_label')
                self.label_pred.setStyleSheet('QLabel#good_pred_label {color: green}')
            else:
                self.label_pred.setObjectName('bad_pred_label')
                self.label_pred.setStyleSheet('QLabel#bad_pred_label {color: red}')

            avg_similarity = self.parent().get_avg_similarity()
            self.label_similarity.setText(f"avg similarity: {str(round(avg_similarity, 2))}")