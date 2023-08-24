import pandas as pd
import re

# Import csv
uncleaned_df = pd.read_csv('./csvs/final_data.csv', header=None)
# Purge dataframe of unnecessary columns
cleaned_df = uncleaned_df.drop(list(range(17, len(uncleaned_df.columns))), axis=1)
# Remove header (header is for convenience when viewing csv)
cleaned_df = cleaned_df.drop(0)
print('Dataframe cleaned!')

# Now extract D.O.B using regex
report_column = 8
dob_term = 'D.O.B:'
dob_pattern = re.compile(rf'{re.escape(dob_term)}\s+(.*)')
dob_file = open('./txts/dob.txt', 'w')
no_dob_count = 0

# Accesssion column setup
a_data = {'Accession no.': []}
accession_df = pd.DataFrame(a_data)
accession_list = []
accession_term = 'Accession #:' # To ensure that the accessions match up to report

# MRN column setup
id_data = {'Patient ID': []}
id_df = pd.DataFrame(id_data)
id_list = []

# DOB column setup
data = {'DOB': []}
dob_df = pd.DataFrame(data)
dob_list = []

# Study Date Column setup
completion_term = 'Completion Date:'
completion_pattern = re.compile(rf'{re.escape(completion_term)}\s+(.*)')

# Make am empty dataframe for completion date
data = {'Completion Date': []}
completion_df = pd.DataFrame(data)
completion_list = []

for index, row in cleaned_df.iterrows():
    report = str(row[report_column])
    dob_match = dob_pattern.search(report)

    # Get patient ID
    patient_id = row[13]
    id_list.append(patient_id)

    # Get accessions
    accession_pattern = re.compile(rf'{re.escape(accession_term)}\s+(.*)')
    accession_match = accession_pattern.search(report)
    # Ensure accessions in report match accession in spreadsheet
    if not accession_match:
        print(f'Accession not matched: {str(row[3])}')
    else:
        extracted_accession = accession_match.group(1).strip()
        accession_list.append(extracted_accession)
        
    # Get DOB
    if dob_match:
        extracted_dob = dob_match.group(1).strip()
        dob_file.write(extracted_dob + '\n')
        dob_list.append(extracted_dob)
    else:
        no_dob_count += 1
        dob_file.write(f'No D.O.B. found for accession no. : {str(row[3])}\n')

    # Get Completion Date
    completion_match = completion_pattern.search(report)
    
    if completion_match:
        extracted_completion = completion_match.group(1).split()[0]
        completion_list.append(extracted_completion)

# First write out number of patients with incomplete reports
dob_file.write(f'Number of patients with incomplete reports: {str(no_dob_count)}')
dob_file.close() # Close file

# Next, populate dataframes
accession_df['Accession no.'] = accession_list
id_df['Patient ID'] = id_list
dob_df['DOB'] = dob_list 
completion_df['Completion Date'] = completion_list 

# Write out dataframes to csv
dob_df.to_csv('./csvs/extracted_dobs.csv', index=False) 
accession_df.to_csv('./csvs/accessions.csv', index=False) 
id_df.to_csv('./csvs/patient_ids.csv', index=False)
completion_df.to_csv('./csvs/completion_date.csv', index=False) # Write out to csv


print('Wrote out D.O.Bs!')
print('Wrote out Accessions!')
print('Wrote out Patient IDs!')
print('Wrote out completion dates!')

# Now get date difference between DOB and CT Completion date
from datetime import datetime
data = {'Age(yrs)': [],
        'Age(mos)': []}
age_df = pd.DataFrame(data)
age_yrs_list = []
age_mos_list = []

test = []

combined_df = pd.concat([accession_df, id_df, dob_df, completion_df], axis=1)
for index, row in combined_df.iterrows():
    dob_date = datetime.strptime(row['DOB'], '%m/%d/%Y')
    completion_date = datetime.strptime(row['Completion Date'], '%m/%d/%Y')
    date_difference = completion_date - dob_date

    age_days = date_difference.days # Get age in days to be consistent with spreadsheet calcs
    
    # Calculate age in months
    age_mos = age_days / 30.45
    age_mos_list.append(age_mos)

    # Calculate age in years
    age_yrs = age_days / 365
    age_yrs_list.append(age_yrs)

# Set the data frame columns
age_df['Age(mos)'] = age_mos_list
age_df['Age(yrs)'] = age_yrs_list

age_df.to_csv('./csvs/ages.csv', index=False)
print('Wrote out ages!')