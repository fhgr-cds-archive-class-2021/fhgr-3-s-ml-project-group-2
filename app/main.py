import pandas as pd
import joblib
from _00_pre_population import pre_population
from _01_pre_cleaning import pre_cleaning
from _02_pre_processing import pre_processing
from _03_modelling import modelling
from _04_interpretation import interpretation

original_data = pd.read_csv("../beijing.csv", encoding="gbk", delimiter=",")

#pre_populated = pre_population(original_data)
pre_populated = pd.read_csv('data/00_pre_populated.csv', sep=';')

pre_cleaned = pre_cleaning(pre_populated)
#pre_cleaned = pd.read_csv('data/01_pre_cleaned.csv', sep=';')

train, test = pre_processing(pre_cleaned)  # train and test variables contain a df including the predicting variable (y_train, y_test)
#train = pd.read_csv('data/02_train.csv', sep=';')
#test = pd.read_csv('data/02_test.csv', sep=';')

#model = modelling(train)
model = joblib.load('data/04_model.joblib')

interpretation(model, test)
