import numpy as np
import glob
import time

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD


#get all .npz files in the folder 'training data'
input_data_path = glob.glob('training_data/*.npz')
X = np.zeros((1, 38400))
y = np.zeros((1, 3), 'float')

for input_file in input_data_path:

    with np.load(input_file) as data:
        X_temp = data['train']
        y_temp = data['train_label']

    X = np.vstack((X, X_temp))
    y = np.vstack((y, y_temp))

# Get rid of the first rows in both matrices that only contain zeros
X = X[1:,:]
y = y[1:,:]

# We use feature scaling to make gradient descent faster because we are dealing with smaller values
# Divide by 255 to get values between 0 and 1
X = X / 255.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# define model
model = Sequential()
training_start =time.time()
print("Training data...")
model.add(Dense(30, input_dim=38400, init='uniform'))
model.add(Dropout(0.2))
model.add(Activation('relu'))
model.add(Dense(3, init='uniform'))
model.add(Activation('softmax'))

# Stochastic gradient descent
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, batch_size=128)


training_finish = time.time() - training_start

#Evaluate on test set
score = model.evaluate(X_test, y_test, batch_size=128)
print("loss={}, accuracy={} ".format(score[0], score[1]))

# Save model as h5
timestr = time.strftime('%Y%m%d_%H%M%S')
filename_timestr = 'nn_{}.h5'.format(timestr)
model.save('nn_h5/nn_{}.h5'.format(timestr))
