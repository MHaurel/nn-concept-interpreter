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

        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_load_model = QtWidgets.QPushButton("Load model")
        self.btn_load_data = QtWidgets.QPushButton("Load data")

    def modify_widgets(self):
        pass

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_load_model)
        self.main_layout.addWidget(self.btn_load_data)

    def setup_connections(self):
        self.btn_load_model.clicked.connect(self.load_model)
        self.btn_load_data.clicked.connect(self.load_data)

    # END UI

    def load_model(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select model folder")
        try:
            self.label_load_model = QtWidgets.QLabel('Loading model...')
            self.main_layout.addWidget(self.label_load_model)
            model = keras.models.load_model(path)
            self.model_path = path
            print(self.model_path)
            self.btn_load_model.setParent(None)

            if self.data_path and self.model_path:
                # Display figure
                self.label_fig = QtWidgets.QLabel()
                self.pixmap_fig = QtGui.QPixmap('./src/img/model_ill.png')
                self.label_fig.setPixmap(self.pixmap_fig)
                self.label_fig.setMask(self.pixmap_fig.mask())

                self.main_layout.addWidget(self.label_fig)

        except:
            # Shows error via label
            print("This is not a model !")

        finally:
            if self.model_path:
                self.label_load_model.setText("Model loaded!")
            else:
                self.label_load_model.setText("Could not load model!")


    def load_data(self):
        path = QtWidgets.QFileDialog.getOpenFileNames(self, "Select some files", '', 'JSON files (*.json)')
        if path != ('', ''):
            self.data_path = path
            print(self.data_path)
            self.btn_load_data.setParent(None)
            if self.data_path and self.model_path:
                # Display figure
                self.label_fig = QtWidgets.QLabel()
                self.pixmap_fig = QtGui.QPixmap('./src/img/model_ill.png')
                self.label_fig.setPixmap(self.pixmap_fig)
                self.label_fig.setMask(self.pixmap_fig.mask())

                self.main_layout.addWidget(self.label_fig)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Visualizer()
    widget.show()

    with open('./css/styles.qss', "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
