import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from data_widget import DataWidget

data = [
    "French_films", "American_black_and_white_films"
]


if __name__ == '__main__':
    # Qt Application
    app = QApplication(sys.argv)
    widget = DataWidget(data=data)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())