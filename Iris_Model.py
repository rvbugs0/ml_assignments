from sklearn.datasets import load_iris
import numpy as np
from LinearRegression import LinearRegression
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8.0, 6.0)

iris = load_iris()
iris_data = iris["data"]

# attributes - Sepal Length, Sepal Width, Petal Length, Petal Width
sepal_length = np.reshape(iris_data[:,0],(iris_data.shape[0],1))
sepal_width = np.reshape(iris_data[:,1],(iris_data.shape[0],1))
petal_length = np.reshape(iris_data[:,2],(iris_data.shape[0],1))
petal_width = np.reshape(iris_data[:,3],(iris_data.shape[0],1))

# Shuffle the data
n= iris_data.shape[0]
indices = np.arange(n)
np.random.shuffle(indices)

# setting aside 10% of data for testing
upperbound = int(n * 0.9)

training_set_indices = indices[:upperbound]
testing_set_indices = indices[upperbound:]

patience_for_all = 3

print("\n\nCombination-1 : Predicting the petal width given petal length and sepal width")
model1 = LinearRegression(learning_rate=0.0005,patience=patience_for_all)

sepal_width_training = sepal_width[training_set_indices]
petal_length_training = petal_length[training_set_indices]

X_input = np.concatenate((sepal_width_training,petal_length_training),axis=1)
Y_input = np.squeeze(np.copy(petal_width)[training_set_indices])


# fitting model-1
model1.fit(X_input,Y_input)

X_test_input = np.concatenate((sepal_width[testing_set_indices],petal_length[testing_set_indices]),axis=1)
Y_test_input = np.squeeze(np.copy(petal_width[testing_set_indices]))


model1.score(X_test_input,Y_test_input)

print("\nTarget Values:",Y_test_input)
model1.predict(X_test_input)

x_plot = model1.batch_validation_loss[:,0]
y_plot = model1.batch_validation_loss[:,1]
plt.scatter(x_plot, y_plot)
plt.show()

print("\n\n###############################################################################################\n\n")


print("Combination-2 : Predicting the petal width given petal length:")

model2 = LinearRegression(learning_rate=0.0005,patience=patience_for_all)

# sepal_width_training = np.copy(sepal_width)[training_set_indices]
petal_length_training = np.copy(petal_length)[training_set_indices]

X_input = petal_length_training
Y_input = np.squeeze(np.copy(petal_width)[training_set_indices])

# fitting model-2
model2.fit(X_input,Y_input)

X_test_input = np.copy(petal_length[testing_set_indices])
Y_test_input = np.squeeze(np.copy(petal_width[testing_set_indices]))

model2.score(X_test_input,Y_test_input)

print("\nModel-2 Target Values:",Y_test_input)

model2.predict(X_test_input)
x_plot = model2.batch_validation_loss[:,0]
y_plot = model2.batch_validation_loss[:,1]
plt.scatter(x_plot, y_plot)
plt.show()


print("\n\n###############################################################################################\n\n")


print("Combination-2-modified : Adding regularization")
print("Model-2: Regularization added")
model2 = LinearRegression(learning_rate=0.0005,regularization=0.1,patience=patience_for_all)
# fitting model-2
model2.fit(X_input,Y_input)
model2.score(X_test_input,Y_test_input)
print("\nTarget Values:",Y_test_input)
model2.predict(X_test_input)
x_plot = model2.batch_validation_loss[:,0]
y_plot = model2.batch_validation_loss[:,1]
plt.scatter(x_plot, y_plot)
plt.show()

print("\n\n###############################################################################################\n\n")


print("Combination-3 : Predicting the petal width given petal length, sepal length and sepal width:") 
model3 = LinearRegression(learning_rate=0.0005,patience=patience_for_all)

sepal_width_training = np.copy(sepal_width)[training_set_indices]
petal_length_training = np.copy(petal_length)[training_set_indices]
sepal_length_training = np.copy(sepal_length)[training_set_indices]

X_input = np.concatenate((sepal_width_training,petal_length_training),axis=1)
X_input = np.concatenate((sepal_length_training,X_input),axis=1)
Y_input = np.squeeze(np.copy(petal_width)[training_set_indices])

# fitting model-3
model3.fit(X_input,Y_input)


sepal_width_testing = np.copy(sepal_width[testing_set_indices])
petal_length_testing = np.copy(petal_length)[testing_set_indices]
sepal_length_testing = np.copy(sepal_length)[testing_set_indices]


X_test_input = np.concatenate((sepal_width_testing,petal_length_testing),axis=1)
X_test_input = np.concatenate((sepal_length_testing,X_test_input),axis=1)


Y_test_input = np.squeeze(np.copy(petal_width[testing_set_indices]))

model3.score(X_test_input,Y_test_input)

print("\nModel-3 Target Values:",Y_test_input)

model3.predict(X_test_input)
x_plot = model3.batch_validation_loss[:,0]
y_plot = model3.batch_validation_loss[:,1]
plt.scatter(x_plot, y_plot)
plt.show()



print("\n\n###############################################################################################\n\n")

print("Combination-4: Predicting the sepal width given sepal length")
model4 = LinearRegression(learning_rate=0.0005,patience=patience_for_all)

sepal_length_training = sepal_length[training_set_indices]

X_input = sepal_length_training
Y_input = np.squeeze(np.copy(sepal_width)[training_set_indices])

# fitting model-4
model4.fit(X_input,Y_input)


sepal_length_testing = np.copy(sepal_length)[testing_set_indices]


X_test_input = sepal_length_testing
Y_test_input = np.squeeze(sepal_width[testing_set_indices])

model4.score(X_test_input,Y_test_input)

print("\nModel-4 Target Values:",Y_test_input)

model4.predict(X_test_input)

x_plot = model4.batch_validation_loss[:,0]
y_plot = model4.batch_validation_loss[:,1]
plt.scatter(x_plot, y_plot)
plt.show()

