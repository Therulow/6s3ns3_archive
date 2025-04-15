from Components.package_imports import *
from Components.data_load import load_data_bridge
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def rf_model_prediction_df(date):
    X, y = load_data_bridge(date)
    X_train = X.iloc[:-1, :]
    X_validate = X.iloc[-1, :].values.reshape(1, -1)
    regressor = RandomForestRegressor(n_estimators = 500, n_jobs = 4)
    regressor.fit(X_train, y)
    prediction = regressor.predict(X_validate)
    start_of_this_quarter_date = pd.Period(date, freq='Q').start_time
    df = y.to_frame().rename(columns = {0: "Actual GDP", "pct_chg": "Actual GDP"})
    df["Predicted GDP"] = regressor.predict(X_train)
    if pd.Timestamp(date) == start_of_this_quarter_date:
        df["Actual GDP"].iloc[-1] = np.nan
    df = pd.concat([df, pd.DataFrame({"Actual GDP": [np.nan], "Predicted GDP": prediction}, index = [start_of_this_quarter_date])])
    df.index = pd.to_datetime(df.index).to_period('Q')
    return df



    


    
    

