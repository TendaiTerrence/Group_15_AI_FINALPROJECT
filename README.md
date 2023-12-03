# Group_15_AI_FINALPROJECT

Face Emotion Recognition Model
This project innovates a music recommendation system by integrating facial emotion recognition technology with advanced Convolutional Neural Networks (CNNs). It's not just about analyzing user preferences; it dives into understanding the user's emotional state for more resonant music selections. This approach fills a gap in traditional music recommendation systems by prioritizing the emotional connection, aiming for a more empathetic and personalized listening experience.

Introduction
The goal is to create a human emotion recognition model using facial expressions. The project tackles data imbalance in emotion classes by downsampling overrepresented classes to improve model accuracy.

Key Processes

Mounting the Drive: Setting up the necessary file system.
Reading and Checking Image Shapes: Ensuring data uniformity.
Loading Training and Testing Data: Organizing the dataset for model training and evaluation.
Displaying Images from Emotion Classes: Visual analysis of each emotion category.
Data Balance Analysis: Evaluating the distribution of data among different emotion classes.

Installation
Begin by importing the required libraries:

import tensorflow
import cv2
import os
import matplotlib.pyplot
import numpy
import os
import random
import sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras import models
from sklearn.metrics import roc_curve, accuracy_score, roc_auc_score


Preparing Input Data: Format your data to align with the model's input requirements.

Making Predictions: Use the model to predict emotions from facial expressions.
Interpreting the Output: Analyze the model's output to understand the recognized emotions.

Conclusion
This project represents a technological leap, blending emotional intelligence with algorithms to redefine how users experience music based on their current mood. It's a testament to the synergy of technology and human emotion in enhancing user experiences.
