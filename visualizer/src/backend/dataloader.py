import os.path
import time
import json

import pandas as pd
import numpy as np
import glob as glob
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap

from scipy import stats
from keras.layers import Embedding, Conv2D, MaxPooling2D, Flatten

from visualizer.src.backend.model import Model


class DataLoader:
    def __init__(self, path, model):
        super().__init__()

        self.path = path
        self.model = model

        self.dirname = self.path.split('/')[-1].split('.')[0]

        self.df = pd.read_json(self.path)
        self.df = self.formalize_outputs(self.df)
        print(list(self.df.columns))

        #self.df = self.get_all_activations(self.model)

        # Will contain a df of activations for each layer of the model
        self.dfs = []

        self.heatmaps = None

        if not os.path.exists(os.path.join('../heatmaps', self.dirname)) or not os.path.exists(os.path.join('../activations', self.dirname)):
            print(f"There are no files in {os.path.join('../heatmaps', self.dirname)}")
            for i in range(len(self.model.get_layers())):
                #if i != 0:#Excluding embedding layer because idk how to deal with 3D data right now
                new_model = self.model.rebuild_model(i)

                df = self.get_all_activations(self.df, new_model)
                self.dfs.append(df)

            if not os.path.exists(os.path.join('../activations', self.dirname)):
                os.makedirs(os.path.join('../activations', self.dirname))

            for i in range(len(self.dfs)):
                pd.to_pickle(self.dfs[i], os.path.join('../activations', self.dirname, f"{i} - {self.model.get_layers()[i].name}.pkl"))

            self.heatmaps = self.get_heatmaps_dict()
        else:
            print(f"YAAAAYY ! There ARE files in {os.path.join('../heatmaps', self.dirname)}")
            # Doesn't compute data, only returns heatmaps
            for filename in os.listdir(os.path.join('../activations', self.dirname)):
                if filename.split('.')[-1] == 'pkl':
                    df = pd.read_pickle(os.path.join('../activations', self.dirname, filename))
                    self.dfs.append(df)

            self.heatmaps = self.get_heatmaps_from_files()

    def get_model(self):
        """
        Return the model
        :return: the model
        """
        return self.model

    def get_dfs(self):
        """
        Return the list of dataframes each containing activations for a layer
        :return: list of dataframe
        """
        return self.dfs

    def get_heatmaps(self):
        """
        Return a dict containing data and path of heatmap for each category and each layer
        :return: dict of heatmaps
        """
        return self.heatmaps

    def get_predictions(self):
        """
        Return a prediction
        :return: a prediction
        """
        inputs = np.array([np.array(x) for x in self.df.input])
        y_pred = self.model.get_model().predict(inputs) #Try to replace with self.model.predict_inputs(inputs)

        if self.dirname == "painters_ds":
            return [1 if p >= 0.5 else 0 for p in y_pred] # Because we're facing a regression problem

        else: # if self.dirname == "bycountry_ds":
            return [np.argmax(p) for p in y_pred] # Because we're facing a classification problem

    def formalize_outputs(self, df):
        """
        Transforms one-hot encoding into a single columns containing encoded output variable
        :param df: the df for which we want to formalize the outputs
        :return: the new df with formalized outputs
        """
        temp_df = df.copy()
        if 'output' not in df.columns:
            output = np.zeros(df.output_low.shape)

            temp_df['true'] = output
            temp_df.loc[(temp_df.output_medium == 1), 'true'] = 1
            temp_df.loc[(temp_df.output_high == 1), 'true'] = 2

        else:
            temp_df['true'] = temp_df['output']

        temp_df['pred'] = self.get_predictions()

        return temp_df

    def get_heatmaps_for_layer_cat(self, layer, category):
        """
        Return the path of the heatmaps for a specific layer and a specific category
        :param layer: the layer for which we want the heatmaps
        :param category: the category for which we want the heatmaps
        :return: a list of the paths of heatmaps corresponding to the layer and the category
        """
        heatmaps = []
        if category in self.heatmaps[layer].keys():
            for heatmap in self.heatmaps[layer][category].keys():
                heatmaps.append(self.heatmaps[layer][category][heatmap]['path'])

        return heatmaps

    def get_diff_heatmaps_for_cat(self, category):
        """
        Return all the heatmaps for the difference between in a category and out of this category.
        :param category: the category for which we want the heatmaps
        :return: a list of the paths of the heatmaps corresponding to the category
        """
        heatmaps_paths = {}
        for layer in self.heatmaps.keys():
            if category in self.heatmaps[layer].keys():
                heatmaps_category = []
                for heatmap in self.heatmaps[layer][category]['diff'].keys():
                    heatmaps_category.append(self.heatmaps[layer][category]['diff']['path'])
                heatmaps_paths[layer] = heatmaps_category

        return heatmaps_paths

    def get_pv_heatmaps_for_cat(self, category):
        """
        Return all the heatmaps of the pvalues for a category.
        :param category: the category for which we want the heatmaps
        :return: a list of the paths of the heatmaps corresponding to the category
        """
        heatmaps_paths = {}
        for layer in self.heatmaps.keys():
            if category in self.heatmaps[layer].keys():
                heatmaps_category = []
                for heatmap in self.heatmaps[layer][category]['pvalue'].keys():
                    heatmaps_category.append(self.heatmaps[layer][category]['pvalue']['path'])
                heatmaps_paths[layer] = heatmaps_category

        return heatmaps_paths

    def get_unique_categories(self):
        """
        Return the unique categories of the dataset
        :return: a list of the unique categories
        """
        unique_categories = []
        for i in range(len(self.df.category)):
            for cat in self.df.category[i]:
                if cat not in unique_categories and cat != '':
                    unique_categories.append(cat)

        return unique_categories

    def clean_category(self, category):
        return category.split('/')[-1]

    def get_popular_categories(self, thresh=500):
        """
        Return the popular categories (i.e. > to thresh) among the uniques ones
        :param thresh: The threshold from which we define a category to be popular among the dataset
        :return: a dictionary containing the category and the number of samples associated to
        """
        categories = self.get_unique_categories()

        dic = {}
        for category in categories:
            dic[category] = len(self.df[self.df.category.apply(lambda x: category in x)])

        return_dic = {c: n for c, n in dic.items() if n >= thresh}

        with open(os.path.join('../activations', self.dirname, 'popular_categories.json'), 'w') as f:
            json.dump(return_dic, f)

        return sorted(return_dic.items(), key=lambda x: x[1], reverse=True) # Return sorted dictionary

    def get_inputs_for_cat(self, category):
        """
        Return the inputs for a specific category
        :param category: The category for which we want to get the inputs
        :return: A list of inputs
        """
        raw_inputs = self.df[self.df.category.apply(lambda x: category in x)].input
        inputs = [i for i in raw_inputs]
        return np.array(inputs)

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
        """
        Returns a DataFrame with all the information and activations associated
        :return: fully completed DataFrame
        """
        start_time = time.time()

        new_df = pd.DataFrame()

        new_df['category'] = df.category
        new_df['input'] = df.input
        """new_df['output_low'] = df.output_low
        new_df['output_medium'] = df.output_medium
        new_df['output_high'] = df.output_high"""
        #new_df['output'] = df.output
        new_df['true'] = df.true
        new_df['pred'] = df.pred

        inputs = np.array([np.array(x) for x in df.input])

        activations = model.predict_input(inputs)

        # If the layer is an embedding layer, we take the mean of activations
        if isinstance(model.get_layers()[-1], Embedding) or \
                isinstance(model.get_layers()[-1], Conv2D) or \
                isinstance(model.get_layers()[-1], MaxPooling2D):
            mean_start_time = time.time()

            print("Taking Embedding activations")

            emb_activations_arr = [a.flatten() for a in activations]
            emb_activations_arr = np.array(emb_activations_arr)

            output_dim = model.get_layers()[-1].output_shape[-1]

            acts = []
            for i in range(len(emb_activations_arr)):
                acts.append(pd.DataFrame(pd.DataFrame(emb_activations_arr[i].reshape(-1, output_dim)).mean()).T)

            activations = np.array(acts).reshape(-1, output_dim)

            for neuron_index, value_list in enumerate(activations.T):
                index = f"neuron_{neuron_index + 1}"
                new_df[index] = value_list

            print(f"--- For taking Embedding activations: {time.time() - mean_start_time} seconds ---")

        elif not isinstance(model.get_layers()[-1], Flatten): # Excepting Flatten layer
            for neuron_index, value_list in enumerate(activations.T):
                index = f"neuron_{neuron_index + 1}"
                #print(np.array(value_list).shape)
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
        activations_cols = [col for col in df.columns if "neuron" in col]
        return self.get_cat_df(category, df).loc[:, df.columns.isin(activations_cols)] #Must be more generic

    def get_mean_activation_for_cat(self, category, df):
        return pd.DataFrame(self.get_activation_for_cat(category, df).mean()).T

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
        activations_cols = [col for col in df.columns if "neuron" in col]
        return self.get_not_cat_df(category, df).loc[:, df.columns.isin(activations_cols)] #Must be more generic

    def find_pv(self, category, df):
        """
        Return the pvalue for a category
        :param category: The category for which we want the pvalue
        :param df: The dataframe to search among
        :return: The pvalue for the category
        """
        #start_time = time.time()
        print(f"=== FIND PV for {category} ===")
        actc = self.get_activation_for_cat(category, df)
        #print(actc)
        actnc = self.get_activation_for_not_cat(category, df)
        #print(actnc)
        reses = []
        for i in range(100): #1000 by default
            actncs = actnc.sample(len(actc), replace=True)
            res = []
            for col in actc:
                p = stats.wilcoxon(np.array(actncs[col]), y=np.array(actc[col])).pvalue
                res.append(p)
            reses.append(res)

        return_df = pd.DataFrame(np.array(reses)).mean()

        #print(f"--- for find_pv with category: {category}: {time.time() - start_time} seconds ---")
        return return_df

    def get_heatmaps_dict(self):
        """
        Generate heatmaps for each popular category for each layer and enter data and path for each heatmap in a
        dictionary. Compute also the heatmap of the difference between the category and all categories except one.
        Return the dict.
        :return: a dictionary of paths and data for each heatmap for each category among the popular ones for each layer
        """
        start_time = time.time()

        dheatmaps = {}

        heatmap_path = '../heatmaps/'
        norm = matplotlib.colors.Normalize(-1, 1)
        colors = [[norm(-1.0), "cyan"],
                  [norm(-0.6), "lightblue"],
                  [norm(0.0), "black"],
                  [norm(0.6), "lightyellow"],
                  [norm(1.0), "yellow"]]

        custom_color_map = LinearSegmentedColormap.from_list(
            "",
            colors=colors,
        )

        if not os.path.exists(heatmap_path):
            os.makedirs(heatmap_path)

        #for i in range(len(self.model.get_layers())):
        for i in range(len(self.dfs)):
            ddf = {}

            current_path = os.path.join(heatmap_path, self.dirname, f"{i+1} - {self.model.get_layers()[i].name}")
            if not os.path.exists(current_path):
                os.makedirs(current_path)

            for c, n in self.get_popular_categories(thresh=200):
                heatmap_dic = {}

                # Difference between in and out of category
                plt.figure(figsize=(16,5))

                data_1 = self.get_activation_for_not_cat(category=c, df=self.dfs[i])
                data_1 = pd.DataFrame(data_1.mean()).T

                diff = np.array(self.get_activation_for_cat(c, self.dfs[i]).mean()) - np.array(data_1.T[0]) #Need to store activations (self.dfs)
                diff = pd.DataFrame(diff).T
                ax = sns.heatmap(
                    data=diff,
                    vmin=-1.0,
                    vmax=1.0,
                    cbar=False,
                    cmap=custom_color_map
                )
                fig = ax.get_figure()
                path = f"{current_path}/{self.clean_category(c)}-diff.png"
                fig.savefig(path)
                heatmap_dic['diff'] = {}
                heatmap_dic['diff']['path'] = path

                # P-values heatmaps
                r = self.find_pv(c, self.dfs[i]) #TO CHECK
                rdf = pd.DataFrame(r)
                rdf[0] = rdf[0].apply(lambda x: 0 if x > 0.01 else 1)
                ax = sns.heatmap(
                    data=rdf.T,
                    vmin=0,
                    vmax=1.0,
                    cbar=False,
                    cmap=custom_color_map
                )
                fig = ax.get_figure()
                path = f"{current_path}/{self.clean_category(c)}-pvalue.png"
                fig.savefig(path)
                heatmap_dic['pvalue'] = {}
                heatmap_dic['pvalue']['path'] = path

                # Add paths to dict
                ddf[c] = heatmap_dic

            dheatmaps[self.model.get_layers()[i].name] = ddf

        print(f"--- For get_heatmaps_dict: {time.time() - start_time} seconds ---")

        return dheatmaps

    def get_category_from_path(self, path):
        """
        Return the category from path
        :param path: the path from which we want to get the category's name
        :return: the category's name
        """
        return path.split('\\')[-1].split('.')[0].split('-')[0]

    def get_heatmaps_from_files(self):
        """
        Return the dict of heatmaps from already generated heatmaps (i.e. doesn't generate heatmaps)
        :return: a dictionary of heatmaps for each layer for each category
        """
        dheatmaps = {}

        heatmap_path = '../heatmaps/'

        if not os.path.exists(heatmap_path):
            return {}

        for dir in os.listdir(os.path.join('..', 'heatmaps', self.dirname)):
            ddf = {}

            for p, n in self.get_popular_categories(thresh=200):
                heatmaps_dict = {}

                hdiff = os.path.join('..', 'heatmaps', self.dirname, dir, f"{self.clean_category(p)}-diff.png")
                heatmaps_dict["diff"] = {}
                heatmaps_dict["diff"]['path'] = hdiff

                hpv = os.path.join('..', 'heatmaps', self.dirname, dir, f"{self.clean_category(p)}-pvalue.png")
                heatmaps_dict["pvalue"] = {}
                heatmaps_dict["pvalue"]['path'] = hpv

                ddf[p] = heatmaps_dict

            dheatmaps[dir] = ddf

        return dheatmaps

    def getTableData(self):
        """
        Compute different parameters to visualize differences between categories in a table
        :return: the computed data of these parameters, the name of these parameters and the categories we compare
        """
        categories = self.get_popular_categories(thresh=200)

        table_data_path = os.path.join('../activations', self.dirname, 'table_data.pkl')
        if not os.path.exists(table_data_path):
            print("Table data not existing. Creating it...")

            data_dict = {}
            for cat, n in categories:
                cdf = self.get_cat_df(cat, self.df)
                print(f"Category is: {cat}")
                data_dict[cat] = {
                    "max-diff": self.get_max_diff(cat),
                    "min-pv": self.get_min_pv(cat), # Was not working because dfs are not saved and then don't contains the activations if heatmaps already computed
                    "mean-pred": cdf.pred.mean(),
                    "mean-real": cdf.true.mean(),
                    "std-pred": cdf.pred.std(),
                    "std-real": cdf.true.std(),
                    "mae": abs(cdf.pred - cdf.true).sum() / len(cdf),
                    "nbr": n
                }

            data = pd.DataFrame().from_dict(data_dict).T
            data.to_pickle(table_data_path)

        else:
            data = pd.read_pickle(table_data_path)

        headers = ['max-diff', 'min-pv', 'mean-pred', 'mean-real', 'std-pred', 'std-real', 'mae', 'nbr']
        categories = [c[0] for c in categories]

        return data, headers, categories

    def get_min_pv(self, cat):
        min_pv = 1
        for i in range(len(self.dfs)):
            pv = self.find_pv(cat, self.dfs[i]).min()
            if pv < min_pv:
                min_pv = pv
        return min_pv

    def get_max_diff(self, cat):
        max_diff = 0
        for i in range(len(self.dfs)):
            df_cat = self.get_activation_for_cat(cat, self.dfs[i])
            df_ncat = self.get_activation_for_not_cat(cat, self.dfs[i])

            temp_max = abs((df_cat.mean() - df_ncat.mean()).max())
            if temp_max > max_diff:
                max_diff = temp_max

        return max_diff



if __name__ == '__main__':

    m = Model(path='../../models/church_model')

    dl = DataLoader('../../data/church_ds.json', model=m)


