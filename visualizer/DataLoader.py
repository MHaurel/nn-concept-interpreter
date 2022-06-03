import keras.models
import pandas as pd


class DataLoader:
    def __init__(self, file_path, data):
        """
        Initialize the class. Loads the model and the JSON serialized DataFrame
        :param file_path: The path to the model
        :param data: the JSON serialized DataFrame
        """
        super(DataLoader).__init__()
        self.model = keras.models.load_model(file_path)
        self.data = pd.read_json(data)
        self.activations_s = self.data.copy()

    def standardize(self):
        for col in self.activations_s:
            if "neuron" in col:
                self.activations_s[col] = \
                    (self.activations_s[col] - self.activations_s[col].mean()) / self.activations_s[col].std()

        return self.activations_s.describe()


if __name__ == "__main__":
    dl = DataLoader('../models/rnn-3', '../data/data.json')
    print(dl.standardize())
