import json
import numpy as np
import pickle

# Încărcarea modelului salvat
def load_model(filepath):
    with open(filepath, "rb") as f:
        model_weights = pickle.load(f)
    return model_weights

# Încărcă greutățile, scaler-ul și maparea claselor
model_weights = load_model("model_weights.pkl")
W1 = model_weights["W1"]
W2 = model_weights["W2"]
W3 = model_weights["W3"]
W4 = model_weights["W4"]
scaler = model_weights["scaler"]
class_map = model_weights["class_map"]

# Funcții activare

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Citirea fișierului cu trăsături pentru prezicții
with open("predict_data.json") as f_predict:
    predict_data = json.load(f_predict)

# Pregătirea datelor
X_predict = np.array([list(item.values()) for item in predict_data])
X_predict = scaler.transform(X_predict)  # Standardizare

# Forward propagation pentru preziceri
Z1 = np.dot(X_predict, W1)
A1 = relu(Z1)
Z2 = np.dot(A1, W2)
A2 = relu(Z2)
Z3 = np.dot(A2, W3)
A3 = relu(Z3)
Z4 = np.dot(A3, W4)
A4 = softmax(Z4)

# Găsirea claselor prezise
predicted_classes = A4.argmax(axis=1)

# Maparea înapoi la clasele originale
class_map_inverse = {v: k for k, v in class_map.items()}
predicted_races = [class_map_inverse[cls] for cls in predicted_classes]

# Afișarea rezultatelor
for i, item in enumerate(predict_data):
    print(f"Datele: {item}, Rasa prezisă: {predicted_races[i]}")
