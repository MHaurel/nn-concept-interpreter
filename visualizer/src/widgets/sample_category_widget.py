from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QListWidget, \
    QSizePolicy


class SampleCategoryWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.checkBox = QCheckBox("Check")
        self.main_layout.addWidget(self.checkBox)

        size.setVerticalStretch(4)
        self.list_widget = QListWidget()
        self.list_widget.setSizePolicy(size)
        self.main_layout.addWidget(self.list_widget)

        self.setLayout(self.main_layout)