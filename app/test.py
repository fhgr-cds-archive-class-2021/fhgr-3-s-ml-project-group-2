# This is a test file to test/monitor the steps and changes in the main files
from _functions import *
import pandas as pd
import os
import numpy as np

pre_cleaned = pd.read_csv(os.path.join("data", "01_pre_cleaned.csv"), sep=';')
#print(pre_cleaned.isnull().sum())

df_test = createYearPeriods(pre_cleaned, columnName="constructionTime", periodLength=20)
print(df_test.constructionTimePeriod.unique())

train = pd.read_csv('data/02_train.csv', sep=';')
test = pd.read_csv('data/02_test.csv', sep=';')

# define X_train, X_test, y_train, y_test
colsToUse = train.columns.to_list()  # all columns
colsToUse.remove('totalPrice')  # remove target variable (predicting variable)
X_train = train[colsToUse]
X_test = test[colsToUse]
y_train = train["totalPrice"]
y_test = test["totalPrice"]
print("Shape X_train:", X_train.shape)
print("Shape X_test:", X_test.shape)
print("Shape y_train:", y_train.shape)
print("Shape y_test:", y_test.shape)