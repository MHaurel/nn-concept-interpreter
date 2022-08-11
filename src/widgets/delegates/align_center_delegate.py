from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt


class AlignCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        """
        Overrides the inherited function to center text in the grid
        :param option: the inherited option parameter
        :param index: the inherited index parameter
        :return: None
        """
        super(AlignCenterDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter