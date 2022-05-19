# -*- coding: utf-8 -*-
"""activations-significant-diffs.ipynb

# Visualizing and understanding significant differences in neuron activations for the trained model in another notebook
"""

import pandas as pd
import numpy as np

df = pd.read_csv('./data/activations.csv')
df.shape

df.head()

df

cats = df.categories.iloc[0]
for c in cats:
    print(c)

def get_unique_cats(df):
  categories = []
  for i in range(3): # len(df.categories)
    for cat in df.categories.iloc[i].split(','):
        _cat = cat.replace('[', '').replace(']', '').replace(' ', '')
        if not _cat in categories:
            categories.append(_cat)
  return categories

get_unique_cats(df)

# Get categories which number of films associated is greater (or equal) than
# a given value
def get_cats_greater_or_equal_than(value):
    cats = []
    for l in get_unique_cats():
        cat, n = l
        if n >= value:
            cats.append((cat, n))
    return cats


# Return the list of activations (list) related to a given category
def get_activations_for_cat(category):
    activations = []
    for i in range(len(df.categories)):
        if category in df.categories.iloc[i]:
#           print(df_cat_act.cat.iloc[i], i)
            act = []
            activations_row = df.iloc[i, 1:]
            for j in range(len(activations_row)):
              act.append(activations_row[j])
            activations.append(act)
    return np.array(activations)