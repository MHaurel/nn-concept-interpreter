import os.path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

from scipy import stats

from visualizer.src.backend.model import Model


class DataLoader:
    def __init__(self, path, model):
        super().__init__()

        self.path = path
        self.model = model

        self.df = pd.read_json(self.path)

        self.df = self.get_all_activations()
        self.heatmaps = self.get_heatmaps_dict()

    def get_model(self):
        return self.model

    def get_df(self):
        return self.df

    def get_heatmaps_for_cat(self, category):
        heatmaps = []
        if category in self.heatmaps.keys():
            for heatmap in self.heatmaps[category].keys():
                heatmaps.append(self.heatmaps[category][heatmap]['path'])

        return heatmaps

    def get_unique_categories(self):
        unique_categories = []
        for i in range(len(self.df.category)):
            for cat in self.df.category[i]:
                if cat not in unique_categories and cat != '':
                    unique_categories.append(cat)

        return unique_categories

    def get_popular_categories(self, thresh=500):
        categories = self.get_unique_categories()

        dic = {}
        for category in categories:
            dic[category] = len(self.df[self.df.category.apply(lambda x: category in x)])

        return_dic = {c: n for c, n in dic.items() if n >= thresh}

        return sorted(return_dic.items(), key=lambda x: x[1], reverse=True)  # Return sorted dictionary

    def get_inputs_for_cat(self, category):
        raw_inputs = self.df[self.df.category.apply(lambda x: category in x)].input
        inputs = []
        for i in range(len(raw_inputs)):
            inputs.append(raw_inputs[i])
        return np.array(inputs)

    def get_activations_for_cat(self, category):
        inputs_cat = self.get_inputs_for_cat(category)
        return self.model.predict(inputs_cat)

    def standardize(self, df):
        """
        Standardize a DataFrame which will replace self.df
        :param df: The DataFrame to standardize
        :return: the standardized DataFrame
        """
        df_s = df.copy()
        for col in df:
            if "neuron" in col:
                df_s[col] = (df[col] - df[col].mean()) / df[col].std()

        return df_s

    def get_all_activations(self):
        """
        Returns a DataFrame with all the information and activations associated
        :return: fully completed DataFrame
        """
        new_df = pd.DataFrame()

        raw_inputs = self.df.input
        inputs = []
        for i in range(len(raw_inputs)):
            inputs.append(raw_inputs[i])

        new_df['category'] = self.df.category
        new_df['input'] = self.df.input
        new_df['output_low'] = self.df.output_low
        new_df['output_medium'] = self.df.output_medium
        new_df['output_high'] = self.df.output_high

        activations = self.model.predict(inputs)
        for neuron_index, value_list in enumerate(activations.T):
            index = f"neuron_{neuron_index + 1}"
            new_df[index] = value_list

        return self.standardize(new_df)

    def get_cat_df(self, category):
        """
        Seek for all the samples including category
        :param category: The category to seek for
        :return: A DataFrame only containing the samples including the category
        """
        return self.df[self.df.category.apply(lambda x: category in x)]

    def get_activation_for_cat(self, category):
        """
        Fetch activations related to a specific category
        :param category: The category to seek the activations for
        :return: A DataFrame containing only those activations
        """
        return self.get_cat_df(category).iloc[:, 5:] #Must be more generic

    def get_not_cat_df(self, category):
        """
        Seek for all the samples which does not include category
        :param category: The category to not search for
        :return: A DataFrame only containing the samples not including category
        """
        return self.df[self.df.category.apply(lambda x: category not in x)]

    def get_activation_for_not_cat(self, category):
        """
        Fetch activations not related to category
        :param category: The category not to seek the activations for
        :return: A DataFrame containing all activations except the ones for category
        """
        return self.get_not_cat_df(category).iloc[:, 5:] #Must be more generic

    def find_pv(self, category):
        actc = self.get_activation_for_cat(category)
        actnc = self.get_activation_for_not_cat(category)
        reses = []
        for i in range(1000):
            actncs = actnc.sample(len(actc), replace=True)
            res = []
            for col in actc:
                p = stats.wilcoxon(np.array(actncs[col]), y=np.array(actc[col])).pvalue
                res.append(p)
            reses.append(res)
        return pd.DataFrame(np.array(reses)).mean()

    def get_heatmaps_dict(self):
        dheatmaps = {}

        if not os.path.exists('../heatmaps'):
            os.makedirs('../heatmaps')

        for c, n in self.get_popular_categories(thresh=500):
            for_cat = {}

            r = self.find_pv(c)

            # 1st heatmap
            rdf = pd.DataFrame(r)
            ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
            fig = ax.get_figure()
            path = f"../heatmaps/{c}-1.png"
            fig.savefig(path)

            for_cat['heatmap-1'] = {}
            for_cat['heatmap-1']['path'] = path
            for_cat['heatmap-1']['data'] = np.array(rdf[0]).T

            # 2nd heatmap
            rdf[0] = rdf[0].apply(lambda x: 0 if x > 0.01 else 1)
            ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
            fig = ax.get_figure()
            path = f"../heatmaps/{c}-2.png"
            fig.savefig(path)

            for_cat['heatmap-2'] = {}
            for_cat['heatmap-2']['path'] = path
            for_cat['heatmap-2']['data'] = np.array(rdf[0]).T

            # Add paths to dict
            dheatmaps[c] = for_cat

        return dheatmaps


if __name__ == '__main__':
    m = Model('../../models/bycountry_model')
    new_m = m.rebuild_model(1)
    dl = DataLoader('../../data/bycountry_ds.json', model=new_m)
