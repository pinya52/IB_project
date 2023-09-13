import csv
import pandas as pd

restaurant_df = pd.read_csv('ichefdata/ichefdata/ichef 資料.csv')
print(restaurant_df.shape)

sector = restaurant_df['店名', '店址'].groupby("店址")
print(sector)

# info = dict()

# for i in range(restaurant_df.shape[0]):
#     info.add((restaurant_df.iloc[i]['店名'], restaurant_df['店址']))

# name = restaurant_df['店名'].unique()
# address = restaurant_df['店址'].unique()
# print(len(name), len(address))