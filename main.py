from csv_parser import parse_csv
import pandas as pd

df_2 = pd.read_csv('./csvs/new_patients_0.csv', header=None)
print(df_2)
parse_csv(df_2, 'combined_2.csv')