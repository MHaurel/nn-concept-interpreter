import os.path
import glob
import time

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

from scipy import stats
from keras.layers import Embedding

from visualizer.src.backend.model import Model


class DataLoader:
    def __init__(self, path, model, compute_data=True):
        super().__init__()

        self.path = path
        self.model = model

        self.df = pd.read_json(self.path)

        #self.df = self.get_all_activations(self.model)

        # Will contain a df of activations for each layer of the model
        self.dfs = []

        self.heatmaps = None

        if compute_data:
            for i in range(len(self.model.get_layers())):
                #if i != 0:#Excluding embedding layer because idk how to deal with 3D data right now
                new_model = self.model.rebuild_model(i)

                df = self.get_all_activations(self.df, new_model)
                self.dfs.append(df)

            self.heatmaps = self.get_heatmaps_dict()
        else:
            # Doesn't compute data, only returns heatmaps
            self.heatmaps = self.get_heatmaps()

    def get_model(self):
        return self.model

    def get_dfs(self):
        return self.dfs

    def get_heatmaps(self):
        return self.heatmaps

    def get_heatmaps_for_layer_cat(self, layer, category):
        heatmaps = []
        if category in self.heatmaps[layer].keys():
            for heatmap in self.heatmaps[layer][category].keys():
                heatmaps.append(self.heatmaps[layer][category][heatmap]['path'])

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

    def get_activations_for_cat(self, category, model):
        inputs_cat = self.get_inputs_for_cat(category)
        return model.predict(inputs_cat)

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

    def get_all_activations(self, df, model):
        start_time = time.time()
        """
        Returns a DataFrame with all the information and activations associated
        :return: fully completed DataFrame
        """
        new_df = pd.DataFrame()

        new_df['category'] = df.category
        new_df['input'] = df.input
        new_df['output_low'] = df.output_low
        new_df['output_medium'] = df.output_medium
        new_df['output_high'] = df.output_high

        inputs = [x for x in df.input]

        activations = model.predict_input(inputs)

        # If the layer is an embedding layer, we take the mean of activations
        if isinstance(model.get_layers()[-1], Embedding):
            mean_start_time = time.time()

            print("Taking mean for Embedding")
            mean_activations = []
            for a in activations:
                mean_activations.append(pd.DataFrame(a).mean())
            activations = np.array(mean_activations)

            print(f"--- For taking mean for Embedding: {time.time() - mean_start_time} seconds ---")

        for neuron_index, value_list in enumerate(activations.T):
            index = f"neuron_{neuron_index + 1}"
            new_df[index] = value_list

        return_df = self.standardize(new_df)
        print(f"--- For get_all_activations with layer {model.get_layers()[-1]}: {time.time() - start_time} seconds ---")
        return return_df

    def get_cat_df(self, category, df):
        """
        Seek for all the samples including category
        :param df:
        :param category: The category to seek for
        :return: A DataFrame only containing the samples including the category
        """
        return df[df.category.apply(lambda x: category in x)]

    def get_activation_for_cat(self, category, df):
        """
        Fetch activations related to a specific category
        :param df:
        :param category: The category to seek the activations for
        :return: A DataFrame containing only those activations
        """
        return self.get_cat_df(category, df).iloc[:, 5:] #Must be more generic

    def get_not_cat_df(self, category, df):
        """
        Seek for all the samples which does not include category
        :param df:
        :param category: The category to not search for
        :return: A DataFrame only containing the samples not including category
        """
        return df[df.category.apply(lambda x: category not in x)]

    def get_activation_for_not_cat(self, category, df):
        """
        Fetch activations not related to category
        :param df:
        :param category: The category not to seek the activations for
        :return: A DataFrame containing all activations except the ones for category
        """
        return self.get_not_cat_df(category, df).iloc[:, 5:] #Must be more generic

    def find_pv(self, category, df):
        start_time = time.time()

        actc = self.get_activation_for_cat(category, df)
        actnc = self.get_activation_for_not_cat(category, df)
        reses = []
        for i in range(1000):
            actncs = actnc.sample(len(actc), replace=True)
            res = []
            for col in actc:
                p = stats.wilcoxon(np.array(actncs[col]), y=np.array(actc[col])).pvalue
                res.append(p)
            reses.append(res)

        return_df = pd.DataFrame(np.array(reses)).mean()

        print(f"--- for find_pv with category: {category}: {time.time() - start_time} seconds ---")
        return return_df

    def get_heatmaps_dict(self):
        start_time = time.time()

        dheatmaps = {}

        heatmap_path = '../heatmaps/'

        if not os.path.exists(heatmap_path):
            os.makedirs(heatmap_path)

        #for i in range(len(self.model.get_layers())):
        for i in range(len(self.dfs)):
            ddf = {}

            current_path = os.path.join(heatmap_path, self.model.get_layers()[i].name)
            if not os.path.exists(current_path):
                os.makedirs(current_path)

            for c, n in self.get_popular_categories(thresh=500):
                for_cat = {}

                r = self.find_pv(c, self.dfs[i])

                # 1st heatmap
                rdf = pd.DataFrame(r)
                ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
                fig = ax.get_figure()
                path = f"{current_path}/{c}-1.png"
                fig.savefig(path)

                for_cat['heatmap-1'] = {}
                for_cat['heatmap-1']['path'] = path
                for_cat['heatmap-1']['data'] = np.array(rdf[0]).T

                # 2nd heatmap
                rdf[0] = rdf[0].apply(lambda x: 0 if x > 0.01 else 1)
                ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
                fig = ax.get_figure()
                path = f"{current_path}/{c}-2.png"
                fig.savefig(path)

                for_cat['heatmap-2'] = {}
                for_cat['heatmap-2']['path'] = path
                for_cat['heatmap-2']['data'] = np.array(rdf[0]).T

                # Add paths to dict
                ddf[c] = for_cat

            dheatmaps[self.model.get_layers()[i].name] = ddf

        print(f"--- For get_heatmaps_dict: {time.time() - start_time} seconds ---")

        return dheatmaps

    def get_category_from_path(self, path):
        return path.split('\\')[-1].split('.')[0].split('-')[0]

    def get_heatmaps(self):
        dheatmaps = {}

        heatmap_path = '../heatmaps/'

        if not os.path.exists(heatmap_path):
            return {}

        ddf = {}

        for dir in os.listdir(os.path.join('..', 'heatmaps')):
            for_cat = {}

            for p, n in self.get_popular_categories(thresh=500):
                h1 = os.path.join('..', 'heatmaps', dir, f"{p}-1.png")
                for_cat["heatmap-1"] = {}
                for_cat["heatmap-1"]['path'] = h1

                h2 = os.path.join('..', 'heatmaps', dir, f"{p}-2.png")
                for_cat["heatmap-2"] = {}
                for_cat["heatmap-2"]['path'] = h2

                ddf[p] = for_cat

            dheatmaps[dir] = ddf

        return dheatmaps


if __name__ == '__main__':

    import time
    start_time = time.time()

    m = Model(path='../../models/bycountry_model')
    # dl = DataLoader('../../data/bycountry_ds.json', model=m, compute_data=False) # 3 seconds
    dl = DataLoader('../../data/bycountry_ds.json', model=m, compute_data=True)
    heatmaps = dl.get_heatmaps()
    #print(heatmaps)

    print(f"--- Overall: {time.time() - start_time} seconds ---")