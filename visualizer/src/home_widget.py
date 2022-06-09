from PySide6.QtWidgets import \
    QWidget, QPushButton, QHBoxLayout, QSizePolicy, \
    QGridLayout, QFileDialog

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

        # Button load model
        self.btn_sample = QPushButton("Sample")
        self.btn_sample.clicked.connect(self.goToSample)

        # Button load data
        self.btn_categories = QPushButton("Categories")
        self.btn_categories.clicked.connect(self.goToCategories)

        # Widget Layout
        self.main_layout = QGridLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Sidebar layout
        self.main_layout.addWidget(self.btn_sample, 1, 0)
        self.main_layout.addWidget(self.btn_categories, 2, 0)

        # Right Layout
        self.main_layout.addWidget(self.btn_load_model, 1, 1)
        self.main_layout.addWidget(self.btn_load_data, 1, 2)

        # Set the Layout to the Widget
        self.setLayout(self.main_layout)

    def loadModel(self):
        path = QFileDialog.getExistingDirectory(self, "Select model source folder")
        try:
            model = keras.models.load_model(path)
            self.model = model
            self.btn_load_model.setEnabled(False)
        except:
            #Show error through label
            print("This is not a model !")

    def loadData(self):
        path = QFileDialog.getOpenFileNames(self, 'Select data files', '', 'JSON files (*.json)')
        if path != ('', ''):
            self.data_path = path
            print(self.data_path)
            self.btn_load_data.setEnabled(False)

    def goToSample(self):
        self.parent().goto("sample")

    def goToCategories(self):
        self.parent().goto("categories")
