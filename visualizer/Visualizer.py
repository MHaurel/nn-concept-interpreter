from tensorflow.keras.models import Sequential


class Visualizer:
    def __init__(self, model, X=None, y=None):
        super(Visualizer).__init__()
        self.model = model
        self.X = X
        self.y = y

        self.layers = [self.model.get_layer(l.name) for l in self.model.layers]

        # self.model.summary()

    def show_layers(self):
        for i, layer in enumerate(self.model.layers):
            print(i, layer.name)

    # Ask layer index as an input to reconstruct the network to make predictions
    def get_activations(self, layer_index):
        if self.X is None:
            return f"Please add X data via function add_data(X_data, y_data)"

        self.show_layers()

        layer_index = -1
        while layer_index < 0 or layer_index > (len(self.layers) - 1):
            layer_index = int(input("Choose the layer index you want to explore"))

        print(f"You chose layer {self.layers[layer_index].name}")

        model = Sequential()
        for i in range(layer_index):
            model.add(self.layers[i])
            print(f"Added layer {self.layers[i].name} to model.")

        return model.predict(self.X)

    # Add X and y data (train & test comprised) to the class
    def add_data(self, X=None, y=None):
        self.X = X
        self.y = y



from tensorflow import keras

if __name__ == "__main__":
    m = keras.models.load_model('../models/rnn-3')

    v = Visualizer(m)

    print(v.get_activations(4))
