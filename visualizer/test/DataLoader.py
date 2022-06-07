import keras.models
import pandas as pd
import visualkeras


class DataLoader:
    def __init__(self, model_path, data_path):
        """
        Initialize the class. Loads the model and the JSON serialized DataFrame
        :param model_path: The path to the model
        :param data_path: the JSON serialized DataFrame
        """
        super(DataLoader).__init__()
        self.model = keras.models.load_model(model_path)
        self.data = pd.read_json(data_path)
        self.activations_s = self.data.copy()

    def model_vis(self):
        """
        Saves the visualization of the model. NOT WORKING
        :return: None
        """
        path = "../src/img/model_ill.png"
        self.model.add(visualkeras.SpacingDummyLayer(spacing=150))
        visualkeras.layered_view(self.model, legend=True, to_file=path)
        return path

    def standardize(self):
        """
        Standardize activations.
        :return: DataFrame --> Standardized activations DataFrame.
        """
        for col in self.activations_s:
            if "neuron" in col:
                self.activations_s[col] = \
                    (self.activations_s[col] - self.activations_s[col].mean()) / self.activations_s[col].std()

        return self.activations_s


if __name__ == "__main__":
    dl = DataLoader('../../models/rnn-3', '../data/data.json')
    dl.model_vis()
