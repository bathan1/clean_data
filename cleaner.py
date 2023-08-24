import pandas as pd

# Import clean csv file
clean_csv = './csvs/clean_sheet.csv'
# Read into dataframe
patients_df = pd.read_csv(clean_csv)
# Strip text to just get ID number of patients
patients_df['CleanID'] = patients_df['Cnmc_ID'].str.replace(r'CNMC_', '')
# print(patients_df.columns)
# Change column names
patients_df.columns = range(len(patients_df.columns))
# print(patients_df.columns)

# Import calculations csv file
calculations_csv = './csvs/calculations.csv'
# Read into dataframe
calculations_df = pd.read_csv(calculations_csv)
# Strip text to just get ID number of patients
calculations_df['CleanID'] = calculations_df['Subject ID'].str.replace(r'CNMC_', '')
# print(calculations_df.columns)
# Change column names
calculations_df.columns = range(len(calculations_df.columns))
# print(calculations_df.columns)