import os

import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import Embedding


class SampleBooster:
    def __init__(self, dataloader, sample, category, layer_index):
        self.factor = 0.25  # e.g. ?????% I believed 0.1 was 10 percent but seems that I was wrong - 25 seems to be good

        self.dataloader = dataloader

        self.layer_index = layer_index

        print(f"boosting the sample on {self.dataloader.model.get_layers()[self.layer_index].name}")

        self.df = self.dataloader.get_dfs()[self.layer_index]

        # Buffer which stores the bunch of new activations at each iteration
        # Can keep track of the history (with index) and allows us to repeat the boosting
        self.na_buffer = {}

        # Dict storing history of boosts
        self.history = {}

        self.sample = sample

        self.category = category
        self.pvalue = None
        self.dfrpv = None

    def boost(self):
        output_rows = self.dataloader.model.get_layers()[self.layer_index].output_shape[-2]
        output_dim = self.dataloader.model.get_layers()[self.layer_index].output_shape[-1]

        if self.dataloader.model.get_layers()[self.layer_index].name in self.na_buffer:
            # do not load the ssr and use the last index of self.na_buffer as the sample activations
            df_ssr = pd.DataFrame(self.na_buffer[self.dataloader.model.get_layers()[self.layer_index].name][-1])
        else:
            self.na_buffer[self.dataloader.model.get_layers()[self.layer_index].name] = []
            self.history[self.dataloader.model.get_layers()[self.layer_index].name] = []
            df_ssr = self.dataloader.get_activation_for_sample(sample=self.sample, df=self.df)

            if isinstance(self.dataloader.model.get_layers()[self.layer_index], Embedding):
                df_ssr = pd.DataFrame(df_ssr.to_numpy().reshape(-1, output_dim))

        if isinstance(self.dataloader.model.get_layers()[self.layer_index], Embedding):
            df_mssr = pd.DataFrame(pd.DataFrame(df_ssr).mean()).T
        else:
            df_mssr = df_ssr
        df_mssr.rename(columns={k: f"neuron_{k+1}" for k in df_mssr.columns.tolist() if str(k).isdigit()}, inplace=True)

        df_smc = self.dataloader.get_mean_activation_for_cat(self.category, df=self.df, index=self.layer_index)
        df_smc.rename(columns={k: f"neuron_{k+1}" for k in df_smc.columns.tolist() if str(k).isdigit()}, inplace=True)

        d = df_mssr.to_numpy() - df_smc.to_numpy()

        fd = self.factor * d
        if isinstance(self.dataloader.model.get_layers()[self.layer_index], Embedding):
            fd /= output_rows

        df_ssrp = df_ssr.to_numpy() - fd
        self.na_buffer[self.dataloader.model.get_layers()[self.layer_index].name].append(df_ssrp)

        df_ssrp = pd.DataFrame(pd.DataFrame(df_ssrp).mean()).T
        df_ssrp.rename(columns={k: f"neuron_{k+1}" for k in df_ssrp.columns.tolist()}, inplace=True)

        self.pvalue = self.dataloader.find_pv(self.category, self.df,
                                              self.dataloader.model.get_layers()[self.layer_index].name,
                                              self.layer_index)

        self.dfrpv = pd.DataFrame(self.pvalue, columns=['pvalue'])
        self.dfrpv['sign'] = self.dfrpv['pvalue'] <= 0.01
        self.dfrpv.rename(index={k: f"neuron_{k + 1}" for k in self.dfrpv.index.tolist()}, inplace=True)

        dfb = pd.concat([df_mssr, df_smc, self.dfrpv.T]).T
        dfb.columns = [
            'sample', 'cat', 'pvalue', 'sign'
        ]

        dfb['new_value'] = dfb['sample']

        for i in range(dfb.shape[0]):
            index = f"neuron_{i+1}"
            if dfb.loc[index, 'sign'] is True:
                dfb.loc[index, 'new_value'] = df_ssrp.T.loc[index, 0]

        return dfb['new_value']

    def predict(self, new_value=None):
        """
        Re-construct the 'back' of the model and predict with new activations in order to get a
        new prediction and see if the boost worked.
        :return: the prediction(s)
        """

        if new_value is None:
            new_value = self.boost()

        model = Sequential()
        for i in range(self.layer_index + 1, len(self.dataloader.model.get_layers())):
            model.add(self.dataloader.model.get_layers()[i])

        model.build(input_shape=self.dataloader.model.get_layers()[self.layer_index].output_shape)

        new_inputs = new_value.to_numpy()
        new_inputs = new_inputs.reshape(-1, new_inputs.shape[0])
        new_inputs = new_inputs.reshape(-1, new_inputs.shape[-2], new_inputs.shape[-1])
        new_inputs = np.array(new_inputs).astype('float32')

        pred = model.predict(new_inputs)
        self.history[self.dataloader.model.get_layers()[self.layer_index].name].append(pred[0][0])

        """
        /!\-/!\-/!\-/!\-/!\-/!\
            NEED TO MAKE THIS PROCESS MORE GENERIC
        /!\-/!\-/!\-/!\-/!\-/!\
        """
        if self.dataloader.dirname == 'painters_ds':
            return [1 if p >= 0.5 else 0 for p in pred]
        return [np.argmax(p) for p in pred]

    def get_history(self):
        """
        Return the history of predictions
        :return: a dict of the history of predictions for each layer
        """
        return self.history

    def update_layer_index(self, layer_index):
        """
        Changes the current df according to the new layer_index
        :param layer_index: the layer for which we want to do the operations next
        :return: None
        """
        self.layer_index = layer_index
        self.df = self.dataloader.get_dfs()[self.layer_index]
