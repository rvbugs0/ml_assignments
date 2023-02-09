import numpy as np
import random


class LinearRegression:
    def __init__(self, batch_size=32, regularization=0, max_epochs=100, patience=3, learning_rate = 0.0001,bias=1):
        self.batch_size = batch_size
        self.regularization = regularization
        self.max_epochs = max_epochs
        self.patience = patience
        self.learning_rate = learning_rate
        self.bias = bias        
        self.weights = None
        self.batch_validation_loss = np.array([[0,0]])

    # def nfit(self, X_DATA, Y_DATA,batch_size=None, regularization=None, max_epochs=None, patience=None):
    #     x_transpose= X_DATA.T
    #     theta = np.dot(X_DATA,x_transpose)
    #     theta = np.linalg.inv(theta)
    #     theta = np.dot(theta,x_transpose)
    #     theta = np.dot(theta,Y_DATA)
    #     print(theta)

    def fit(self, X_DATA, Y_DATA,batch_size=None, regularization=None, max_epochs=None, patience=None):
        
        if batch_size is not None:
            self.batch_size = batch_size
        if regularization is not None:
            self.regularization = regularization
        if max_epochs is not None:
            self.max_epochs = max_epochs
        if patience is not None:
            self.patience = patience

        # setting aside 10% of data for validation set
        upperbound = int(X_DATA.shape[0] * 0.9)
        X = np.copy(X_DATA)[:upperbound]
        y = np.copy(Y_DATA)[:upperbound]

        validation_x = X_DATA[upperbound:]
        validation_y = Y_DATA[upperbound:]
        
        column_of_ones = self.bias* np.ones((X.shape[0],1))
        np.concatenate((column_of_ones, X), axis=1)

        n, d = X.shape
        # n = no of data points
        # d  = no of features + 1 (for bias)

        self.weights = np.zeros(d)

        best_validation_loss = float('inf')
        wait = 0
        for epoch in range(self.max_epochs):

            print("Running epoch:",epoch+1,"/",self.max_epochs)
            # Shuffle the data
            indices = np.arange(n)
            np.random.shuffle(indices)
            X = X[indices]
            y = y[indices]


            # Split into batches
            for i in range(0, n, self.batch_size):
                X_batch = X[i:i + self.batch_size]
                
                y_batch = y[i:i + self.batch_size]
                

                # Compute the prediction
                y_pred = np.dot(X_batch,self.weights)
                

                # Compute the gradients
                grad_weights = np.dot(X_batch.T, (y_pred - y_batch)) / y_batch.size + self.regularization * self.weights
                
                # Update the weights
                self.weights -= self.learning_rate * grad_weights

                batch_loss = np.mean((y_batch - (np.dot(X_batch,self.weights))) ** 2)
                # print("Validation loss:",validation_loss)
                tup = [[len(self.batch_validation_loss),batch_loss]]
                
                
                self.batch_validation_loss = np.append(self.batch_validation_loss,tup,axis=0)



            # Compute the validation loss
            validation_loss = np.mean((validation_y - (np.dot(validation_x,self.weights))) ** 2)
            # print("Validation loss:",validation_loss)
            # Early stopping
            if validation_loss < best_validation_loss:
                best_validation_loss = validation_loss
                wait = 0
            else:
                wait += 1
                if wait >= self.patience:
                    break
        self.batch_validation_loss = np.delete(self.batch_validation_loss,(0),axis=0)    

        print(self.weights)



    def predict(self, X):
        """Predict using the linear model.

        Parameters
        ----------
        X: numpy.ndarray
            The input data.
        """

        Y = np.dot(X,self.weights)
        print("\nPredicitions: ",Y)
        return Y


    def score(self, X, y):
        """Evaluate the linear model using the mean squared error.

        Parameters
        ----------
        X: numpy.ndarray
            The input data.
        y: numpy.ndarray
            The target data.
        """
        # TODO: Implement the scoring function.
        
        validation_loss = np.mean((y - (np.dot(X,self.weights))) ** 2)
        print("Score: Final validation Loss:",validation_loss)
        return validation_loss


if __name__ == "__main__":
    X = np.array([i for i in range(1,101)])
    X = np.reshape(X,[100,1])
    
    Y = np.array([i*0.1*(random.randint(-1,1))*(random.randint(-5,5)) +2   for i in range(1,101)])
    

    X = np.reshape(Y,[100,1])
    lr = LinearRegression()
    lr.fit(X,Y)
    print("Y original:",Y)
    lr.predict(X)
    lr.score(X,Y)
