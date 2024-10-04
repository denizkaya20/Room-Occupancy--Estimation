# Room Occupancy  Estimation
IoT Room Occupancy Detection Using ML Techniques

Project Overview:

This project focuses on detecting room occupancy using IoT (Internet of Things) sensors and applying various machine learning (ML) techniques to analyze the data. The sensors measure parameters such as temperature, light, sound, CO2, and movement, which are used to estimate the number of people in a room.

Dataset:

The dataset used for this project was sourced from the UCI Machine Learning Repository. It includes data from 7 sensors and spans 4 days of controlled measurements. The dataset consists of 10,129 rows and 19 columns, capturing environmental sensor readings such as temperature, light, sound, and CO2 levels, along with the room occupancy.

Source: UCI Repository

Methods:
The machine learning models used in this project include:

Decision Tree (DT)
Random Forest (RF)
K-Nearest Neighbors (KNN)
Support Vector Machine (SVM)
The dataset was split into training and test sets (85% training, 15% test) and normalized using Min-Max scaling. Hyperparameter tuning was performed for each model to avoid overfitting.

Results:

The performance of the models was evaluated using F1-score and accuracy:

Decision Tree: F1-score 98%, Accuracy 98%
Random Forest: F1-score 99%, Accuracy 99%
K-Nearest Neighbors: F1-score 99%, Accuracy 99%
Support Vector Machine: F1-score 98%, Accuracy 98%
Cross-validation using Stratified K-Fold (n_splits=5) was also performed, with the SVM model achieving the highest cross-validation score (97%).

Conclusion:

The Support Vector Machine (SVM) model provided the best classification performance for detecting room occupancy based on IoT sensor data. This project highlights the effectiveness of combining IoT data with machine learning techniques to improve energy efficiency and resource management in smart buildings.

How to Run:

Install the required libraries using pip install -r requirements.txt.
Download the dataset from the UCI repository.
Run the provided Python code (link below) for data preprocessing, model training, and evaluation.
