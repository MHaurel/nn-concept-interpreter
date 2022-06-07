import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from data_widget import DataWidget

# from tensorflow import keras


data = [ # Will be changed to JSON loaded files
    "French_films", "American_black_and_white_films"
]

# model = keras.models.load_model('../../models/rnn-3')
model = None


if __name__ == '__main__':
    # Qt Application
    app = QApplication(sys.argv)
    widget = DataWidget(data=data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())