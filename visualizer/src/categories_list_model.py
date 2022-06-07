from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtGui import QColor


class CategoriesListModel(QAbstractListModel):
    def __init__(self, data=None):
        QAbstractListModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.row_count = 50
        self.column_count = 1
        print(data)

    def rowCount(self, parent=QModelIndex):
        return self.row_count

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return f"Category: at index {row}"
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None