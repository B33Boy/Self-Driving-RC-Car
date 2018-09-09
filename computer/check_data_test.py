import numpy as np
import glob

f = glob.glob('/')
print(f)
# get all .npz files in the folder 'training data'
training_data = glob.glob('training_data/*.npz')
X = np.zeros((1, 38400))
y = np.zeros((1, 3), 'float')

print("input_data_path: ", training_data)

for input_file in training_data:

    with np.load(input_file) as data:
        X_temp = data['train']
        y_temp = data['train_label']

    X = np.vstack((X, X_temp))
    y = np.vstack((y, y_temp))

# Get rid of the first rows in both matrices that only contain zeros
X = X[1:, :]
y = y[1:, :]

print(X)
print(" |||")
print(y)
