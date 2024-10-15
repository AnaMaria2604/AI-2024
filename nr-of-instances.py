import pandas as pd

# Load the Excel file
file_path = 'first_sheet_from_data.xlsx'  # Update with the correct path
df = pd.read_excel(file_path)

# Function to compute distinct values and frequencies for each column
def compute_distinct_values_and_frequencies(df):
    result = {}
    for col in df.columns:
        distinct_values = df[col].value_counts(dropna=False)
        result[col] = distinct_values
    return result

# Compute distinct values and frequencies for the entire dataset
distinct_values_frequencies = compute_distinct_values_and_frequencies(df)

# Function to compute distinct values and frequencies for each column, grouped by race
def compute_distinct_values_by_race(df, group_col='Race'):
    grouped_result = {}
    grouped_df = df.groupby(group_col)
    
    for race, group in grouped_df:
        grouped_result[race] = compute_distinct_values_and_frequencies(group)
    
    return grouped_result

# Compute distinct values and frequencies for each attribute by race
distinct_values_by_race = compute_distinct_values_by_race(df)

#print(distinct_values_frequencies)
print(distinct_values_by_race['EUR'])


