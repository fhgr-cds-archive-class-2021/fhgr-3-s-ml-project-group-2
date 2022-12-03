# custom defined functions
from _functions import *
# standard libraries
from typing import Tuple

# data handling
import pandas as pd
import numpy as np
from scipy.stats import shapiro
from scipy.stats import randint
from feature_engine.imputation import MeanMedianImputer
from feature_engine.imputation import CategoricalImputer
from feature_engine.encoding import CountFrequencyEncoder, RareLabelEncoder
from feature_engine.encoding import OneHotEncoder as fe_OneHotEncoder
from feature_engine.selection import DropConstantFeatures, DropDuplicateFeatures
from feature_engine.selection import DropCorrelatedFeatures, SmartCorrelatedSelection

# machine learning
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV

def pre_processing(pre_cleaned: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # define pre_cleaned df
    df = pre_cleaned
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)  # drop unnamed column (index column) if exists

    
    # create time periods for constructionTime column (grouped by a specific range of years)
    df = createYearPeriods(df, columnName="constructionTime", periodLength=20)  # -> create new column: constructionTimePeriod 
    df.drop(['constructionTime'], axis=1, inplace=True)  # remove old constructionTime column

    
    # train/test split
    colsToUse = df.columns.to_list()  # all columns
    colsToUse.remove('totalPrice')  # remove target variable (predicting variable)

    X_train, X_test, y_train, y_test = train_test_split(
        df[colsToUse],
        df['totalPrice'],  # target
        test_size=0.3,
        random_state=6)

    # define categorical columns and set datatype
    categoricalColumns = ["floorType", "buildingType", "renovationCondition", "buildingStructure", "constructionTimePeriod", "town", "placeRank"]
    for category in categoricalColumns:  # change dtype of categorical columns to object dtype for later processing
        def numeric_to_string_mapper(x):
            if type(x) == float or type(x) == int:
                if x is not np.nan:
                    return str(x)
                else:
                    return np.nan
            return x
        X_train[category] = X_train[category].apply(numeric_to_string_mapper)
        X_test[category] = X_test[category].apply(numeric_to_string_mapper)
        X_train[category] = X_train[category].astype("object")
        X_test[category] = X_test[category].astype("object")

    # missing value imputation pipeline
    transformationsPipe = Pipeline([  # Define the pipeline
        ('median_imputer', MeanMedianImputer(imputation_method='median', variables=['communityAverage', 'districtPopulation', 'districtArea'])),
        ('frequent_category_imputer', CategoricalImputer(imputation_method='frequent', variables=['buildingType', 'constructionTimePeriod', 'town', 'placeRank'])),
        ('rare_label_encoder', RareLabelEncoder(n_categories=2, variables=categoricalColumns)),
        ('count_frequency_encoder', CountFrequencyEncoder(encoding_method='count', variables=categoricalColumns)),
    ])

    transformationsPipe.fit(X_train)
    X_train = transformationsPipe.transform(X_train)
    X_test = transformationsPipe.transform(X_test)

    # create final preprocessed df
    trainDF = X_train.copy()
    trainDF["totalPrice"] = y_train  # Add label / predicting variable

    testDF = X_test.copy()
    testDF["totalPrice"] = y_test  # Add label / predicting variable

    # write csv
    trainDF.to_csv(path_or_buf='data/02_train.csv', sep=';', index=False)
    testDF.to_csv(path_or_buf='data/02_test.csv', sep=';', index=False)

    return trainDF, testDF
