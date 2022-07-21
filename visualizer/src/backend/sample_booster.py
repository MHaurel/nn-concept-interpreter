import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential

from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader


class SampleBooster:
    def __init__(self, df, sample):
        self.factor = 0.1  # e.g. 10%

        self.df = df
        self.sample = sample

    def boost(self, sample, pvalue=None):
        category = sample.category
        df = pd.concat([sample, category, pvalue]).T
        df.columns = [
            'sample', 'cat', 'pvalue', 'sign'
        ]

        df['new_value'] = df['sample']

        for i in range(df.shape[0]):
            index = f"neuron_{i+1}"
            if df.loc[index, 'sign']:
                df.loc[index, 'new_value'] = df.loc[index, 'sample'] - \
                                             (df.loc[index, 'sample'] - df.loc[index, 'cat']) * self.factor

        return df

    def predict(self):
        pass


if __name__ == '__main__':
    m = Model(path='../../models/painter_model')
    dl = DataLoader('../../data/painters_ds.json', model=m, thresh=500)

    sample_index = 'http://dbpedia.org/resource/Jacopo_Vignali'
    df = dl.df
    sample = dl.get_sample_for_cat()

    sb = SampleBooster()