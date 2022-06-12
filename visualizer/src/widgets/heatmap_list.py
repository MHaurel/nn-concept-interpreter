from PySide6.QtWidgets import \
    (QListView, QListWidget, QListWidgetItem, QLabel)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from visualizer.src.widgets.heatmap import Heatmap


class HeatmapList(QListWidget):
    def __init__(self, paths=None):
        QListWidget.__init__(self)

        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(512, 512))

        self.paths = paths

        if self.paths is not None:
            self.populate_list(self.paths)

    def populate_list(self, paths):
        for path in paths:
            try:
                heatmap = Heatmap(path)
                item = QListWidgetItem()
                icon = QIcon()
                icon.addPixmap(heatmap.get_pixmap())
                item.setIcon(icon)
                self.addItem(item)
            except:
                print("Error encountered with heatmap loading")

    def update(self, paths):
        self.clear()
        self.populate_list(paths)
