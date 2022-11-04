import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

class ConvertDateToTimestampTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for col in X.columns:
            X[col] = pd.to_datetime(X[col]).astype(int)/ 10**9
        return X

class FixLivingRoomTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def mapper(x):
            if x == '#NAME?':
                return np.nan
            else: return int(x)
        for col in X.columns:
            X[col] = X[col].apply(mapper)
        return X 

class FixDrawingRoomTransformer(BaseEstimator, TransformerMixin):
    chars = ['中', '低', '底', '顶', '高']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def mapper(x):
            for c in self.chars:
                if c in str(x):
                    return np.nan
            return int(x)
        for col in X.columns:
            X[col] = X[col].apply(mapper)
        return X

class FixBathRoomTransformer(BaseEstimator, TransformerMixin):
    chars = ['未知']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def mapper(x):
            for c in self.chars:
                if c in str(x):
                    return np.nan
            return int(x)
        for col in X.columns:
            X[col] = X[col].apply(mapper)
        return X

def get_preprocessing():
    return ColumnTransformer([
        ('convert_date_to_timestamp', ConvertDateToTimestampTransformer(), ['tradeTime']),
        ('fix_living_room', FixLivingRoomTransformer(), ['livingRoom']),
        ('impute_living_room', SimpleImputer(missing_values=np.nan, strategy='most_frequent'), ['livingRoom']),
        ('fix_drawing_room', FixDrawingRoomTransformer(), ['drawingRoom']),
        ('impute_drawing_room', SimpleImputer(missing_values=np.nan, strategy='most_frequent'), ['drawingRoom']),
        ('fix_bath_room', FixBathRoomTransformer(), ['bathRoom']),
        ('impute_bath_room', SimpleImputer(missing_values=np.nan, strategy='most_frequent'), ['bathRoom'])
        # columns that are repeated in transformer pipeline will be duplicated since paralell
    ], remainder='passthrough')