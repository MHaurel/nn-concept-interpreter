from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap, QImage

import seaborn as sns


class Heatmap(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        self.path = './heatmap.png' # Will be saved as datetime datatype

        # Create the heatmap
        ax = sns.heatmap(data)
        fig = ax.get_figure()
        fig.savefig(self.path)

    def get_pixmap(self):
        im = QImage(self.path)
        return QPixmap(im)
