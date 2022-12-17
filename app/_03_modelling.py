# data handling
import pandas as pd
import joblib
# machine learning
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def modelling(train: pd.DataFrame) -> pd.DataFrame:
    columns = train.columns.tolist()
    columns.remove("communityAverage")
    columns.remove("totalPrice")
    X_train = train[columns]
    y_train = train['totalPrice']

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

    joblib.dump(stacking_regressor, "data/04_model.joblib", compress=3)

    return stacking_regressor