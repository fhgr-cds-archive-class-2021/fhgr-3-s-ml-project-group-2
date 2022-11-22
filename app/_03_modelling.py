# data handling
import pandas as pd
# machine learning
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV

def modelling(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:

    # define X_train, X_test, y_train, y_test
    colsToUse = train.columns.to_list()  # all columns
    colsToUse.remove('totalPrice')  # remove target variable (predicting variable)
    X_train = train[colsToUse]
    X_test = test[colsToUse]
    y_train = train["totalPrice"]
    y_test = test["totalPrice"]
    

    # define and fit machine learning model
    linearRegression = linear_model.LinearRegression()  # create linear regression
    multipleLinearRegression = linearRegression.fit(X_train,y_train)

    y_pred= multipleLinearRegression.predict(X_test)  # Make predictions using the testing set
    print("\nMean absolute error: %.2f" % mean_absolute_error(y_test, y_pred))  # The mean absolute error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))  # The mean squared error
    print("Coefficient of determination (R^2): %.2f" % r2_score(y_test, y_pred))  # The coefficient of determination: 1 is perfect prediction


    # define final model
    model = multipleLinearRegression

    return model