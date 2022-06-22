from PySide6.QtWidgets import \
    (QListView, QListWidget, QListWidgetItem, QLabel)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from visualizer.src.widgets.heatmap import Heatmap


class HeatmapList(QListWidget):
    def __init__(self, paths_dict=None):
        QListWidget.__init__(self)

        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(500, 500))

        self.paths_dict = paths_dict

        if self.paths_dict is not None:
            self.populate_list(self.paths_dict)

    def populate_list(self, paths_dict):
        """
        Fill the list with heatmaps got from paths
        :param paths_dict: A dict containing paths as value for each layer as key
        :return: None
        """
        for layer in paths_dict.keys():
            item_layer_name = QListWidgetItem()
            item_layer_name.setText(layer)
            self.addItem(item_layer_name)#Attach QSS, define model object name and edit font-size to make it bigger

            for path in paths_dict[layer]:
                try:
                    heatmap = Heatmap(path)
                    item = QListWidgetItem()
                    icon = QIcon()
                    icon.addPixmap(heatmap.get_pixmap())
                    item.setIcon(icon)
                    self.addItem(item)
                except:
                    print("Error encountered with heatmap loading")

    def update(self, paths_dict):
        """
        Clear & Update the list of heatmaps
        :param paths: the paths of the new heatmaps to display in the updated list
        :return: None
        """
        self.clear()
        self.populate_list(paths_dict)
