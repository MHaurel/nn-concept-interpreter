from tensorflow import keras
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
import re
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from statistics import *

import glob as glob

from Visualizer import Visualizer

import nltk
nltk.download('stopwords')

df = pd.DataFrame()

filepath = "..\data\\"  # Local notebook in a data subfolder
# filepath = '.\\' # If using temp files on colab
# filepath = '/content/drive/MyDrive/Cours/Stage/data/' # My drive repo

for filename in glob.glob(filepath + 'data-*.csv'):
    print(f"Concatening {filename} to df...")
    df = pd.concat([df, pd.read_csv(filename)], axis=0)

# df.shape

df = df.drop_duplicates()

df_cat = pd.concat([df.film, df.cat], axis=1)


def normalize_cat(x):
    return "".join(x.split(':')[2])


df_cat['cat_p'] = df_cat['cat'].apply(lambda x: normalize_cat(x))

films = df.film.unique()

incomes = []
for f in films:
    incomes.append(df[df.film == f].income.mean())

df_film = pd.DataFrame(films)
df_desc = pd.DataFrame(df.desc.unique())
df_income = pd.DataFrame(incomes)

df_new = pd.DataFrame()
df_new['film'] = df_film
df_new['income'] = df_income
df_new['desc'] = df_desc

df = df_new

zscore = (df.income - df.income.mean()) / df.income.std()
dfwo = df[abs(zscore) < 2.0]

dfwo = df[df.income < 500000000]

# fig = px.violin(dfwo, y="income")
# fig.show()

MEDIAN_VALUE = dfwo[dfwo.income < 10000000].income.median()

dfwo.loc[(dfwo.income >= 0), 'income_c'] = 'medium-low'
dfwo.loc[(dfwo.income >= MEDIAN_VALUE), 'income_c'] = 'medium-high'
dfwo.loc[(dfwo.income >= 10e6), 'income_c'] = 'exceptional'

stopwords = nltk.corpus.stopwords.words('english')


def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])

    # Remove links starting with http
    text1 = re.sub(r'http\S+', ' ', text)

    # Remove digits
    text2 = re.sub(r'\d+', ' ', text1)
    tokens = re.split('\W+', text2)
    text = [word for word in tokens if word not in stopwords + [""]]  # MdA: Added the empty string to stopwords

    return text


dfwo['desc_p'] = dfwo['desc'].apply(lambda x: clean_text(x))

X = dfwo['desc_p']
y = dfwo['income_c']

y = pd.get_dummies(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# The maximum number of words to be used (most frequent)
MAX_NB_WORDS = 10000

# Max number of words in each Tweet
MAX_SEQUENCE_LENGTH = 100

# Intialize and fit the tokenizer
tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True, split=' ')
tokenizer.fit_on_texts(X_train)

# Use that tokenizer to transform the text messages in the training and test sets
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)


def get_max_len(seq):
    max_len = 0
    for x in seq:
        if len(x) > max_len:
            max_len = len(x)
    return max_len


def get_mean_std_len(seq):
    values = []
    for x in seq:
        values.append(len(x))

    std = stdev(values)
    m = mean(values)
    return int(m + std)


X_train_seq_padded = pad_sequences(X_train_seq, get_mean_std_len(X_train_seq))
X_test_seq_padded = pad_sequences(X_test_seq, get_mean_std_len(X_train_seq))

model = keras.models.load_model('../models/rnn-3')

v = Visualizer(model, X_train_seq_padded, y_train)

print(v.get_activations(4))
