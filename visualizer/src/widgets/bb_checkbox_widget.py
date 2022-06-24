from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox, QLineEdit


class BBCheckBoxWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.thresh = 200 # Fetch it from dataloader

        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.go_to_home)

        self.checkbox_pv = QCheckBox("P-values")
        self.checkbox_pv.stateChanged.connect(self.filter_pvalue)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.btn_home)
        self.main_layout.addWidget(self.checkbox_pv)

        self.setLayout(self.main_layout)

    def go_to_home(self):
        """
        Call the parent function go_to_home() to change the window and show the home window
        :return: None
        """
        self.parent().go_to_home()

    def filter_pvalue(self):
        """
        When checkbox checked, change the heatmaps to be the pvalue instead of the difference of activations.
        On the opposite, when unchecked, show the heatmaps of the difference of activations
        :return: None
        """
        print(self.parent())
        self.parent().update_heatmap_list_with_pv(self.checkbox_pv.isChecked())
        print(f"Filter p-value: {self.checkbox_pv.isChecked()}")

