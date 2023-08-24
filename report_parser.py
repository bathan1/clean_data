import pandas as pd
import re

# Import csv
uncleaned_dob_df = pd.read_csv('./csvs/dob.csv', header=None)
# Purge dataframe of unnecessary columns
cleaned_dob_df = uncleaned_dob_df.drop(list(range(17, len(uncleaned_dob_df.columns))), axis=1)
print('Dataframe cleaned!')
print(cleaned_dob_df.shape[0])

# Now extract D.O.B using regex
dob_column = 8
dob_term = 'D.O.B:'
dob_pattern = re.compile(rf'{re.escape(dob_term)}\s+(.*)')
dob_file = open('./txts/dob.txt', 'w')
for index, row in cleaned_dob_df.iterrows():
    report = str(row[dob_column])
    match = dob_pattern.search(report)
    
    if match:
        extracted_dob = match.group(1).strip()
        dob_file.write(extracted_dob + '\n')

print('Wrote out D.O.B\'s!')
dob_file.close() # Close file
