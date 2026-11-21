import pandas as pd

data_frame = pd.read_csv('insumos/dados/produtos.csv',delimiter=',')
data_frame.head()
print(data_frame.head())
print('Total de registros:', len(data_frame))