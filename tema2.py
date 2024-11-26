import json
import numpy as np
from sklearn.preprocessing import StandardScaler

# Încărcarea datelor
with open("train_data.json") as f_train, open("test_data.json") as f_test:
    train_data = json.load(f_train)
    test_data = json.load(f_test)

# Pregătirea datelor
X_train = np.array([list(item.values())[:-1] for item in train_data])
y_train = np.array([item['Race'] for item in train_data]).reshape(-1, 1)

X_test = np.array([list(item.values())[:-1] for item in test_data])
y_test = np.array([item['Race'] for item in test_data]).reshape(-1, 1)

# Standardizare
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Mapare clase
unique_classes = np.unique(y_train)
class_map = {value: idx for idx, value in enumerate(unique_classes)}
y_train_mapped = np.array([class_map[val[0]] for val in y_train])
y_test_mapped = np.array([class_map[val[0]] for val in y_test])

# Encodare one-hot
num_classes = len(unique_classes)
y_train_encoded = np.eye(num_classes)[y_train_mapped]
y_test_encoded = np.eye(num_classes)[y_test_mapped]

# Parametri rețea
input_size = X_train.shape[1]
hidden1_size = 54
hidden2_size = 40
hidden3_size = 30  # Noul strat ascuns
output_size = num_classes
learning_rate = 0.01
epochs = 10000

# Inițializare greutăți cu He Initialization
np.random.seed(42)
W1 = np.random.randn(input_size, hidden1_size) * np.sqrt(2 / input_size)
W2 = np.random.randn(hidden1_size, hidden2_size) * np.sqrt(2 / hidden1_size)
W3 = np.random.randn(hidden2_size, hidden3_size) * np.sqrt(2 / hidden2_size)
W4 = np.random.randn(hidden3_size, output_size) * np.sqrt(2 / hidden3_size)

# Funcții auxiliare
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def cross_entropy_loss(y_pred, y_true):
    return -np.sum(y_true * np.log(y_pred + 1e-9)) / y_true.shape[0]

def accuracy(y_pred, y_true):
    acc = y_pred.argmax(axis=1) == y_true.argmax(axis=1)
    return acc.mean()

# Antrenare rețea
for epoch in range(epochs):
    # Forward propagation
    Z1 = np.dot(X_train, W1)
    A1 = relu(Z1)
    Z2 = np.dot(A1, W2)
    A2 = relu(Z2)
    Z3 = np.dot(A2, W3)
    A3 = relu(Z3)
    Z4 = np.dot(A3, W4)
    A4 = softmax(Z4)

    # Calculul pierderii și acurateței
    loss = cross_entropy_loss(A4, y_train_encoded)
    if epoch % 100 == 0:
        acc = accuracy(A4, y_train_encoded)
        print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {acc:.4f}")

    # Backward propagation
    E4 = A4 - y_train_encoded
    dW4 = np.dot(A3.T, E4)

    E3 = np.dot(E4, W4.T) * relu_derivative(A3)
    dW3 = np.dot(A2.T, E3)

    E2 = np.dot(E3, W3.T) * relu_derivative(A2)
    dW2 = np.dot(A1.T, E2)

    E1 = np.dot(E2, W2.T) * relu_derivative(A1)
    dW1 = np.dot(X_train.T, E1)

    # Actualizare greutăți
    W4 -= learning_rate * dW4 / X_train.shape[0]
    W3 -= learning_rate * dW3 / X_train.shape[0]
    W2 -= learning_rate * dW2 / X_train.shape[0]
    W1 -= learning_rate * dW1 / X_train.shape[0]

# Evaluare pe setul de test
Z1 = np.dot(X_test, W1)
A1 = relu(Z1)
Z2 = np.dot(A1, W2)
A2 = relu(Z2)
Z3 = np.dot(A2, W3)
A3 = relu(Z3)
Z4 = np.dot(A3, W4)
A4 = softmax(Z4)
test_accuracy = accuracy(A4, y_test_encoded)
print(f"Accuracy on test set: {test_accuracy:.4f}")
