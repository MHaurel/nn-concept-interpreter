import keras.models

from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Dropout


class Model:
    def __init__(self, path):

        self.path = path
        self.model = keras.models.load_model(self.path)

    def display_layers(self):
        for i, layer in enumerate(self.model.layers):
            print(f"Index: {i}, Layer : {layer.name}")

    def rebuild_model(self, layer_index):
        model = Sequential()
        for i in range(layer_index + 1):
            model.add(self.model.layers[i])

        print(f"Using layer {self.model.layers[i].name}")

        return model


if __name__ == '__main__':
    m = Model('../../models/bycountry_model')
    m.display_layers()
    new_model = m.rebuild_model(0)
