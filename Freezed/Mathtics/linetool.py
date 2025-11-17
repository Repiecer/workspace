from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
x = [2, 3, 6, 8, 7, 12, 36, 55]
y = [3, 4, 7, 9, 10 ,13, 38, 57]
x = np.array(x).reshape(-1, 1)
y = np.array(y).reshape(-1, 1)
lineObj = LinearRegression()
lineObj.fit(x, y)
print(lineObj.coef_, lineObj.intercept_)
y_predict = lineObj.predict(x)
print(mean_squared_error(y, y_predict))

