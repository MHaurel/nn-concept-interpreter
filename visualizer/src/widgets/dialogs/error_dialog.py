from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel,\
    QMessageBox


class ErrorDialog(QMessageBox):
    def __init__(self, window_title="Error", text="There is an unspecified error"):
        super().__init__()

        self.setWindowTitle(window_title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(QMessageBox.Critical)

