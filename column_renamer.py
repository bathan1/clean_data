import pandas as pd
from combiner import combined_cleaned

new_columns = []
# Read in variables from txt file to rename columns back to variable names
with open('vars.txt', 'r') as file:
    for line in file:
        var = line.strip()
        new_columns.append(var)

# Set columns
combined_cleaned.columns = new_columns
print('Set columns back to original names')

# Export to csv
combined_cleaned.to_excel('final_clean.xlsx', index=False)
print('Exported to xlsx')