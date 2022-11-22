# This is a test file to test/monitor the steps and changes in the main files
from _functions import *
import pandas as pd
import os
import numpy as np

pre_cleaned = pd.read_csv(os.path.join("data", "01_pre_cleaned.csv"), sep=';')
#print(pre_cleaned.isnull().sum())

test = createYearPeriods(pre_cleaned, columnName="constructionTime")
print(test.constructionTimePeriod)