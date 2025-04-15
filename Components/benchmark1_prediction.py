from Components.package_imports import *
from Components.data_load import load_data_bridge
import datetime
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

fred = Fred(api_key = os.getenv("API_KEY"))

def mean_benchmark_prediction_df(date):
    X, y = load_data_bridge(date)
    mean_value = y.mean()
    start_of_this_quarter_date = pd.Period(date, freq='Q').start_time
    if pd.Timestamp(date) == start_of_this_quarter_date:
        y.iloc[-1] = np.nan
    y = y.to_frame().rename(columns = {0: "Actual GDP", "pct_chg": "Actual GDP"})
    y["Predicted GDP"] = mean_value
    y = pd.concat([y, pd.DataFrame({"Actual GDP": [np.nan], "Predicted GDP": [mean_value]}, index = [start_of_this_quarter_date])])
    y.index = pd.to_datetime(y.index).to_period('Q')
    return y

# def benchmark1_prediction(date = datetime.date.today()):
#     train = get_most_recent_series_of_date("GDP", date, fred)
#     train = pct_chg(train)

#     train = train["pct_chg"]
#     train = train.to_frame()
#     train["Indicator"] = "Actual"

#     start_date_pred = train.index[-1] + pd.offsets.QuarterBegin(1, startingMonth= 1)
#     end_date_pred = pd.Period(date, freq='Q').start_time

#     quarter_intervals = pd.date_range(start = start_date_pred, end = end_date_pred, freq = pd.offsets.QuarterBegin(1, startingMonth= 1))

#     for quarter in quarter_intervals:
#         mean = train["pct_chg"].mean()
#         row = pd.DataFrame({"pct_chg": mean, "Indicator": "Forecast"}, index = [quarter])
#         train = pd.concat([train, row])

    
#     train.index = pd.to_datetime(train.index).to_period('Q')
#     train["quarters"] = train.index.astype(str)

#     train = train.reset_index(drop = True)

#     return train

# print((benchmark1_prediction()))