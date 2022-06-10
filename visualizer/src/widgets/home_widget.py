from PySide6.QtWidgets import \
    QWidget, QPushButton, QFileDialog, QHBoxLayout

from visualizer.src.widgets.sidebar import Sidebar

from tensorflow import keras


class HomeWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.model = None
        self.data = None #NOT USED
        self.data_path = None

        # Button load model
        self.btn_load_model = QPushButton("Load model")
        self.btn_load_model.clicked.connect(self.loadModel)

        # Button load data
        self.btn_load_data = QPushButton("Load data")
        self.btn_load_data.clicked.connect(self.loadData)

        # Widget Layout
        self.main_layout = QHBoxLayout()

        # Sidebar layout
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # Right Layout
        self.main_layout.addWidget(self.btn_load_model)
        self.main_layout.addWidget(self.btn_load_data)

        # Set the Layout to the Widget
        self.setLayout(self.main_layout)

    def loadModel(self):
        path = QFileDialog.getExistingDirectory(self, "Select model source folder")
        try:
            model = keras.models.load_model(path)
            self.model = model
            self.btn_load_model.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.sidebar.enableCategoriesButton()

        except:
            #Show error through label
            print("This is not a model !")

    def loadData(self):
        path = QFileDialog.getOpenFileNames(self, 'Select data files', '', 'JSON files (*.json)')
        if path != ('', ''):
            self.data_path = path
            self.btn_load_data.setEnabled(False)

            if self.model is not None and self.data_path is not None:
                self.sidebar.enableCategoriesButton()

    # These functions may need to be implemented in an abstract function
    # and pages window to override them
    def goToHome(self):
        pass  # Because already on home page

    def goToSample(self):
        self.parent().goto("sample", self.model, self.data_path)

    def goToCategories(self):
        self.parent().goto("categories", self.model, self.data_path)
