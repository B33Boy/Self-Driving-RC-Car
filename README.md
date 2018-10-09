# Self-Driving-RC-Car

## Deep Learning Problem
Problem Definition: The model will predict the correct keypress to move the car given a live video feed.
Inputs: list of 120x320 images (unrolled), list of 1x3 one-hot-encoded labels that determine the direction to turn
Type of problem: multiclass single-label classification where each input image should be categorized into one of the following:
[1 0 0], [0 1 0], [0 0 1].

Metric: accuracy
Evaluation protocol: Validation Accuracy
Because the problem is a multiclass single-label classification problem, our last layer activation function is softmax, and our loss function is binary cross-entropy


## Project Structure

arduino/
    rc_keyboard-control/ 
        rc_keyboard_control.ino - Contains the file to flash onto the Arduino
    
computer/
    Tests/                  - Contains Tests
        MirrorTest.ipynb    - Test for generating more data by mirroring images in x direction
        ParseDataTest.ipynb - Test for parsing the data (used when training the model)
        keyboard_control.py - Testing teleoperation via keyboard control 
        stream_test.py      - Test the rpi's streaming capabilites
    chess_board/            - Contains images for camera correction 
    deepln_h5/              - Contains final trained neural network h5 files
    training_data/          - Contains npz files containing traning data images, and one-hot encoded output labels
        
        
  

  
