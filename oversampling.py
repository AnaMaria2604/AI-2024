import json
import pandas as pd
from imblearn.over_sampling import SMOTE

with open("data.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)

target_column = 'Race'
X = df.drop(columns=[target_column])
y = df[target_column]

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print("Original class distribution:", y.value_counts())
print("Resampled class distribution:", pd.Series(y_resampled).value_counts())

balanced_df = pd.concat([pd.DataFrame(X_resampled), pd.Series(y_resampled, name=target_column)], axis=1)

balanced_df.to_json("balanced_data.json", orient="records", indent=4)
