from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2007-12-01"

df = get_most_recent_series_of_date("FDEFX", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]
# print(df)

#transform series
pct_chg_fed_defence = transform_series(df, 5).dropna()*100
# pct_chg_fed_defence.plot()
# plt.show()
# outlier in 1951 due to Korean War, to keep data from 1952 onwards
pct_chg_fed_defence = pct_chg_fed_defence[pct_chg_fed_defence.index >= pd.to_datetime("1952-01-01")]
# pct_chg_fed_defence.plot()
# plt.show()



#checking for stationarity
# print("ADF Test Result: ", adfuller(pct_chg_fed_defence, regression="c"))
# plot_acf_pacf(pct_chg_fed_defence)
# plt.show()


# best_arma(pct_chg_fed_defence, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5, freq="QS")
# best arma: p=2, q=3
model = ARIMA(pct_chg_fed_defence, order=(2, 0, 3), trend = 'c', freq = 'QS')
model = model.fit(start_params = np.full(2+3+1+1, .01))

# fig, ax = plt.subplots()
# ax.plot(model.fittedvalues)
# ax.plot(pct_chg_fed_defence)
# plt.show()

plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.QuarterBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

quarterly_pct_chage = pd.concat([pct_chg_fed_defence, pred])

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_defence(date = "2020-01-01"):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("FDEFX", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(2, 0, 3), trend = 'c', freq = 'QS').fit(start_params = np.full(2+3+1+1, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.QuarterBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    quarterly_pct_chage = pd.concat([pct_chg_fed_defence, pred])
    return quarterly_pct_chage