# data handling
import pandas as pd
import joblib
# machine learning
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
# cuml for GPU (NVIDIA Rapids)
import cuml

def modelling(train: pd.DataFrame) -> pd.DataFrame:
    columns = train.columns.tolist()
    columns.remove("communityAverage")
    columns.remove("totalPrice")
    X_train = train[columns]
    y_train = train['totalPrice']

    # Ensemble learning with XGBRegressor, RandomForest and ElasticNet
    estimators = [
        ("xgboost regressor", XGBRegressor(
            booster="dart",
            eta=0.2,
            max_depth=8,
            min_child_weight=2,
            n_jobs=-1
        )),
        ("RandomFR", cuml.ensemble.RandomForestRegressor(n_estimators=100)),
        ('ENet', cuml.ElasticNet(alpha=0.001))
    ]

    stacking_regressor = StackingRegressor(
        cv=10,
        estimators=estimators, 
        final_estimator=Ridge(alpha=0.01), 
        n_jobs=-1
    )
    stacking_regressor.fit(X_train,y_train)

    joblib.dump(stacking_regressor, "data/04_model.joblib", compress=3)

    return stacking_regressor
