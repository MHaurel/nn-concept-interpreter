import sys
import numpy as np

from PySide6.QtWidgets import QApplication

from visualizer.src.widgets.data_widget import DataWidget

# from tensorflow import keras

data_cat = [ # Will be changed to JSON loaded files
    "French_films", "American_black_and_white_films"
]

data = [
    np.random.randn(10, 12),
    np.random.randn(9, 3),
    np.random.randn(17, 4),
]

# model = keras.models.load_model('../../models/rnn-3')
model = None


if __name__ == '__main__':
    # Qt Application
    app = QApplication(sys.argv)
    widget = DataWidget(data_cat, data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())