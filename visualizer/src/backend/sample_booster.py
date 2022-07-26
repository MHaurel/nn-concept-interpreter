import os

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

        self.category = category

        self.pvalue = self.dataloader.find_pv(self.category, self.df,
                                              self.dataloader.model.get_layers()[layer_index].name)

        """self.dfrpv = pd.DataFrame(self.pvalue, columns=['pvalue'])
        self.dfrpv['sign'] = self.dfrpv['pvalue'] <= 0.01
        self.dfrpv.set_index(self.df_act_sample.T.index, inplace=True)
        self.dfrpv = self.dfrpv.T"""

    def boost(self):
        output_dim = self.dataloader.model.get_layers()[self.layer_index].output_shape[-1]

        df_ssr = self.dataloader.get_activation_for_sample(sample=self.sample, df=self.df)
        df_ssr = pd.DataFrame(df_ssr.to_numpy().reshape(-1, output_dim))
        df_ssr.to_pickle('df_ssr.pkl')

        df_mssr = pd.DataFrame(pd.DataFrame(df_ssr).mean()).T
        df_mssr.to_pickle('df_mssr.pkl')

        df_smc = self.dataloader.get_mean_activation_for_cat(self.category, df=self.df,
                                                             index=self.layer_index) # df Mean Category
        df_smc.to_pickle('df_smc.pkl')

        d = df_mssr - df_smc
        print("d", d)

        output_rows = self.dataloader.model.get_layers()[self.layer_index].output_shape[-2]

        print(f"f.d = {self.factor * d}")
        print('output_rows', output_rows)
        df_ssrp = df_ssr - ((self.factor * d) / output_rows)
        print(f"df_ssrp: {df_ssrp}")
        #df_new_ssr = None #standardize df_new_sr

        """df = pd.concat([self.df_act_sample, self.df_mean_cat, self.dfrpv]).T
        df.columns = [
            'sample', 'cat', 'pvalue', 'sign'
        ]

        df['new_value'] = df['sample']

        for i in range(df.shape[0]):
            index = f"neuron_{i+1}"
            if df.loc[index, 'sign']:
                df.loc[index, 'new_value'] = df.loc[index, 'sample'] - \
                                             (df.loc[index, 'sample'] - df.loc[index, 'cat']) * self.factor

        return df"""
        return None

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
        # model.predict
