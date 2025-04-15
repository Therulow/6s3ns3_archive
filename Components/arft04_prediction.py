from Components.package_imports import *
from Components.data_load import load_data_bridge
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

def arft04_benchmark_prediction_df(date):
    X, y = load_data_bridge(date)
    y.index = pd.to_datetime(y.index).to_period('Q')
    model =  AutoReg(y, lags = 4, trend = 'ct').fit()

    # start_of_this_quarter_date = pd.Period(date, freq='Q').start_time
    # if pd.Timestamp(date) == start_of_this_quarter_date:
    #     y.iloc[-1] = np.nan

    df = y.to_frame().rename(columns = {0: "Actual GDP", "pct_chg": "Actual GDP"})
    predicted_gdp_values =  pd.concat([model.fittedvalues, model.predict(len(y), end = len(y))]).to_frame().rename(columns = {0: "Predicted GDP"})
    start_of_this_quarter_date = pd.Period(date, freq='Q').start_time
    if pd.Timestamp(date) == start_of_this_quarter_date:
        df["Actual GDP"].iloc[-1] = np.nan
    df = pd.concat([df, predicted_gdp_values], axis = 1)
    df = df.to_timestamp()
    df.index = df.index.to_period("Q")
    return df
