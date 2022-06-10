from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QMouseEvent


class SidebarTile(QWidget):
    def __init__(self, label):
        QWidget.__init__(self)

        # Label
        self.label = QLabel(label)

        # Icon
        self.icon = QPixmap('../img/model_ill.png')
        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.icon)

        # Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.label)

        self.setLayout(self.main_layout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f"Mouse event : {event}")