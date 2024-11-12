import json
from sklearn.model_selection import train_test_split

with open("balanced_data.json", "r") as file:
    data = json.load(file)

X = [ {key: value for key, value in entry.items() if key != "Race"} for entry in data ]
y = [ entry["Race"] for entry in data ]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_data = [dict(entry, Race=label) for entry, label in zip(X_train, y_train)]
test_data = [dict(entry, Race=label) for entry, label in zip(X_test, y_test)]

with open("train_data.json", "w") as train_file:
    json.dump(train_data, train_file, indent=4)

with open("test_data.json", "w") as test_file:
    json.dump(test_data, test_file, indent=4)

print("Data successfully split and saved into train_data.json and test_data.json.")
