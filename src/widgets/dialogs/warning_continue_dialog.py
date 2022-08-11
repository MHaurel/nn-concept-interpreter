from PySide6.QtWidgets import QMessageBox


class WarningContinueDialog(QMessageBox):
    def __init__(self, window_title="Continue ?", text="There is an unspecified warning. Would you like to continue ?"):
        super().__init__()

        self.setWindowTitle(window_title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        self.setIcon(QMessageBox.Warning)

