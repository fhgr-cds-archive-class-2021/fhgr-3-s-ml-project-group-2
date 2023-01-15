import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def interpretation(model, train, test):
    columns = test.columns.tolist()
    columns.remove("communityAverage")
    columns.remove("totalPrice")
    X_train = train[columns]
    y_train = train['totalPrice']
    X_test = test[columns]
    y_test = test['totalPrice']

    y_test_pred = model.predict(X_test.to_numpy())
    y_train_pred = model.predict(X_train.to_numpy())

    rows = [
        [
            "test", 
            r2_score(y_test.to_numpy(), y_test_pred),
            mean_absolute_error(y_test.to_numpy(), y_test_pred), 
            mean_squared_error(y_test.to_numpy(), y_test_pred), 
            np.sqrt(mean_squared_error(y_test.to_numpy(), y_test_pred)),
            np.max(np.abs(y_test_pred - y_test.to_numpy())),
            np.min(y_test.to_numpy()),
            np.average(y_test.to_numpy()),
            np.std(y_test.to_numpy()),
            np.max(y_test.to_numpy()),
        ],
        [
            "train", 
            r2_score(y_train.to_numpy(), y_train_pred),
            mean_absolute_error(y_train.to_numpy(), y_train_pred), 
            mean_squared_error(y_train.to_numpy(), y_train_pred), 
            np.sqrt(mean_squared_error(y_train.to_numpy(), y_train_pred)),
            np.max(np.abs(y_train_pred - y_train.to_numpy())),
            np.min(y_train.to_numpy()),
            np.average(y_train.to_numpy()),
            np.std(y_train.to_numpy()),
            np.max(y_train.to_numpy()),
        ],
    ]
    predDf = pd.DataFrame(rows, columns=["Dataset", "R2", "MAE", "MSE", "RMSE", "Max_Error", "Min", "Avg", "Std", "Max"])
    print(predDf)
