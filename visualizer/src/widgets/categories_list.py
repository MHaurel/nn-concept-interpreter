from PySide6.QtWidgets import QListWidget


class CategoriesList(QListWidget):
    def __init__(self, data):
        QListWidget.__init__(self)

        self.data = data
        for i, rowName in enumerate(data):
            self.insertItem(i, rowName)