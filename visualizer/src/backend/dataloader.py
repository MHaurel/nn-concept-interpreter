import pandas as pd
import numpy as np

from visualizer.src.backend.model import Model


class DataLoader:
    def __init__(self, path, model):
        super().__init__()

        self.path = path
        self.model = model

        self.df = pd.read_json(self.path)

    def get_unique_categories(self):
        unique_categories = []
        for i in range(len(self.df.category)):
            for cat in self.df.category[i]:
                if cat not in unique_categories and cat != '':
                    unique_categories.append(cat)

        return unique_categories

    def get_inputs_for_cat(self, category):
        raw_inputs = self.df[self.df.category.apply(lambda x: category in x)].input
        inputs = []
        for i in range(len(raw_inputs)):
            inputs.append(raw_inputs[i])
        return np.array(inputs)

    def get_activations_for_cat(self, category):
        inputs_cat = self.get_inputs_for_cat(category)
        return self.model.predict(inputs_cat)


if __name__ == '__main__':
    m = Model('../../models/bycountry_model')
    new_m = m.rebuild_model(1)
    dl = DataLoader('../../data/bycountry_ds.json', model=new_m)
    print(dl.get_activations_for_cat('France'))