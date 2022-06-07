import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from data_widget import DataWidget


if __name__ == '__main__':
    # Qt Application
    app = QApplication(sys.argv)
    widget = DataWidget(data=None)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec())