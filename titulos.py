import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)


df = pd.read_csv('titulos.csv', delimiter=';')

df.plot()
