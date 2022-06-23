from PySide6.QtWidgets import \
    QWidget, QPushButton, QFileDialog, QHBoxLayout

from visualizer.src.widgets.sidebar import Sidebar
from visualizer.src.widgets.table_categories_widget import TableCategoriesWidget
from visualizer.src.backend.dataloader import DataLoader
from visualizer.src.backend.model import Model

from tensorflow import keras


class HomeWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.model = None

        self.data = None #NOT USED
        self.data_path = None
        self.dataloader = None

        # Button load model
        self.btn_load_model = QPushButton("Load model")
        self.btn_load_model.clicked.connect(self.loadModel)

        # Button load data
        self.btn_load_data = QPushButton("Load data")
        self.btn_load_data.clicked.connect(self.loadData)

        # Widget Layout
        self.main_layout = QHBoxLayout()

        # Sidebar layout
        #self.sidebar = Sidebar()
        #self.main_layout.addWidget(self.sidebar)

        # Right Layout
        self.main_layout.addWidget(self.btn_load_model)
        self.main_layout.addWidget(self.btn_load_data)

        # Set the Layout to the Widget
        self.setLayout(self.main_layout)

    def loadModel(self):
        """
        Show a dialog window and load the model from the folder selected by the user. And disabled the button if load
        successful. If model and data are loaded, the category table is revealed.
        :return: None
        """
        path = QFileDialog.getExistingDirectory(self, "Select model source folder")
        try:
            self.model = Model(path)
            self.btn_load_model.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.dataloader = DataLoader(self.data_path[0], self.model, compute_data=True) #This is NOT for production.
                self.revealCategoryTable()
        except:
            #Show error through label
            print("This is not a model ! / data could not be load successfully")

    def loadData(self):
        """
        Show a dialog window and load the data from the file selected by the user. And disabled the button if load
        successful. If model and data are loader, the category table is revealed.
        :return: None
        """
        path = QFileDialog.getOpenFileName(self, 'Select a data file', '', 'JSON files (*.json)')
        if path != ('', ''):
            self.data_path = path
            self.btn_load_data.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.dataloader = DataLoader(self.data_path[0], self.model, compute_data=True) #This is NOT for production
                self.revealCategoryTable()

    def revealCategoryTable(self):
        """
        Remove both of the load buttons and display the category table.
        :return: None
        """
        self.btn_load_model.setParent(None)
        self.btn_load_data.setParent(None)

        self.table_view_category = TableCategoriesWidget(dataloader=self.dataloader)
        self.main_layout.addWidget(self.table_view_category)

    def go_to_home(self):
        pass  # Because already on home page

    def go_to_sample(self):
        """
        Change current window to sample window
        :return: None
        """
        self.parent().goto("sample")

    def go_to_explore_category(self, category):
        """
        Change current window to explore_category window
        :param category: the category to pass to the new current window
        :return: None
        """
        self.parent().goto("explore_category", self.dataloader, category)
