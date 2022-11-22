import pandas as pd

def modelling(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:

    # define X_train, X_test, y_train, y_test
    colsToUse = train.columns.to_list()  # all columns
    colsToUse.remove('totalPrice')  # remove target variable (predicting variable)
    X_train = train[colsToUse]
    X_test = test[colsToUse]
    y_train = train["totalPrice"]
    y_test = test["totalPrice"]
    

    return None