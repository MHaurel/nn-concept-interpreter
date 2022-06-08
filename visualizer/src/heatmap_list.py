from PySide6.QtWidgets import \
    (QListView, QListWidget, QListWidgetItem, QLabel)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from heatmap import Heatmap


class HeatmapList(QListWidget):
    def __init__(self, data=None):
        QListWidget.__init__(self)

        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(512, 512))

        self.data = data

        for i, h in enumerate(data):
            heatmap = Heatmap(h, i)

            item = QListWidgetItem()
            icon = QIcon()
            icon.addPixmap(heatmap.get_pixmap())
            item.setIcon(icon)
            self.addItem(item)

    def update(self, data):
        pass