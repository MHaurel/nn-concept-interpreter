import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from utils import *


class Visualizer:
    def __init__(self, model, X_train=None, y_train=None, X_test=None, y_test=None):
        super(Visualizer).__init__()
        self.model = model
        self.X_train, self.X_test = X_train, X_test
        self.y_train, self.y_test = y_train, y_test

        self.layers = [self.model.get_layer(l.name) for l in self.model.layers]
        self.layer_index = None

        self.choose_layer()
        # self.model.summary()

    # Add X and y data (train & test comprised) to the class
    def add_data(self, X_train=None, y_train=None, X_test=None, y_test=None):
        self.X_train, self.X_test = X_train, X_test
        self.y_train, self.y_test = y_train, y_test

    # Add a variable to make a comparison (ex: film categories)
    def add_comparison_variable(self, data: pd.DataFrame()):
        # We can't have access at the same amount of dataframe and variable than previously in
        # notebook.
        # Intuition: To do so, we could keep track of categories in the preprocessing phase
        # even when splitting X and y
        pass

    def choose_layer(self):
        """self.show_layers()

        layer_index = -1
        while layer_index < 0 or layer_index > (len(self.layers) - 1):
            layer_index = int(input("Choose the layer index you want to explore\n"))

        print(f"You chose layer {self.layers[layer_index].name}")
        self.layer_index = layer_index"""

        self.layer_index = 4

    # Ask layer index as an input to reconstruct the network to make predictions
    def get_activations(self):
        if self.X_test is None:  # X_test for the moment
            return "Please add X data via function add_data(X_data, y_data)"

        model = Sequential()
        for i in range(self.layer_index + 1):
            model.add(self.layers[i])
            print(f"Added layer {self.layers[i].name} to model.")

        return model.predict(self.X_test)  # Still X_test for the moment

    def get_activation_matrix_per_neuron(self):
        activations = np.array(self.get_activations())
        df = pd.DataFrame()

        for neuron_index, value_list in enumerate(activations.T):
            index = f"neuron_{neuron_index + 1}"
            df[index] = value_list

        print(df.shape)
        print(df.head())

    def make_predictions(self):
        pass

    def show_confusion_matrix(self):
        fig, ax = plt.subplots(figsize=(8, 8))

        y_pred = self.model.predict(self.X_test)  # MdA: get the predictions for X_test

        # MdA: show the confusion matrix
        y_pred_r = np.argmax(y_pred, axis=1)
        y_test_r = np.argmax(np.array(self.y_test), axis=1)
        matrix = confusion_matrix(y_test_r, y_pred_r)
        disp = ConfusionMatrixDisplay(confusion_matrix=matrix,
                                      display_labels=["exceptional", "medium-high", "medium-low"])
        disp.plot(ax=ax)

        return matrix

    def show_layers(self):
        for i, layer in enumerate(self.model.layers):
            print(i, layer.name)

    def summary(self):
        self.model.summary()


from tensorflow import keras

if __name__ == "__main__":
    m = keras.models.load_model('../models/rnn-3')

    v = Visualizer(m)

    v.get_activation_matrix_per_neuron()
