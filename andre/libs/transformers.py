import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

class DropColumnsTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.drop(columns=X.columns)

class ConvertDateToTimestampTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for col in X.columns:
            X[col] = pd.to_datetime(X[col]).astype(int)/ 10**9
        return X

class CreateIDTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X['id'] = X.index + 1
        return X

class FixLivingRoomTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def mapper(x):
            if x == '#NAME?':
                return np.nan
            else: return int(x)
        X['livingRoom'] = X['livingRoom'].apply(mapper)
        return X

def get_preprocessing():
    return ColumnTransformer([
        ('drop_columns_with_no_use', DropColumnsTransformer(), ['url']),
        ('convert_date_to_timestamp', ConvertDateToTimestampTransformer(), ['tradeTime']),
        ('create_id', CreateIDTransformer(), ['id']),
        ('fix_living_room', FixLivingRoomTransformer(), ['livingRoom']),
        ('impute_living_room', SimpleImputer(missing_values=np.nan, strategy='most_frequent'), ['livingRoom'])
    ], remainder='passthrough')