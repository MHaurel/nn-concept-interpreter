import os.path
import json

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

        self.table_view_category = None
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

        # Button use precedent config
        self.btn_previous_config = QPushButton("Use previous config")
        self.btn_previous_config.clicked.connect(self.load_previous_config)
        if not os.path.exists(os.path.join('..', 'visualizer_data', 'previous_config.json')):
            self.btn_previous_config.setEnabled(False)

        # Widget Layout
        self.main_layout = QHBoxLayout()

        # Sidebar layout
        #self.sidebar = Sidebar()
        #self.main_layout.addWidget(self.sidebar)

        # Right Layout
        self.main_layout.addWidget(self.btn_load_model)
        self.main_layout.addWidget(self.btn_load_data)
        self.main_layout.addWidget(self.btn_previous_config)

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
            self.model_path = path[0]
            self.btn_load_model.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.dataloader = DataLoader(self.data_path, self.model)
                self.store_config(model_path=self.model_path, data_path=self.data_path)
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
            self.data_path = path[0]
            self.btn_load_data.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.dataloader = DataLoader(self.data_path, self.model)
                self.store_config(model_path=self.model_path, data_path=self.data_path)
                self.revealCategoryTable()

    def store_config(self, model_path, data_path):
        """
        Saves the last configuration used in a json file
        :param model_path: The path of the model used
        :param data_path: The path of the data used
        :return: None
        """
        if model_path is not None and data_path is not None:
            cfg_path = os.path.join('..', 'visualizer_data', 'previous_config.json')
            cfg = {
                'model_path': model_path,
                'data_path': data_path
            }
            with open(cfg_path, 'w') as f:
                json.dump(cfg, f)

            print("Config saved !")
            print(cfg)

    def load_previous_config(self):
        """
        Load the previous config stored in a json file if it exists
        :return: None
        """
        cfg_path = os.path.join('..', 'visualizer_data', 'previous_config.json')
        if os.path.exists(cfg_path):
            with open(cfg_path, 'r') as f:
                cfg = json.load(f)

            model_path = cfg['model_path']
            data_path = cfg['data_path']

            self.model = Model(model_path)
            self.data_path = data_path
            if self.model is not None and self.data_path is not None:
                self.dataloader = DataLoader(self.data_path, self.model)
                #self.store_config(model_path=self.model_path, data_path=self.data_path[0])
                self.revealCategoryTable()


    def revealCategoryTable(self):
        """
        Remove both of the load buttons and display the category table.
        :return: None
        """
        self.btn_load_model.setParent(None)
        self.btn_load_data.setParent(None)
        self.btn_previous_config.setParent(None)

        self.table_view_category = TableCategoriesWidget(dataloader=self.dataloader)
        self.main_layout.addWidget(self.table_view_category)

    def update_thresh(self, value):
        if value != self.dataloader.thresh:
            print(f"New thresh will be: {value}")
            self.table_view_category.setParent(None)
            print(self.data_path)
            self.dataloader = DataLoader(self.data_path, self.model, thresh=value)
            self.table_view_category = TableCategoriesWidget(dataloader=self.dataloader)
            self.main_layout.addWidget(self.table_view_category)

    def go_to_home(self):
        pass  # Because already on home page

    def go_to_sample(self):
        """
        Change current window to sample window
        :return: None
        """
        self.parent().goto("sample", self.dataloader)

    def go_to_explore_category(self, category):
        """
        Change current window to explore_category window
        :param category: the category to pass to the new current window
        :return: None
        """
        self.parent().goto("explore_category", self.dataloader, category)

    def go_to_boost(self):
        """

        :return:
        """
        self.parent().goto("boost")