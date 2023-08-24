from cleaner import calculations_df, patients_df
import pandas as pd

# Iterate through the dataframes to find matching ids
for index_p, row_patients in patients_df.iterrows():
    for index_c, row_calcs in calculations_df.iterrows():
        if row_calcs[20] == row_patients[21]:
            matching_row = calculations_df[calculations_df[20] == row_patients[21]]
            if not matching_row.empty:
                values_to_concat = matching_row.iloc[0].values
                
                # Add the measurements to the corresponding patient's row
                col_num = 22
                for col_index, col_value in enumerate(values_to_concat):
                    patients_df.at[index_p, col_num] = col_value
                    col_num += 1

# Delete unnecessary columns
cols_to_delete = [1, 2, 6, 7, 8, 9, 10, 11, 16, 20, 21, 22, 42]
combined_cleaned = patients_df.drop(cols_to_delete, axis=1)