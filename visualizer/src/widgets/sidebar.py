from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from visualizer.src.widgets.sidebar_tile import SidebarTile


class Sidebar(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Button Home
        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.goToHome)

        # Button Sample
        self.btn_sample = QPushButton("Sample")
        self.btn_sample.clicked.connect(self.goToSample)

        self.btn_sample.setEnabled(False)

        # Button Categories
        self.btn_categories = QPushButton("Categories")
        #self.btn_categories = SidebarTile("Categories")
        self.btn_categories.clicked.connect(self.goToCategories)

        self.btn_categories.setEnabled(False)

        # Button Grid
        self.btn_grid = QPushButton("Grid")
        self.btn_grid.clicked.connect(self.goToGrid)

        self.btn_grid.setEnabled(False)

        # Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.btn_home)
        self.main_layout.addWidget(self.btn_sample)
        self.main_layout.addWidget(self.btn_categories)
        self.main_layout.addWidget(self.btn_grid)

        #self.setFixedSize(Q)

        # Set Layout to QWidget
        self.setLayout(self.main_layout)

    def enableSampleButton(self):
        self.btn_sample.setEnabled(True)

    def enableCategoriesButton(self):
        self.btn_categories.setEnabled(True)

    def enableGridButton(self):
        self.btn_grid.setEnabled(True)

    def goToHome(self):
        self.parent().goToHome()

    def goToSample(self):
        self.parent().goToSample()

    def goToCategories(self):
        self.parent().goToCategories()

    def goToGrid(self):
        self.parent().goToGrid()