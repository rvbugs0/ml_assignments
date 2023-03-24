import numpy as np


class CrossEntropyLoss:
    def __init__(self):
        self.eps = 1e-15  # avoid taking log of zero

    def forward(self, y_pred, y_true):
        m = y_true.shape[0]
        self.y_pred = y_pred
        self.y_true = y_true
        loss = -np.sum(y_true * np.log(y_pred + self.eps) +
                       (1 - y_true) * np.log(1 - y_pred + self.eps)) / m
        return loss

    def backward(self):
        m = self.y_true.shape[0]
        d_loss = (self.y_pred - self.y_true) / \
            (self.y_pred * (1 - self.y_pred) + self.eps) / m
        return d_loss


class Layer:
    def __init__(self, input_size=1, output_size=1):
        self.input = None
        self.output = None
        self.weights = np.random.randn(
            input_size, output_size) * np.sqrt(2 / input_size)
        self.bias = np.zeros(output_size)

    def forward(self, input):
        raise NotImplementedError

    def backward(self, output_gradient=None):
        raise NotImplementedError

    def get_weights(self):
        return np.array([self.weights, self.bias])

    def get_bias(self):
        return self.bias

    def set_weights(self, weights):
        self.weights = weights[0]
        self.bias = weights[1]


class LinearLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__(input_size, output_size)

    def forward(self, x):
        self.input = x
        output = np.dot(x, self.weights.T) + self.bias
        self.output = output
        return output

    def backward(self, error, learning_rate=0.001):
        grad_input = np.dot(error, self.weights)
        grad_weights = np.dot(self.input.T, error)
        grad_bias = np.sum(error, axis=0)
        self.weights -= learning_rate * grad_weights
        self.bias -= learning_rate * grad_bias
        return grad_input


class SoftmaxLayer(Layer):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        exp_input = np.exp(input - np.max(input, axis=1, keepdims=True))
        self.output = exp_input / np.sum(exp_input, axis=1, keepdims=True)
        return self.output

    def backward(self, output_gradient):
        # Simplified backward pass for cross-entropy loss
        return output_gradient


class SigmoidLayer(Layer):
    def __init__(self, input_size):
        super().__init__(input_size, 1)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_gradient(self, x):
        sigm = self.sigmoid(x)
        return sigm * (1 - sigm)

    def forward(self, x):
        self.input = x
        linear_output = np.dot(x, self.weights) + self.bias
        self.output = self.sigmoid(linear_output)
        return self.output

    def backward(self, error, learning_rate=0.001):
        grad_output = self.sigmoid_gradient(self.output) * error
        grad_weights = np.dot(self.input.T, grad_output)
        grad_bias = np.sum(grad_output, axis=0)
        grad_input = np.dot(grad_output, self.weights.T)
        self.weights -= learning_rate * grad_weights
        self.bias -= learning_rate * grad_bias
        return grad_input


class TanhLayer(Layer):
    def __init__(self):
        super().__init__()

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, input):
        self.input = input
        output = self.tanh(input)
        return output

    def backward(self, output_gradient):
        tanh_grad = 1 - np.square(self.tanh(self.input))
        grad_input = output_gradient * tanh_grad
        return grad_input


class Sequential(Layer):
    def __init__(self):
        super().__init__()
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        self.output = output
        return output

    def backward(self, output_gradient):
        error = output_gradient
        for layer in reversed(self.layers):
            error = layer.backward(error)
        return error

    def save_weights(self, filename):
        weights = [layer.get_weights() for layer in self.layers]
        np.save(filename, weights)

    def load_weights(self, filename):
        weights = np.load(filename, allow_pickle=True)
        for i in range(len(self.layers)):
            self.layers[i].set_weights(weights[i])

    def predict(self, X):
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def train(self, X, y, learning_rate=0.1, epochs=1000):
        for epoch in range(epochs):
            output = self.predict(X)
            error = y - output

            for layer in reversed(self.layers):
                error = layer.backward(error, learning_rate)


if __name__ == "__main__":
    # construct input data for XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    # construct neural network
    model = Sequential()
    model.add(LinearLayer(2, 2))
    model.add(SigmoidLayer(2))
    model.add(LinearLayer(2, 1))
    model.add(SigmoidLayer(2))
    loss = CrossEntropyLoss()

    # train neural network
    learning_rate = 0.1
    for i in range(10000):
        # forward pass
        output = model.forward(X)
        loss_val = loss.forward(output, y)

        # backward pass
        grad = loss.backward()
        model.backward(grad)

        # update weights
        for layer in model.layers:
            if isinstance(layer, LinearLayer):
                layer.weights -= learning_rate * layer.grad_weights
                layer.biases -= learning_rate * layer.grad_biases

        # check for convergence
        if i % 1000 == 0:
            print(f"Iteration {i}: loss = {loss_val}")

    # evaluate the trained model
    output = model.forward(X)
    print("Predictions:")
    print(output)
