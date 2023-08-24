import pandas as pd
from report_parser import id_df

existing_patients = './csvs/clean_sheet.csv'
existing_p_df = pd.read_csv(existing_patients)

data = {'Duplicates': []}
duplicates_df = pd.DataFrame(data)
duplicates_list = []

duplicate_count = 0
for index_i, row_i in id_df.iterrows():
    for index_j, row_j in existing_p_df.iterrows():
        if (row_i[0] == row_j[2]):
            duplicate_count += 1
            duplicates_list.append(row_i[0])

print(f'Number of dupes: {duplicate_count}')
duplicates_df['Duplicates'] = duplicates_list
duplicates_df.to_csv('./csvs/duplicates.csv', index=False)
print('Wrote out duplicates!')