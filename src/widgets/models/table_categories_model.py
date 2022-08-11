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
        """
        Overrided function setting the header data
        :param section: inherited parameter
        :param orientation: inherited parameter
        :param role: inherited parameter
        :return: The model to insert
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return self.categories[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent):
        """
        Overrided function counting the number of rows
        :param parent: inherited parameter
        :return: the number of rows
        """
        return len(self.list)

    def columnCount(self, parent):
        """
        Overrided function counting the number of columns
        :param parent: inherited parameter
        :return: the number of columns
        """
        return len(self.list[0])

    def data(self, index, role):
        """
        Overrided function
        :param index: inherited parameter
        :param role: inherited parameter
        :return: depends on the case
        """
        if not index.isValid():
            return None
        elif role == Qt.EditRole:
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.list[index.row()][index.column()]