import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential

from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader


class SampleBooster:
    def __init__(self, dataloader, sample, category, layer_index):
        self.factor = 0.1  # e.g. 10%

        self.dataloader = dataloader
        self.layer_index = layer_index
        self.df = self.dataloader.get_dfs()[self.layer_index]
        self.sample = sample
        self.df_act_sample = self.dataloader.get_activation_for_sample(self.sample, self.df)
        self.category = category
        self.df_mean_cat = self.dataloader.get_mean_activation_for_cat(self.category, self.df)
        self.pvalue = self.dataloader.find_pv(self.category, self.df,
                                              self.dataloader.model.get_layers()[layer_index].name)

        self.dfrpv = pd.DataFrame(self.pvalue, columns=['pvalue'])
        self.dfrpv['sign'] = self.dfrpv['pvalue'] <= 0.01
        self.dfrpv.set_index(self.df_act_sample.T.index, inplace=True)
        self.dfrpv = self.dfrpv.T

    def boost(self):
        df = pd.concat([self.df_act_sample, self.df_mean_cat, self.dfrpv]).T
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

    def predict(self, dfb=None):
        """
        Re-construct the 'back' of the model and predict with new activations in order to get a
        new prediction and see if the boost worked.
        :return: the prediction
        """

        # NEED TO CHECK IF THE PROCESS HERE IS GOOD (see visualizer.txt on desktop)
        if dfb is None:
            dfb = self.boost()
        # re-construct model
        model = Sequential()
        for i in range(self.layer_index + 1, len(self.dataloader.model.get_layers())):
            model.add(self.dataloader.model.get_layers()[i])

        model.build(input_shape=self.dataloader.model.get_layers()[0].output_shape)

        # then predict