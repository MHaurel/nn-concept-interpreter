from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QWidget, QPushButton, QLabel

from visualizer.src.widgets.threads.dataloader_init_thread import DataloaderInitThread
from visualizer.src.widgets.threads.dataloader_init_thread import RunFunctionDialog
from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader

class TestWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.main_layout = QVBoxLayout()

        self.btn = QPushButton('Show dialog')
        self.btn.clicked.connect(self.show_dialog)

        self.main_layout.addWidget(self.btn)

        self.setLayout(self.main_layout)

    def show_dialog(self):
        dialog = RunFunctionDialog(self.init_dataloader)
        dialog.show()

    def init_dataloader(self):
        model = Model('../../../models/bycountry_model')
        print(model.model.summary())
        data_path = ('../../../data/bycountry_ds.json')
        dataloader = DataLoader(data_path, model, compute_data=False)
        print(dataloader.path)