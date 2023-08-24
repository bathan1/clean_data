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
print('Matched IDs!')

# Delete patients without measurements
count_deleted_patients = 0
file = open('no_measurements.txt', 'w')
for index_p, row_patients in patients_df.iterrows():
    if pd.isna(row_patients[22]):
        count_deleted_patients += 1 # Increment count
        file.write(str(row_patients[0]) + '\n') # Write out patient ID 
        patients_df.drop(index_p, inplace=True) # Drop the patient
# Write out total amount of patients whose measurements weren't included and close file
file.write(str(count_deleted_patients))
file.close()
print('Deleted patients without measurements!')

new_rows = []
# Iterate one more time to include any patients not in the clean sheet
for index_c, row_calcs in calculations_df.iterrows():
    patient_id = row_calcs[20]
    if patient_id not in patients_df[21].values:
        new_row = {column: '' for column in patients_df.columns}
        new_row[0] = row_calcs[0]
        
        for i in range(23, 43):
            new_row[i] = row_calcs[i - 22]
        new_rows.append(new_row)

new_rows_df = pd.DataFrame(new_rows)
patients_df = pd.concat([patients_df, new_rows_df])
print('Added patients not in patients sheet')

# Delete unnecessary columns
cols_to_delete = [1, 2, 6, 7, 8, 9, 10, 11, 16, 20, 21, 22, 42]
combined_cleaned = patients_df.drop(cols_to_delete, axis=1)
print('Deleted unneeded columns!')