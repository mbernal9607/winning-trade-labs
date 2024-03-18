import pandas as pd
from sklearn.linear_model import LinearRegression
from regressors import stats
import numpy as np

def regresion(close_price, cantidad, max_p_value):
    try:
        y = close_price
        mins = pd.Series(range(1,cantidad+1))
        X_df = pd.DataFrame(mins,columns= ['x'])
        # Convertir a una lista de listas
        X = X_df[['x']]
        modelo = LinearRegression()
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        regresion_robot = modelo.fit(X,y)

        pendiente = regresion_robot.coef_
        p_valor = stats.coef_pval(regresion_robot,X,y)

        if pendiente[0] > 0 and p_valor[1] <= max_p_value:
            var_ind = 1
        elif pendiente[0] < 0 and p_valor[1] <= max_p_value:
            var_ind = 2
        else:
            var_ind = 0
            
        return var_ind
    except Exception as err:
        return {
            "message": err,
            "error": True
        }