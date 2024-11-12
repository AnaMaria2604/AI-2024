import json
import numpy as np
from sklearn.preprocessing import StandardScaler

with open("train_data.json") as f_train, open("test_data.json") as f_test:
    train_data = json.load(f_train)
    test_data = json.load(f_test)

X_train = np.array([list(item.values())[:-1] for item in train_data])
y_train = np.array([item['Race'] for item in train_data]).reshape(-1, 1)

X_test = np.array([list(item.values())[:-1] for item in test_data])
y_test = np.array([item['Race'] for item in test_data]).reshape(-1, 1)

#StandardScaler() pentru a standardiza caracteristicile (cu o medie de 0 și o deviație standard de 1)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

unique_classes = np.unique(y_train)
class_map = {value: idx for idx, value in enumerate(unique_classes)}
y_train_mapped = np.array([class_map[val[0]] for val in y_train])
y_test_mapped = np.array([class_map[val[0]] for val in y_test])

num_classes = len(unique_classes)
y_train_encoded = np.eye(num_classes)[y_train_mapped]
y_test_encoded = np.eye(num_classes)[y_test_mapped]

#Parametri retea 
input_size = X_train.shape[1]
hidden_size = 150  
output_size = num_classes
learning_rate = 0.01
epochs = 1000

# Initialize weights with Xavier initialization
np.random.seed(42)
W1 = np.random.randn(input_size, hidden_size) * np.sqrt(1 / input_size)
W2 = np.random.randn(hidden_size, output_size) * np.sqrt(1 / hidden_size)

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

for epoch in range(epochs):
    # Forward propagation
    Z1 = np.dot(X_train, W1)
    A1 = relu(Z1)
    Z2 = np.dot(A1, W2)
    A2 = softmax(Z2)
    
    # Compute cross-entropy loss and accuracy
    loss = cross_entropy_loss(A2, y_train_encoded)
    if epoch % 100 == 0:
        acc = accuracy(A2, y_train_encoded)
        print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {acc:.4f}")
    
    # Backward propagation
    E2 = A2 - y_train_encoded
    dW2 = np.dot(A1.T, E2)
    
    E1 = np.dot(E2, W2.T) * relu_derivative(A1)
    dW1 = np.dot(X_train.T, E1)
    
    # Update weights
    W2 -= learning_rate * dW2 / X_train.shape[0]
    W1 -= learning_rate * dW1 / X_train.shape[0]

# Evaluate on test set
Z1 = np.dot(X_test, W1)
A1 = relu(Z1)
Z2 = np.dot(A1, W2)
A2 = softmax(Z2)

test_accuracy = accuracy(A2, y_test_encoded)
print(f"Accuracy on test set: {test_accuracy:.4f}")
