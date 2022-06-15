from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import Qt


class AlignCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenterDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter