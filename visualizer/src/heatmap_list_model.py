from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from heatmap import Heatmap


class HeatmapListModel(QAbstractListModel):
    def __init__(self, data=None):
        QAbstractListModel.__init__(self)

        data_heatmaps = []
        for df in data:
            h = Heatmap(df)
            data_heatmaps.append(h.get_pixmap())

        self.load_data(data_heatmaps)

    def load_data(self, data):
        self.heatmaps = data

        self.row_count = len(self.heatmaps)
        self.column_count = 1

    def rowCount(self, parent=QModelIndex):
        return self.row_count

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return self.heatmaps[row]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None