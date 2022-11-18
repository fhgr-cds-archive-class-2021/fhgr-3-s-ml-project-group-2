from _01_pre_cleaning import pre_cleaning
from _02_pre_processing import pre_processing
from _03_modelling import modelling

# pre_cleaning()
train, test = pre_processing()
results = modelling(train, test)