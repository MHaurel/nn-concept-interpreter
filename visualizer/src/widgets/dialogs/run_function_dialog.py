import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie

from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        print('[INFO] Loading screen initialized')

        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)

        self.movie = QMovie('loading.gif')
        self.label_animation.setMovie(self.movie)

        #timer = QTimer(self)

        self.startAnimation()
        
        #timer.singleShot(3000, self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()

    def end(self):
        print("[INFO] Loading screen ended")

        self.stopAnimation()
        self.close()


from PySide6.QtWidgets import QProgressBar, QProgressDialog


class DialogTest(QWidget):
    def __init__(self):
        super().__init__()




if __name__ == '__main__':

    app = QApplication(sys.argv)

    #demo = AppDemo()
    """d = QProgressDialog()
    d.setMaximum(50)
    d.setValue(10)
    d.show()"""

    w = LoadingScreen()


    #app.processEvents()

    #while 1
    model = Model('../../../models/painter_model')
    dataloader = DataLoader('../../../data/painters_ds.json', model=model)

    #d.setValue(50)
    w.end()

    app.exit(app.exec())