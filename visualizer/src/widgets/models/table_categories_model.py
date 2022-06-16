from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL
from PySide6.QtWidgets import QCheckBox
from PySide6 import QtCore
import operator


class TableCategoriesModel(QAbstractTableModel):
    def __init__(self, parent, list, header, categories=None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.header = header
        self.categories = categories

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return self.categories[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.list[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.EditRole:
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.list[index.row()][index.column()]