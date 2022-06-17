from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox


class BBCheckBoxWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.go_to_home)

        self.checkbox_pv = QCheckBox("P-values")
        self.checkbox_pv.stateChanged.connect(self.filter_pvalue)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.btn_home)
        self.main_layout.addWidget(self.checkbox_pv)

        self.setLayout(self.main_layout)

    def go_to_home(self):
        self.parent().go_to_home()

    def filter_pvalue(self):
        print(f"Filter p-value: {self.checkbox_pv.isChecked()}")