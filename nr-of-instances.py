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

# Afisare
# 1. valori distincte si frecvente pentru tot dataset-ul
print("Distinct values and frequencies for the entire dataset:")
for col, values in distinct_values_frequencies_cleaned.items():
    print(f"\nColumn: {col}")
    print(values)
    print(f"Total distinct values: {len(values)}")

# # 2.Valori distincte si frecvente raportandu-ne la rase
# print("\nDistinct values and frequencies for each class (grouped by 'Race'):")
# for race, values_by_group in distinct_values_by_race_cleaned.items():
#     print(f"\nRace: {race}")
#     for col, values in values_by_group.items():
#         print(f"\n  Column: {col}")
#         print(values)
#         print(f"  Total distinct values in {race}: {len(values)}")



# Exemplu concret pt doar o rasa ca sa fie mai usor de citit
# race_to_display = 'EUR'  # Rasa pe care dorim să o afișăm

# if race_to_display in distinct_values_by_race_cleaned:
#     print(f"\nDistinct values and frequencies for race: {race_to_display}")
#     values_by_group = distinct_values_by_race_cleaned[race_to_display]
    
#     for col, values in values_by_group.items():
#         print(f"\n  Column: {col}")
#         print(values)
#         print(f"  Total distinct values in {race_to_display}: {len(values)}")



