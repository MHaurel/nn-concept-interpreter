# Neural Network Concept Interpreter

This repository is the result of an internship at LORIA in Nancy, France.

## Description

Here is a Python software entirely developed by myself with the PyQt library.

The purpose of this software is to find underlying concepts inside the activation values of the different layers of a 
Deep Learning model.

You just have to provide a Tensorflow/Keras model and a .json dataset (for example the one you used to train and test the model) with a column
category in which there would be the concept you want to align the data with.
*You can see examples of datasets in the data folder.* 

## Installation

Before running anything, you may want to install all the dependencies relative to this project.
There is a *requirements.txt* file you can run with the command:
```bash
pip install -r ./requirements.txt
```

The software is not compiled to an .exe file, so you'd have to run it inside a prompt or an IDE, *window.py* being the starting point of the whole project.

## Dataset format



## Infos

This software is the first one I develop in Python (3.10.2) with the PyQt library, so I'd understand if there were any mistakes 
I made.

You're free to fork this project to improve it or give me feedbacks about my work.
