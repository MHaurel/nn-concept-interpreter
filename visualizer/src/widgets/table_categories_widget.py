from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, \
    QTableView, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtCore import SIGNAL

from visualizer.src.widgets.models.table_categories_model import TableCategoriesModel
from visualizer.src.widgets.delegates.align_center_delegate import AlignCenterDelegate
from visualizer.src.backend.dataloader import DataLoader
from visualizer.src.backend.model import Model

import numpy as np


class TableCategoriesWidget(QWidget):
    def __init__(self, dataloader):
        QWidget.__init__(self)

        self.dataloader = dataloader

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.data, self.header, self.categories = self.dataloader.getTableData()
        self.data_list = self.data.values.tolist()

        # Table View
        self.table_model = TableCategoriesModel(self, self.data_list, self.header, self.categories)
        self.table_view = QTableView()

        self.table_view.setModel(self.table_model)

        align_center_delegate = AlignCenterDelegate()
        for i in range(len(self.data_list[0])):
            self.table_view.setItemDelegateForColumn(i, align_center_delegate)

        # Center Layout
        #size.setHorizontalStretch(4)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Connections
        #self.table_view.clicked.connect(self.clickedCell) #Keep it for now
        self.table_view.connect(self.table_view.verticalHeader(), SIGNAL("sectionClicked(int)"), self.clickedIndex)
        self.table_view.connect(self.table_view.horizontalHeader(), SIGNAL("sectionClicked(int)"), self.clickedColumn)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def clickedIndex(self, i):
        print(f"Index clicked is {self.categories[i]}")
        # Open associated categories window
        self.go_to_explore_category(self.categories[i])
        #self.go_to_sample()

    def clickedColumn(self, i):
        print(f"Column clicked is {self.header[i]}")
        sorted_df = self.data.sort_values(by=[self.header[i]], ascending=False)
        indexes = [ind for ind in sorted_df.index]
        new_model = TableCategoriesModel(self, sorted_df.values.tolist(), self.header, indexes)
        self.table_view.setModel(new_model)

    def clickedCell(self):
        index = self.table_view.selectionModel().currentIndex()
        value = index.sibling(index.row(), index.column()).data()
        print(value)

    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def go_to_sample(self):
        self.parent().go_to_sample()

    def go_to_explore_category(self, category):
        self.parent().go_to_explore_category(category)
