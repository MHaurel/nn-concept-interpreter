import os

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Embedding

from visualizer.src.backend.model import Model
from visualizer.src.backend.dataloader import DataLoader


class SampleBooster:
    def __init__(self, dataloader, sample, category, layer_index):
        self.factor = 0.25  # e.g. 25%

        self.dataloader = dataloader

        self.layer_index = layer_index
        self.layer_index = 1 # Short-circuiting the program to test another layer

        print(f"boosting the sample on {self.dataloader.model.get_layers()[self.layer_index].name}")

        self.df = self.dataloader.get_dfs()[self.layer_index]

        self.sample = sample

        self.category = category

        self.pvalue = self.dataloader.find_pv(self.category, self.df,
                                              self.dataloader.model.get_layers()[self.layer_index].name, self.layer_index)

        self.dfrpv = pd.DataFrame(self.pvalue, columns=['pvalue'])
        self.dfrpv['sign'] = self.dfrpv['pvalue'] <= 0.01
        self.dfrpv.rename(index={k: f"neuron_{k+1}" for k in self.dfrpv.index.tolist()}, inplace=True)

    def boost(self):
        output_rows = self.dataloader.model.get_layers()[self.layer_index].output_shape[-2]
        output_dim = self.dataloader.model.get_layers()[self.layer_index].output_shape[-1]

        df_ssr = self.dataloader.get_activation_for_sample(sample=self.sample, df=self.df)
        #df_ssr = pd.DataFrame(df_ssr.to_numpy().reshape(-1, output_dim)) # only for embedding
        df_ssr.to_pickle('df_ssr.pkl')

        df_mssr = pd.DataFrame(pd.DataFrame(df_ssr).mean()).T
        df_mssr.rename(columns={k: f"neuron_{k+1}" for k in df_mssr.columns.tolist() if str(k).isdigit()}, inplace=True)
        df_mssr.to_pickle('df_mssr.pkl')

        df_smc = self.dataloader.get_mean_activation_for_cat(self.category, df=self.df,
                                                             index=self.layer_index) # df Mean Category
        df_smc.rename(columns={k: f"neuron_{k+1}" for k in df_smc.columns.tolist() if str(k).isdigit()}, inplace=True)
        df_smc.to_pickle('df_smc.pkl')

        d = df_mssr.to_numpy() - df_smc.to_numpy()

        fd = self.factor * d
        if isinstance(self.dataloader.model.get_layers()[self.layer_index], Embedding):
            fd /= output_rows

        df_ssrp = df_ssr.to_numpy() - fd
        df_ssrp = pd.DataFrame(pd.DataFrame(df_ssrp).mean()).T
        df_ssrp.rename(columns={k: f"neuron_{k+1}" for k in df_ssrp.columns.tolist()}, inplace=True)

        """
        /!\-/!\-/!\-/!\-/!\-/!\
            ATTENTION : ON NE FAIT LA DISTANCE QUE SUR LES NEURONES OU 
            LA DIFFERENCE EST SIGNIFICATIVE
        /!\-/!\-/!\-/!\-/!\-/!\
        """

        dfb = pd.concat([df_mssr, df_smc, self.dfrpv.T]).T
        self.dfrpv.T.to_pickle('dfrpv.pkl')
        dfb.columns = [
            'sample', 'cat', 'pvalue', 'sign'
        ]
        #df.rename(index={k: f'neuron_{k+1}' for k in df.index.tolist() if str(k).isdigit()}, inplace=True) # Renaming indexes
        dfb.to_pickle('dfb.pkl')

        dfb['new_value'] = dfb['sample']

        for i in range(dfb.shape[0]):
            index = f"neuron_{i+1}"
            if dfb.loc[index, 'sign'] is True:
                dfb.loc[index, 'new_value'] = df_ssrp.T.loc[index, 0]

        print(f"dfb['sample'].to_numpy(): {dfb['sample'].to_numpy()}")
        print(f"dfb['cat'].to_numpy(): {dfb['cat'].to_numpy()}")
        print(f"dfb['new_value'].to_numpy(): {dfb['new_value'].to_numpy()}")

        print()

        return dfb

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
        return -1 # default to test
