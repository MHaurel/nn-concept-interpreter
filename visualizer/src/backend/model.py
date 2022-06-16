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
        return self.model

    def get_layers(self):
        return self.model.layers

    def predict_input(self, seq):
        return self.model.predict(seq)

    def display_layers(self):
        for i, layer in enumerate(self.model.layers):
            print(f"Index: {i}, Layer : {layer.name}")

    def rebuild_model(self, layer_index):
        model = Sequential()
        for i in range(layer_index + 1):
            model.add(self.model.layers[i])

        print(f"Using layers {[x.name for x in model.layers]}")

        return Model(model=model)


if __name__ == '__main__':
    m = Model(path='../../models/bycountry_model')

