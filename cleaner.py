import pandas as pd

# Import clean csv file
clean_csv = './csvs/clean_sheet.csv'
# Read into dataframe
patients_df = pd.read_csv(clean_csv)
# Strip text to just get ID number of patients
patients_df['CleanID'] = patients_df['Cnmc_ID'].str.replace(r'CNMC_', '')

# Import calculations csv file
calculations_csv = './csvs/calculations.csv'
# Read into dataframe
calculations_df = pd.read_csv(calculations_csv)
# Strip text to just get ID number of patients
calculations_df['CleanID'] = calculations_df['Subject ID'].str.replace(r'CNMC_', '')