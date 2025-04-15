from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

get_date = "2007-12-01"
df = get_most_recent_series_of_date("HOUST", get_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

pct_chg_housing_units_started = transform_series(df, 4)
pct_chg_housing_units_started.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_housing_units_started))
# plot_acf_pacf(pct_chg_housing_units_started )
# plt.show() 

# best_p, best_q = best_arma(pct_chg_housing_units_started, max_p = 5,start_q=15,  max_q = 17, trend = "c", test_size = 10) ## best p and q are 1 and 1 respectively
model = ARIMA(pct_chg_housing_units_started, order=(3, 0, 16), trend = 'n', freq = 'MS')
model = model.fit(start_params = np.full(25, .01))

# fig, ax = plt.subplots()
# ax.plot(model.fittedvalues, label = "fitted")
# ax.plot(pct_chg_housing_units_started, label = "actual")
# ax.legend(loc="upper left")
# plt.show()

# plot_acf_pacf(model.resid)
# plt.plot(model.resid)
# plt.show()

start_date_pred = pct_chg_housing_units_started.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(pct_chg_housing_units_started, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_housing_units_started, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_chg_housing_units_started(given_date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("HOUST", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_housing_units_started = transform_series(df, 4).diff().dropna()*100
    model = ARIMA(pct_chg_housing_units_started, order=(1, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(1+1+1, .01))
    start_date_pred = pct_chg_housing_units_started.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_housing_units_started, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage