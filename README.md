# Self-Driving-RC-Car

This project is based on [Hamuchiwa's AutoRCCar]{https://github.com/hamuchiwa/AutoRCCar} project.

## Project Structure 
    arduino/
        rc_keyboard-control/ 
            rc_keyboard_control.ino - Contains the file to flash onto the Arduino
    
    computer/
        Tests/                          - Contains Tests
            MirrorTest.ipynb            - Test for generating more data by mirroring images in x direction
            ParseDataTest.ipynb         - Test for parsing the data (used when training the model)
            keyboard_control.py         - Testing teleoperation via keyboard control 
            stream_test.py              - Test the rpi's streaming capabilites
            check_data_test.py  - 
        chess_board/                    - Contains images for camera correction 
        deepln_h5/                      - Contains final trained neural network h5 files
        training_data/                  - Contains npz files containing traning data images, and one-hot encoded output labels
        collect_calibration_images.py   - Collect the images needed for camera calibration and save to chess_board/ 
        collect_training_data.py        - Collect training data and save to the training_data/
        colour_detection_trackbar.py    - Not Needed
        generate_more_data.py           - Generates more data by flipping images and labels in x direction 
        model.py                        - Deep learning model in Keras
        picam_calibration.py 	        - Calibration script for the picamera
        self_driver.py                  - Script to drive the car by itself
        self_driver_helper.py           - Aids the self_driver.py file with useful classes
      
    raspberry_pi/
        ultrasonic_client.py            - Sends ultrasonic data over tcp
        video_client.py                 - Sends images from picam to server
        

## Deep Learning Problem
Problem Definition: The model will predict the correct keypress to move the car given a live video feed.
Inputs: list of 120x320 images (unrolled), list of 1x3 one-hot-encoded labels that determine the direction to turn
Type of problem: multiclass single-label classification where each input image should be categorized into one of the following:
[1 0 0], [0 1 0], [0 0 1].

Metric: accuracy
Evaluation protocol: Validation Accuracy
Because the problem is a multiclass single-label classification problem, our last layer activation function is softmax, and our loss function is binary cross-entropy
