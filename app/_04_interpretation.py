from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def interpretation(model, test):
    columns = test.columns.tolist()
    columns.remove("communityAverage")
    columns.remove("totalPrice")
    X_test = test[columns]
    y_test = test['totalPrice']

    y_pred = model.predict(X_test) # Make predictions using the testing set
    print("\nMean absolute error: %.2f" % mean_absolute_error(y_test, y_pred))  # The mean absolute error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))  # The mean squared error
    print("Coefficient of determination (R^2): %.2f" % r2_score(y_test, y_pred))  # The coefficient of determination: 1 is perfect prediction
