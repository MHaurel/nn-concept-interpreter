from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap, QImage

import os
import seaborn as sns


class Heatmap(QWidget):
    def __init__(self, data, index):
        QWidget.__init__(self)
        self.path = './heatmaps/'
        self.filename = f"heatmap-{index}.png"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.full_path = os.path.join(self.path, self.filename)

        # Create the heatmap
        ax = sns.heatmap(data, cbar=False)
        fig = ax.get_figure()
        fig.savefig(self.full_path)

    def get_pixmap(self):
        im = QImage(self.full_path)
        return QPixmap(im)
