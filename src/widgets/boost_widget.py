from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

from src.backend.sample_booster import SampleBooster
from src.widgets.charts.boost_chart_widget import BoostChartWidget
from src.widgets.header_boost_widget import HeaderBoostWidget
from src.widgets.dialogs.history_boosting_popup import HistoryBoostingPopup


class BoostWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sample = None
        self.dataloader = None
        self.category = None
        self.sample_booster = None
        self.layer_index = 0  # First layer by default

        # Home button & layer combobox
        self.header_boost_widget = HeaderBoostWidget()

        # Chart widget
        self.boost_chart_widget = BoostChartWidget()

        # True output label
        self.label_true_output = QLabel(f"True output: ")

        # Old prediction
        self.label_old_pred = QLabel(f"Old prediction: ")

        # New prediction
        self.label_new_pred = QLabel(f"New prediction: ")

        # History of boost label
        self.label_history = QLabel("")

        # History of boost button
        self.btn_history_boost = QPushButton('Show boost history')
        self.btn_history_boost.clicked.connect(self.show_history_with_popup)

        # Boost button
        self.btn_boost = QPushButton("Boost sample")
        self.btn_boost.clicked.connect(self.boost_sample)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.header_boost_widget)
        self.main_layout.addWidget(self.boost_chart_widget)
        self.main_layout.addWidget(self.label_true_output)
        self.main_layout.addWidget(self.label_old_pred)
        self.main_layout.addWidget(self.label_new_pred)
        self.main_layout.addWidget(self.label_history)
        self.main_layout.addWidget(self.btn_history_boost)
        self.main_layout.addWidget(self.btn_boost)

        self.setLayout(self.main_layout)

    def set_dataloader(self, dataloader):
        """
        Updates the dataloader in this class and in the child elements.
        Also initialize the sample booster.
        :param dataloader: The dataloader to set
        :return: None
        """
        self.dataloader = dataloader
        self.header_boost_widget.set_datalaoder(self.dataloader)
        self.boost_chart_widget.set_dataloader(self.dataloader)

        self.init_sample_booster()

    def set_sample(self, sample):
        """
        Updates the sample on this class and in the child elements.
        Also initialize the sample booster.
        :param sample: the sample to set
        :return: None
        """
        self.sample = sample
        self.header_boost_widget.set_sample(self.sample)
        self.boost_chart_widget.set_sample(self.sample)
        self.label_true_output.setText(f"True output: {self.sample.true[0]}")
        self.label_old_pred.setText(f"Old prediction: {self.sample.pred[0]}")

        self.init_sample_booster()

    def set_category(self, category):
        """
        Update the category in this class and in the child elements.
        Also initialize the sample booster.
        :param category: The category to set
        :return: None
        """
        self.category = category
        self.header_boost_widget.set_category(self.category)
        self.boost_chart_widget.set_category(self.category)

        self.init_sample_booster()

    def init_sample_booster(self):
        """
        Tries to initialize the sample booster.
        :return: None
        """
        if self.dataloader is not None and self.sample is not None and self.category is not None:
            self.sample_booster = SampleBooster(
                dataloader=self.dataloader, sample=self.sample, category=self.category, layer_index=self.layer_index
            )

    def boost_sample(self):
        """
        Calls the sample booster to get sample activations closer and updates the history with the new
        prediction(s).
        :return: None
        """
        new_value = self.sample_booster.boost()
        # Update chart with new series
        self.boost_chart_widget.add_series(new_value.to_numpy(), "boosted activations")

        new_pred = self.sample_booster.predict(new_value)
        self.label_new_pred.setText(f"New prediction: {new_pred[0]}")
        if self.sample.true[0] == new_pred[0]:
            self.label_new_pred.setObjectName('good_pred_label')
            self.label_new_pred.setStyleSheet('QLabel#good_pred_label {color: green}')
        else:
            self.label_new_pred.setObjectName('bad_pred_label')
            self.label_new_pred.setStyleSheet('QLabel#bad_pred_label {color: red}')
        self.show_history()

    def update_layer_index(self, layer_index):
        """
        Update the layer index in this class, in the child elements and in the sample booster.
        Also clears to UI to wait displaying the newly updated layer.
        :param layer_index: The layer index to set
        :return: None
        """
        self.layer_index = layer_index
        self.boost_chart_widget.update_layer_index(self.layer_index)

        self.sample_booster.update_layer_index(self.layer_index)

        self.boost_chart_widget.set_dataloader(self.dataloader)
        self.boost_chart_widget.set_sample(self.sample)
        self.boost_chart_widget.set_category(self.category)

        self.clear_ui()

    def clear_ui(self):
        """
        Clears the UI.
        :return: None
        """
        self.label_history.setText("")
        self.label_new_pred.setText("")

    def show_history(self):
        """
        Displays the history of predicitons at the bottom of the window
        :return: None
        """
        if self.sample_booster is not None:
            try:
                history = self.sample_booster.get_history()[self.dataloader.model.get_layers()[self.layer_index].name]
                print(history)

                try:
                    self.label_history.setText(" ; ".join([str(h) for h in history]))
                except:
                    pass
            except KeyError as ke:
                print(ke)

    def show_history_with_popup(self):
        """
        Show history of predictions in a chart displayed by a popup.
        :return: None
        """
        if self.sample_booster is not None:
            try:
                history = self.sample_booster.get_history()[self.dataloader.model.get_layers()[self.layer_index].name]

                h = HistoryBoostingPopup(history)
                x = h.exec()

                try:
                    self.label_history.setText(" ; ".join([str(h) for h in history]))
                except:
                    pass
            except KeyError as ke:
                print(ke)

    def go_to_home(self):
        """
        Return to home page and clears the UI.
        :return: None
        """
        self.clear_ui()
        self.boost_chart_widget.clear_chart()
        self.parent().goto("home", self.dataloader)