from csv_parser import parse_csv
import pandas as pd

if __name__ == '__main__':
    df_2 = pd.read_csv('./csvs/new_patients_0.csv', header=None)
    report_df = parse_csv(df_2, 'combined_2.csv')

    print(report_df)