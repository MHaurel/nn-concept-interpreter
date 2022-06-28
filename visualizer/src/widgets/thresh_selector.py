from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy, QMessageBox, QLabel

from visualizer.src.widgets.dialogs.error_dialog import ErrorDialog
from visualizer.src.widgets.dialogs.warning_continue_dialog import WarningContinueDialog


class ThreshSelector(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.thresh = None #Might init it at first start

        self.main_layout = QHBoxLayout()

        self.label_enter_thresh = QLabel("Edit the threshold to define a category as popular")

        self.entry_thresh = QLineEdit()
        self.entry_thresh.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.btn_validate_thresh = QPushButton("OK")
        self.btn_validate_thresh.clicked.connect(self.change_thresh)
        self.btn_validate_thresh.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.main_layout.addWidget(self.label_enter_thresh)
        self.main_layout.addWidget(self.entry_thresh)
        self.main_layout.addWidget(self.btn_validate_thresh)

        self.setLayout(self.main_layout)

    def change_thresh(self):
        """
        Calls parent to reload heatmaps from a new threshold
        :return: None
        """
        if not self.entry_thresh.text().isdigit():
            # Show error dialog saying it needs digits
            dlg = ErrorDialog(
                window_title="Error",
                text="You must enter digits !"
            )
            dlg.exec()

        else:
            # Show warning dialog saying the treatment could be long
            dlg = WarningContinueDialog(
                window_title="Continue ?",
                text="The process could be very long, would you like to continue ?"
            )
            button = dlg.exec()

            if button == QMessageBox.Yes:
                print("Continue into the process")
            else:
                print("ABORT")