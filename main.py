from csv_parser import parse_csv
import pandas as pd

df_2 = pd.read_csv('./csvs/final_data_1.csv', header=None)
df_2 = df_2.drop(0)
parse_csv(df_2, 'combined_2.csv')