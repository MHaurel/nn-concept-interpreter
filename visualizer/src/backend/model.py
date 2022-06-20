import keras.models
import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Dropout


class Model:
    def __init__(self, path=None, model=None):

        if path is not None:
            self.path = path
            self.model = keras.models.load_model(self.path)

        elif model is not None and path is None:
            self.model = model

    def get_model(self):
        """
        Return the model
        :return: the model
        """
        return self.model

    def get_layers(self):
        """
        Return the layers of the model
        :return: a list of Layer objects
        """
        return self.model.layers

    def predict_input(self, input):
        """
        Make a prediction from the inputs
        :param input: The input from which we want the prediction
        :return: a prediction
        """
        return self.model.predict(input)

    def display_layers(self):
        """
        Display all the layers with an index in the terminal
        :return: None
        """
        for i, layer in enumerate(self.model.layers):
            print(f"Index: {i}, Layer : {layer.name}")

    def rebuild_model(self, layer_index):
        """
        Rebuild a model until the selected layer index
        :param layer_index: The layer until which we want the model to be rebuilt
        :return: The new rebuilt model
        """
        model = Sequential()
        for i in range(layer_index + 1):
            model.add(self.model.layers[i])

        print(f"Using layers {[x.name for x in model.layers]}")

        return Model(model=model)


if __name__ == '__main__':
    m = Model(path='../../models/bycountry_model')

