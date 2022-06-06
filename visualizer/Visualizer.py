import random
import sys

from PySide6 import QtWidgets, QtCore, QtGui

from DataLoader import DataLoader

from tensorflow import keras


class Visualizer(QtWidgets.QWidget):
    def __init__(self):
        """
        Initialize the class. Display the frame and the sub-elements.
        """
        super(Visualizer).__init__()
        QtWidgets.QWidget.__init__(self)

        self.setFixedSize(1080, 600)
        self.setWindowTitle("Visualizer")

        self.model_path = None
        self.data_path = None

        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.label_overview_head = QtWidgets.QLabel("Overview")
        self.btn_load_model = QtWidgets.QPushButton("Load model")
        self.btn_load_data = QtWidgets.QPushButton("Load data")

        self.label_overview_nav = QtWidgets.QPushButton("Overview")
        self.label_activations_nav = QtWidgets.QPushButton("Activations")
        self.label_categories_nav = QtWidgets.QPushButton("Categories")

    def modify_widgets(self):
        self.btn_load_model.setObjectName("button-load")
        self.btn_load_model.setFixedSize(150, 50)

        self.btn_load_data.setObjectName("button-load")
        self.btn_load_data.setFixedSize(150, 50)

        self.label_overview_nav.setObjectName("nav")
        self.label_activations_nav.setObjectName("nav")
        self.label_categories_nav.setObjectName("nav")

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)  # QtWidgets.QHBoxLayout(self)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.setSpacing(300)
        self.sidebar_layout = QtWidgets.QVBoxLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_load_model, 0, 0, 0, 0)
        self.main_layout.addWidget(self.btn_load_data, 0, 1, 0, 1)

        self.sidebar_layout.addWidget(self.label_overview_nav)
        self.sidebar_layout.addWidget(self.label_activations_nav)
        self.sidebar_layout.addWidget(self.label_categories_nav)

    def setup_connections(self):
        self.btn_load_model.clicked.connect(self.load_model)
        self.btn_load_data.clicked.connect(self.load_data)

        self.label_overview_nav.clicked.connect(self.load_overview_page)
        self.label_activations_nav.clicked.connect(self.load_activations_page)
        self.label_categories_nav.clicked.connect(self.load_categories_page)

    # END UI

    def load_model(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select model folder")
        try:
            model = keras.models.load_model(path)
            self.model_path = path
            print(self.model_path)
            self.btn_load_model.setParent(None)

            if self.data_path and self.model_path:
                # Display figure
                # self.display_model_fig()
                self.main_layout.addLayout(self.sidebar_layout, 0, 0, 1, 1)
                self.main_layout.addWidget(self.label_overview_head, 0, 1, 2, 1)

        except:
            # Shows error via label
            print("This is not a model !")

    def load_data(self):
        path = QtWidgets.QFileDialog.getOpenFileNames(self, "Select some files", '', 'JSON files (*.json)')
        if path != ('', ''):
            self.data_path = path
            print(self.data_path)
            self.btn_load_data.setParent(None)
            if self.data_path and self.model_path:
                # Display figure
                # self.display_model_fig()
                self.main_layout.addLayout(self.sidebar_layout, 0, 0, 1, 1)
                self.main_layout.addWidget(self.label_overview_head, 0, 1, 2, 1)

    def load_overview_page(self):
        print("Loading overview page")

    def load_activations_page(self):
        print("Loading activations page")

    def load_categories_page(self):
        print("Loading categories page")

    def display_model_fig(self):
        self.label_fig = QtWidgets.QLabel()
        self.pixmap_fig = QtGui.QPixmap('./src/img/model_ill.png')
        self.label_fig.setPixmap(self.pixmap_fig)
        self.label_fig.setMask(self.pixmap_fig.mask())
        self.label_fig.setFixedSize(500, 300)

        self.main_layout.addWidget(self.label_fig)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Visualizer()
    widget.show()

    with open('./css/styles.qss', "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
