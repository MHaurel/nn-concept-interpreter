from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, \
    QTableView, QCheckBox

from visualizer.src.widgets.sidebar import Sidebar
from visualizer.src.widgets.models.grid_model import GridModel
from visualizer.src.widgets.delegates.align_center_delegate import AlignCenterDelegate


class GridWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.dataloader = None

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Sidebar
        self.sidebar = Sidebar()

        # Left Layout
        size.setHorizontalStretch(1)
        self.sidebar.setSizePolicy(size)
        self.main_layout.addWidget(self.sidebar)

        # Grid
        dataList = [
            ['20', '21', '22', '20', '21', '22'],
            ['20', '21', '22', '20', '21', '22'],
            ['20', '21', '22', '20', '21', '22']
        ]
        header = ['max-diff', 'min-pv', 'mean-pred', 'mean-real', 'std-real', 'mae']
        categories = ['France', 'Chine', 'United States']

        self.grid_model = GridModel(self, dataList, header, categories)
        self.grid = QTableView()

        self.grid.setModel(self.grid_model)

        align_center_delegate = AlignCenterDelegate()
        for i in range(len(dataList[0])):
            self.grid.setItemDelegateForColumn(i, align_center_delegate)

        # Right Layout
        size.setHorizontalStretch(4)
        self.grid.setSizePolicy(size)
        self.main_layout.addWidget(self.grid)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)


    def set_dataloader(self, dataloader):
        self.dataloader = dataloader

    def goToHome(self):
        self.parent().goto("home", self.dataloader)

    def goToSample(self):
        self.parent().goto("sample", self.dataloader)

    def goToCategories(self):
        self.parent().goto("categories", self.dataloader)

    def goToGrid(self):
        pass  # This is already the current window
