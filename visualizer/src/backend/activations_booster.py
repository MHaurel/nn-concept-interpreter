import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential


class ActivationsBooster:
    def __init__(self, df, sample):
        self.factor = 0.1  # e.g. 10%

        self.df = df
        self.sample = sample

    def boost(self, sample, category, pvalue=None):
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
