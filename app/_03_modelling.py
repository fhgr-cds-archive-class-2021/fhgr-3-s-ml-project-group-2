# data handling
import pandas as pd
# machine learning
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBRegressor

def modelling(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    columns = train.columns.tolist()
    columns.remove("communityAverage")
    columns.remove("totalPrice")
    X_train = train[columns]
    y_train = train['totalPrice']
    X_test = test[columns]
    y_test = test['totalPrice']

    # Ensemble learning with XGBRegressor, RandomForest and Gradient Boosting Regressor
    estimators = [
        ("xgboost regressor", XGBRegressor(
            booster="dart",
            eta=0.2,
            max_depth=9,
            min_child_weight=2,
            n_jobs=-1
        )),
        ("RandomFR", RandomForestRegressor(n_estimators=200, n_jobs=-1)),
        ("Gradient Boosting", HistGradientBoostingRegressor()),
    ]

    stacking_regressor = StackingRegressor(estimators=estimators, final_estimator=RidgeCV(), n_jobs=-1)
    stacking_regressor.fit(X_train,y_train)

    y_pred = stacking_regressor.predict(X_test) # Make predictions using the testing set
    
    print("\nMean absolute error: %.2f" % mean_absolute_error(y_test, y_pred))  # The mean absolute error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))  # The mean squared error
    print("Coefficient of determination (R^2): %.2f" % r2_score(y_test, y_pred))  # The coefficient of determination: 1 is perfect prediction

    return stacking_regressor