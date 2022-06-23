import sys
import time

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout, \
    QWidget, QPushButton, QApplication, QSizePolicy, QMainWindow
from PySide6.QtGui import QPalette


class TestWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.leftMargin = 30
        self.chartWidth = 250
        self.chartHeight = 250
        self.minDisplayValue = 0
        self.maxDisplayValue = 100

        self.minValue = -1
        self.maxValue = 1
        self.span = 1

        self.setMinimumSize(self.chartWidth + self.rightMargin + self.leftMargin,
                            self.chartHeight + self.topMargin + self.bottomMargin)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        pal = QPalette()
        pal.setColor(QPalette.Background, self.backgroundColor)
        self.setPalette(pal)
        self.setAutoFillBackground(True)


class TestWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.w = TestWidget()
        self.setCentralWidget(self.w)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())