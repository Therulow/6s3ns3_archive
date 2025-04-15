from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2007-12-01"

df = get_most_recent_series_of_date("BUSINV", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

pct_chg_business_inventories = transform_series(df, 5).dropna()
pct_chg_business_inventories.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_business_inventories, regression = 'c'))

plot_acf_pacf(pct_chg_business_inventories)
# plt.show()

# best_p, best_q = best_arma(pct_chg_business_inventories, max_p=7, start_q=3, max_q= 9, test_size = 10, trend = "c")

model = ARIMA(pct_chg_business_inventories, order=(5, 0, 8), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(20, .01))

fig, ax = plt.subplots()
ax.plot(model.fittedvalues, label = "fitted")
ax.plot(pct_chg_business_inventories, label = "actual")
ax.legend(loc="upper left")
plt.show()

plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

# start_date_pred = pct_chg_business_inventories.index[-1]+ pd.offsets.MonthBegin(1)
# end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

# #prediction
# pred = model.predict(start = start_date_pred, end = end_date_pred)

# pct_chg_pred = pd.concat([pct_chg_business_inventories, pred])

# quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_business_inventories(date = "2020-01-01", period = 'Q'):
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSINV", date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_business_inventories = transform_series(df, 5).dropna().diff().dropna()*100
    model = ARIMA(pct_chg_business_inventories, order=(2, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(2+1+1, .01))
    start_date_pred = pct_chg_business_inventories.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_inventories, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':
        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage