import pandas as pd

existing_patients = './csvs/current_patient_mrns.csv'
comparison_df = pd.read_csv(existing_patients)

def check_duplicates(id: int, dupe_count: int) -> tuple:
    is_dupe = False
    for index, row in comparison_df.iterrows():
        if (row[0] == id):
            dupe_count += 1
            is_dupe = True

    return (is_dupe, dupe_count)