from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel

from src.widgets.dialogs.choose_layer_popup import ChooseLayerPopup


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

        self.btn_misclassified_sample = QPushButton('Load misclassified sample')
        self.btn_misclassified_sample.clicked.connect(self.load_misclassified_sample)

        self.btn_boost = QPushButton('Boost')
        self.btn_boost.clicked.connect(self.boost_sample) #self.choose_layer

        self.btn_next_sample = QPushButton("Next")
        self.btn_next_sample.clicked.connect(self.display_next_sample)

        self.main_layout.addWidget(self.label_true)
        self.main_layout.addWidget(self.label_pred)
        self.main_layout.addWidget(self.btn_misclassified_sample)
        self.main_layout.addWidget(self.btn_next_sample)

        self.setLayout(self.main_layout)

    def load_misclassified_sample(self):
        self.parent().display_misclassified_sample()

    def display_next_sample(self):
        self.parent().display_next_sample()

    def choose_layer(self):
        """
        Display a popup for the user to select the layer.
        Then, redirects the user to the sample boosting window
        :return: None
        """
        # Open the popup
        clp = ChooseLayerPopup(self, self.parent().dataloader)#need to get a proper dataloader attribute in this class
        clp.exec()

    def boost_sample(self):
        """
        Go to the boost window by passing the sample to it.
        :return:
        """
        self.parent().go_to_boost(self.sample)


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
                self.btn_boost.setParent(None)
            else:
                self.label_pred.setObjectName('bad_pred_label')
                self.label_pred.setStyleSheet('QLabel#bad_pred_label {color: red}')
                self.main_layout.addWidget(self.btn_boost)