# -*- coding: utf-8 -*-
"""Room_Occupancy_Estimation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P_CKU3OfOGjCiHB4GuROWcsWCXsicDZf
"""

from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import requests
import zipfile
import io
import pandas as pd
import requests
import zipfile
import io
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import svm as svm
from sklearn import tree
from sklearn.preprocessing import MinMaxScaler

# Path to your downloaded CSV file
csv_file_path = '/content/drive/MyDrive/İstatistiksel_Veri_Analizi_Proje/Occupancy_Estimation.csv'  # Replace with your actual file path

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_file_path)

# Printing the head of the data
print(data.head())

# Searching for missing values
print(data.isnull().sum())

# Descriptive Statistics
a1 = ["S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp"]
b1 = data[a1]
print(b1.describe().T)

a2 = ["S1_Light", "S2_Light", "S3_Light", "S4_Light"]
b2 = data[a2]
print(b2.describe().T)

a3 = ["S1_Sound", "S2_Sound", "S3_Sound", "S4_Sound"]
b3 = data[a3]
print(b3.describe().T)
a4 = ["S5_CO2", "S5_CO2_Slope"]
b4 = data[a4]
print(b4.describe())

# Setting Feature
features = ["S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp", "S1_Light", "S2_Light", "S3_Light", "S4_Light", "S1_Sound", "S2_Sound", "S3_Sound", "S4_Sound", "S5_CO2", "S5_CO2_Slope", "S6_PIR", "S7_PIR", "Room_Occupancy_Count"]
data = data[features]

# Drawing occupancy plot
sns.set_theme(style='darkgrid', palette='pastel', rc={'figure.figsize': (8, 6)})
ax = sns.countplot(x=data.Room_Occupancy_Count)
for container in ax.containers: ax.bar_label(container)
ax.set(title='Distrubition of Room Occupancy')
# plt.show()

# Histograms of Temperatures
sns.set(style="whitegrid")
fig, axs = plt.subplots(1, 4, figsize=(10, 5))
sns.histplot(data=data, x="S1_Temp", kde=True, color="skyblue", ax=axs[0])
plt.xlabel('S1_Temp')
sns.histplot(data=data, x="S2_Temp", kde=True, color="olive", ax=axs[1])
sns.histplot(data=data, x="S3_Temp", kde=True, color="gold", ax=axs[2])
sns.histplot(data=data, x="S4_Temp", kde=True, color="teal", ax=axs[3])
fig.tight_layout()
fig.suptitle(' Histogram of Temperature(Celsius) ', fontsize=14, y=1.0001) # plt.show() # Histograms of Lights fig, axs = plt.subplots(1, 4, figsize=(10, 5))
sns.histplot(data=data, x="S1_Light", kde=True, color="teal", ax=axs[0])

sns.histplot(data=data, x="S2_Light", kde=True, color="blue", ax=axs[1])
sns.histplot(data=data, x="S3_Light", kde=True, color="purple", ax=axs[2])
sns.histplot(data=data, x="S4_Light", kde=True, color="red", ax=axs[3])
fig.tight_layout()
fig.suptitle(' Histogram of Light(Lux) ', fontsize=14, y=1.0001) # plt.show()

# Histograms of Sounds
fig, axs = plt.subplots(1, 4, figsize=(10, 5))
sns.histplot(data=data, x="S1_Sound", kde=True, color="purple", ax=axs[0])
sns.histplot(data=data, x="S2_Sound", kde=True, color="black", ax=axs[1])
sns.histplot(data=data, x="S3_Sound", kde=True, color="red", ax=axs[2])
sns.histplot(data=data, x="S4_Sound", kde=True, color="blue", ax=axs[3])
fig.tight_layout()
fig.suptitle(' Histogram of Sound(Volts) ', fontsize=14, y=1.0001)
# plt.show()

# Histograms of Sound CO2s
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
sns.histplot(data=data, x="S5_CO2", kde=True, color="green", ax=axs[0])
sns.histplot(data=data, x="S5_CO2_Slope", kde=True, color="red", ax=axs[1])
fig.tight_layout()
fig.suptitle(' Histogram of CO2 (PMP/Slope) ', fontsize=14, y=1.0001) # plt.show()

# Correlation between features with masking
corr = data.corr()
f, ax = plt.subplots(figsize=(15, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
ax = sns.heatmap(corr, annot=True, mask=mask, cmap=cmap, fmt=".3f", linewidth=.5)
ax.tick_params(axis='x', labelsize=8, rotation=22)
ax.tick_params(axis='y', labelsize=8)
ax.set_title("Correlation Between Features", fontsize=14) # plt.show()

# Prepare data for modelling
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
feature_cols = ["S1_Temp", "S2_Temp", "S3_Temp", "S4_Temp", "S1_Light", "S2_Light", "S3_Light", "S4_Light", "S1_Sound", "S2_Sound", "S3_Sound", "S4_Sound", "S5_CO2", "S5_CO2_Slope", "S6_PIR", "S7_PIR"]
X = data[feature_cols]
y = data.Room_Occupancy_Count

# Split data as train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15, random_state=0)

# Use MinMaxScaler to scale the data
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_cv = scaler.fit_transform(X)

# Models for data
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, accuracy_score, make_scorer
from yellowbrick.model_selection import FeatureImportances

# DT Classifier
print(f'Model: Decision Tree \n--------------')
# For Classification Problem StratifiedKFold
from sklearn.model_selection import cross_val_score
DT = DecisionTreeClassifier(criterion="gini", min_samples_split=50, random_state=0, max_depth=10, min_samples_leaf=50, class_weight='balanced')
DT.fit(X_train_scaled, y_train)
y_pred_DT = DT.predict(X_test_scaled)
skf = StratifiedKFold(n_splits=10)
scores = cross_val_score(DT, X_cv, y, cv=skf,scoring='accuracy')
print(f"Score: ", '{:.3f}'.format(scores.mean()))

# Classification Report for DT
print(f'Classification Report: \n{classification_report(y_test, y_pred_DT,digits=4)}')
# Confusion Matrix for DT
cm = confusion_matrix(y_test, y_pred_DT, labels=DT.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp = disp.plot(cmap=plt.cm.Blues)
plt.grid(False)
plt.title('Confusion Matrix for Decision Tree')
plt.show() # Feature Importance in every models visualizer = FeatureImportances(DT) visualizer.fit(X_train, y_train) visualizer.show()

# Feature Importance in every models
visualizer = FeatureImportances(DT)
visualizer.fit(X_train, y_train)
visualizer.show()
# RF Classifier
RF = RandomForestClassifier(criterion='gini', min_samples_split=50, random_state=0, max_depth=10, min_samples_leaf=50, class_weight='balanced')
print(f'Model: Random Forest \n--------------')
RF.fit(X_train_scaled, y_train)
y_pred_RF = RF.predict(X_test_scaled)

# For Classification Problem StratifiedKFold
from sklearn.model_selection import cross_val_score
skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(RF, X_cv, y, cv=skf, scoring='accuracy')
print(f"Score Mean: ", scores.mean())

# Confusion Matrix for RF
cm = confusion_matrix(y_test, y_pred_RF, labels=RF.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp = disp.plot(cmap=plt.cm.Greens)
plt.grid(False)
plt.title('Confusion Matrix for Random Forest')
plt.show()

# Classification Report for RF
print(f'Classification Report: \n{classification_report(y_test, y_pred_RF,digits=4)}')
# Feature Importance in every models
visualizer = FeatureImportances(RF)
visualizer.fit(X_train, y_train)
visualizer.show()

# KNN Classifier
KNN = KNeighborsClassifier(n_neighbors=5, algorithm='kd_tree', metric='minkowski', p=2, leaf_size=30)
print(f'Model: K-Nearest Neighbors \n--------------')
KNN.fit(X_train_scaled, y_train)
y_pred_KNN = KNN.predict(X_test_scaled)

# For Classification Problem StratifiedKFold
from sklearn.model_selection import cross_val_score
skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(RF, X_cv, y, cv=skf,scoring='accuracy')
print(f"Score Mean: ", scores.mean())

# K value Mean error
error=[]
for i in range(1, 40):
  knn = KNeighborsClassifier(n_neighbors=i, algorithm='kd_tree', metric='minkowski', p=2, leaf_size=30)
  knn.fit(X_train_scaled, y_train)
  pred_i = knn.predict(X_test_scaled)
  error.append(np.mean(pred_i != y_test))
plt.figure(figsize=(12, 6))
plt.plot(range(1, len(error) + 1), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')

# Confusion Matrix for KNN
cm = confusion_matrix(y_test, y_pred_KNN, labels=KNN.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp = disp.plot(cmap=plt.cm.Purples)
plt.grid(False)
plt.title('Confusion Matrix for K-Nearest Neighbors')
plt.show() # Classification Report for KNN print(f'Classification Report: \n{classification_report(y_test, y_pred_KNN,digits=4)}')

# SVM Classifier
SVM = SVC(kernel='linear', random_state=0)
print(f'Model: Support Vector Machine \n--------------')
SVM.fit(X_train_scaled, y_train)
y_pred_SVM = SVM.predict(X_test_scaled)

# For Classification Problem StratifiedKFold
from sklearn.model_selection import cross_val_score
skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(SVM, X_cv, y, cv=skf, scoring='accuracy')
print(f"Score Mean: ", (scores.mean()))

# Confusion Matrix for SVM
cm = confusion_matrix(y_test, y_pred_SVM, labels=SVM.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp = disp.plot(cmap=plt.cm.Reds)
plt.grid(False)
plt.title('Confusion Matrix for Support Vector Machine')
plt.show()

# Classification Report for SVM
print(f'Classification Report: \n{classification_report(y_test, y_pred_SVM,digits=4)}')