import pandas as pd
import re

# Import csv
uncleaned_df = pd.read_csv('./csvs/dob.csv', header=None)
# Purge dataframe of unnecessary columns
cleaned_df = uncleaned_df.drop(list(range(17, len(uncleaned_df.columns))), axis=1)
# Remove header (header is for convenience when viewing csv)
cleaned_df = cleaned_df.drop(0)
print('Dataframe cleaned!')

# Now extract D.O.B using regex
dob_column = 8
dob_term = 'D.O.B:'
dob_pattern = re.compile(rf'{re.escape(dob_term)}\s+(.*)')
dob_file = open('./txts/dob.txt', 'w')

accession_term = 'Accession #:' # To ensure that the accessions match up to report
no_dob_count = 0
for index, row in cleaned_df.iterrows():
    report = str(row[dob_column])
    match = dob_pattern.search(report)

    accession_pattern = re.compile(rf'{re.escape(accession_term)}\s+(.*)')
    accession_match = accession_pattern.search(report)
    # Ensure accessions in report match accession in spreadsheet
    if not accession_match:
        print(f'Accession not matched: {str(row[3])}')
    
    if match:
        extracted_dob = match.group(1).strip()
        dob_file.write(extracted_dob + '\n')
    else:
        no_dob_count += 1
        dob_file.write(f'No D.O.B. found for accession no. : {str(row[3])}\n')

dob_file.write(f'Number of patients with incomplete reports: {str(no_dob_count)}')
print('Wrote out D.O.B\'s!')
dob_file.close() # Close file
