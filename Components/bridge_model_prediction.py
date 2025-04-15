from Components.package_imports import *
from Components.data_load import load_data_bridge
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def bridge_model_prediction_df(date):
    X, y = load_data_bridge(date)
    X_= sm.add_constant(X)    
    X_test = X.iloc[-1, :]
    X_train = X.iloc[:-1, :]
    model = sm.OLS(y, X_train).fit()

    start_of_this_quarter_date = pd.Period(date, freq='Q').start_time
    predicted_values = pd.concat([model.fittedvalues, pd.Series(model.predict(X_test)[0], index = [start_of_this_quarter_date])]).to_frame().rename(columns = {0: "Predicted GDP"})
    if pd.Timestamp(date) == start_of_this_quarter_date:
        y.iloc[-1] = np.nan
    y = y.to_frame().rename(columns = {0: "Actual GDP", "pct_chg": "Actual GDP"})
    df = pd.concat([y, predicted_values], axis = 1)
    df.index = pd.to_datetime(df.index).to_period('Q')
    return df

