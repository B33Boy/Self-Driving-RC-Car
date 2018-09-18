import numpy as np
import glob
import os
import cv2

# get all .npz files in the folder 'training data'
training_data = glob.glob('./training_data/*.npz')

X = np.zeros((0, 38400))
y = np.zeros((0, 3), 'float')

for input_file in training_data:

    with np.load(input_file) as data:
        X_temp = data['train']
        y_temp = data['train_labels']

    # Get rid of the first rows of each training_data file
    X = np.vstack((X, X_temp[1:]))
    y = np.vstack((y, y_temp[1:]))

X_mirror = X.copy()
y_mirror = y.copy()
numImages = X_mirror.shape[0]

# y_right = np.where(y == [0., 0., 1.])[0]
# print(y_right.shape)
labels = np.identity(3)

for i in range(numImages):

    if not np.array_equal(y_mirror[i], labels[1]):
        # Convert image from (1,38400) to (120, 320), flip it, and convert it back into (1,38400)
        temp = X_mirror[i].reshape(120, 320).astype(np.float32)
        temp = cv2.flip(temp, 1)
        X_mirror[i] = temp.reshape(1, 38400).astype(np.float32)

        # Switch the left and right y values
        y_mirror[i][0], y_mirror[i][2] = y_mirror[i][2], y_mirror[i][0]

directory = "training_data"
if not os.path.exists(directory):
    os.makedirs()
try:
    np.savez(directory + '/' + 'FlippedImages.npz', train=X_mirror, train_labels=y_mirror)
except IOError as e:
    print(e)



