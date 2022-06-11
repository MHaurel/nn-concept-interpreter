from PySide6.QtWidgets import QListWidget


class CategoriesList(QListWidget):
    def __init__(self, data):
        QListWidget.__init__(self)

        self.data = data

        if data is not None:
            for i, rowName in enumerate(data):
                self.insertItem(i, rowName[0])

    def update(self, data=None):
        self.data = data
        if data is not None:
            for i, rowName in enumerate(data):
                self.insertItem(i, rowName[0])
