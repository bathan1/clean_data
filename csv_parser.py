import pandas as pd
import re
from id_duplicate_checker import check_duplicates

def parse_csv(cleaned_df: pd.DataFrame, output_file_name: str):
    pd.set_option('display.max_columns', None)

    # Extract D.O.B using regex
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

    gender_data = {'Gender': []}
    gender_df = pd.DataFrame(gender_data)
    gender_list = []

    # DOB column setup
    dob_data = {'DOB': []}
    dob_df = pd.DataFrame(dob_data)
    dob_list = []

    # Study Date Column setup
    completion_term = 'Completion Date:'
    completion_pattern = re.compile(rf'{re.escape(completion_term)}\s+(.*)')

    # Make am empty dataframe for completion date
    completion_data = {'Completion Date': []}
    completion_df = pd.DataFrame(completion_data)
    completion_list = []

    dupe_data = {'Duplicates': []}
    dupe_df = pd.DataFrame(dupe_data)
    dupe_list = []

    # Initialize duplicate count
    dupe_count = 0
    for index, row in cleaned_df.iterrows():
        report = str(row[report_column])
        dob_match = dob_pattern.search(report)

        # Get patient ID
        patient_id = row[13]
        # Check if patient is a dupe
        (is_dupe, dupe_count) = check_duplicates(patient_id, dupe_count)
        if is_dupe:
            print(f'Patient {patient_id} is a dupe!')
            dupe_list.append(patient_id)
            continue
        # If patient isn't a dupe, continue with the parsing
        id_list.append(patient_id)

        # Get accessions
        accession_pattern = re.compile(rf'{re.escape(accession_term)}\s+(.*)')
        accession_match = accession_pattern.search(report)
        # Ensure accessions in report match accession in spreadsheet
        if not accession_match:
            print(f'No Accession # found for patient {str(row[13])}')
            accession_list.append('')
        else:
            extracted_accession = accession_match.group(1).strip()
            if (str(row[3]) != extracted_accession):
                print(f'Accession # {str(row[3])} not matched for patient {str(row[13])}')
                accession_list.append('')
            else:
                accession_list.append(extracted_accession)

        # Get gender
        gender = row[11]
        if gender == 'Female':
            gender_list.append('F')
        else:
            gender_list.append('M')
            
        # Get DOB
        if dob_match:
            extracted_dob = dob_match.group(1).strip()
            dob_file.write(extracted_dob + '\n')
            dob_list.append(extracted_dob)
        else:
            no_dob_count += 1
            dob_file.write(f'No D.O.B. found for accession no. : {str(row[3])}\n')
            dob_list.append('')

        # Get Completion Date
        completion_match = completion_pattern.search(report)
        
        if completion_match:
            extracted_completion = completion_match.group(1).split()[0]
            completion_list.append(extracted_completion)
        else:
            completion_list.append('')

    # Print out number of dupes
    print(f'Number of dupes: {dupe_count}')

    # First write out number of patients with incomplete reports
    dob_file.write(f'Number of patients with incomplete reports: {str(no_dob_count)}')
    dob_file.close() # Close file

    # Next, populate dataframes
    accession_df['Accession no.'] = accession_list
    id_df['Patient ID'] = id_list
    gender_df['Gender'] = gender_list
    dob_df['DOB'] = dob_list 
    completion_df['Completion Date'] = completion_list 
    dupe_df['Duplicates'] = dupe_list

    # Write out dupes to csv
    dupe_df.to_csv('./out/dupes.csv', index=False)
    print('Wrote out dupes!')

    # Combine dataframes into one dataframe
    combined_df = pd.concat([accession_df, id_df, gender_df, dob_df, completion_df], axis=1)

    # Now get date difference between DOB and CT Completion date
    from datetime import datetime
    data = {'Age(yrs)': [],
            'Age(mos)': []}
    age_df = pd.DataFrame(data)
    age_yrs_list = []
    age_mos_list = []


    for index, row in combined_df.iterrows():
        try:
            dob_date = datetime.strptime(row['DOB'], '%m/%d/%Y')
            completion_date = datetime.strptime(row['Completion Date'], '%m/%d/%Y')
            date_difference = completion_date - dob_date

            # Get age in days to be consistent with spreadsheet calcs
            age_days = date_difference.days 
            
            # Calculate age in months
            age_mos = age_days / 30.45
            age_mos_list.append(age_mos)

            # Calculate age in years
            age_yrs = age_days / 365
            age_yrs_list.append(age_yrs)

        except:
            age_mos_list.append('')
            age_yrs_list.append('')
            print(f'Invalid DOB for patient {row[1]}')
            continue

    # Set the data frame columns
    age_df['Age(mos)'] = age_mos_list
    age_df['Age(yrs)'] = age_yrs_list

    combined_df = combined_df.reset_index(drop=True)
    age_df = age_df.reset_index(drop=True)

    # Concatenate ages to main dataframe
    combined_df = pd.concat([combined_df, age_df], axis=1)
    combined_df.to_csv(f'./out/{output_file_name}', index=False)
    print('Wrote out all data to csv!')