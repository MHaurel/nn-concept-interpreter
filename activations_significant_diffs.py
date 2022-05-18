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
for cat in cats:
  print(cat)

def get_unique_cats(df):
  categories = []
  for i in range(3): # len(df.categories)
    for cat in df.categories.iloc[i]:
      if not cat in categories:
        categories.append(cat)
  return categories

get_unique_cats(df)

