from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2011-07-01"

df = get_most_recent_series_of_date("ANDENO", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

pct_chg_nondefense_capital_goods = transform_series(df, 5).dropna()
# print(pct_chg_nondefense_capital_goods)
# pct_chg_nondefense_capital_goods.plot()
# plt.show()

# print("ADF Test Result: ", adfuller(pct_chg_nondefense_capital_goods))
# plot_acf_pacf(pct_chg_nondefense_capital_goods)
# plt.show()

# gridsearch chosen base on pcf and acf
#seasonal order based on acf
best_arma(pct_chg_nondefense_capital_goods, trend='c', test_size=20, start_p= 0, start_q=0, max_p=6, max_q=6)
model = ARIMA(pct_chg_nondefense_capital_goods, order=(0, 0, 6), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(6+2, .01))

fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_nondefense_capital_goods)
plt.show()

# plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_nondefense_capital_goods.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_nondefense_capital_goods, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

def quart_pct_cap(date = "2020-01-01", period = 'Q'):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("ANDENO", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_fed_defence = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_fed_defence, order=(0, 0, 6), trend = 'c', freq = 'QS').fit(start_params = np.full(6+2, .01))
    start_date_pred = pct_chg_fed_defence.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_fed_defence, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage