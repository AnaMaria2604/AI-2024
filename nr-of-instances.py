import pandas as pd
from data import data_without_duplicates
# Convert the data_without_duplicates into a DataFrame
df_cleaned = pd.DataFrame(data_without_duplicates)

# Function to compute distinct values and their frequencies for each column
def compute_distinct_values_and_frequencies(df):
    result = {}
    for col in df.columns:
        distinct_values = df[col].value_counts(dropna=False)  # Include NaNs if any
        result[col] = distinct_values
    return result

# Function to compute distinct values and frequencies grouped by a specified column (e.g., 'Race')
def compute_distinct_values_by_group(df, group_col='Race'):
    grouped_result = {}
    grouped_df = df.groupby(group_col)  # Group the DataFrame by the 'Race' column
    
    # Compute distinct values and frequencies for each group (class)
    for group, group_df in grouped_df:
        grouped_result[group] = compute_distinct_values_and_frequencies(group_df)
    
    return grouped_result

# Compute distinct values and frequencies for the entire cleaned dataset
distinct_values_frequencies_cleaned = compute_distinct_values_and_frequencies(df_cleaned)

# Compute distinct values and frequencies for each class (grouped by 'Race')
distinct_values_by_race_cleaned = compute_distinct_values_by_group(df_cleaned)

# Display distinct values, frequencies, total values, and total distinct values for the entire dataset
print("Distinct values, frequencies, and totals for each column in the entire dataset:")
for col in df_cleaned.columns:
    total_values = df_cleaned[col].count()  # Count of non-null values in the column
    distinct_values = distinct_values_frequencies_cleaned[col]
    
    print(f"\nColumn: {col}")
    print(f"Total values: {total_values}")
    print("Distinct values and frequencies:")
    print(distinct_values)
    print(f"Total distinct values: {len(distinct_values)}")


print("\nDistinct values and frequencies for each class (grouped by 'Race'):") 
for race, values_by_group in distinct_values_by_race_cleaned.items():
    print(f"\nRace: {race}")
    for col, values in values_by_group.items():
        total_values = values.sum()  # Sum of frequencies gives total values for this group
        print(f"\n  Column: {col}")
        print(f"  Total values in {race}: {total_values}")
        print(values)
        print(f"  Total distinct values in {race}: {len(values)}")
