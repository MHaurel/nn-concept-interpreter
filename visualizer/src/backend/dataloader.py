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

    def get_pv_heatmaps(self):
        for c, n in self.get_popular_categories(thresh=500):
            print(f"Generating heatmaps for {c}.")
            r = self.find_pv(c)

            rdf = pd.DataFrame(r)
            # 1st heatmap
            ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
            fig = ax.get_figure()
            fig.savefig(f"../heatmaps/{c}-1.png")
            """
            data = [go.Heatmap(z=rdf.T, zmin=0, zmax=1,
                               colorscale=['rgb(255, 255, 255)', 'rgb(0, 0, 0)'],
                               reversescale=False)]
            layout = go.Layout(template='none', height=300)
            fig = go.Figure(data=data, layout=layout)
            fig.write_image(f"../heatmaps/{c}-1.png")
            """

            rdf[0] = rdf[0].apply(lambda x: 0 if x > 0.01 else 1)
            # 2nd heatmap
            ax = sns.heatmap(rdf.T, cbar=False, cmap="Greys")
            fig = ax.get_figure()
            fig.savefig(f"../heatmaps/{c}-2.png")
            """
            data = [go.Heatmap(z=rdf.T, zmin=0, zmax=1,
                               colorscale=['rgb(0, 0, 0)', 'rgb(255, 255, 255)'],
                               reversescale=False)]
            layout = go.Layout(template='none', height=300)
            fig = go.Figure(data=data, layout=layout)
            fig.write_image(f"../heatmaps/{c}-2.png")
            """


if __name__ == '__main__':
    m = Model('../../models/bycountry_model')
    new_m = m.rebuild_model(1)
    dl = DataLoader('../../data/bycountry_ds.json', model=new_m)

    dl.get_pv_heatmaps()
