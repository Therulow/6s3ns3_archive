from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2011-07-01"

df = get_most_recent_series_of_date("TLPBLCONS", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

## need to double check the correct transformation for this
pct_chg_govt_construction = transform_series(df, 5).dropna()*100
pct_chg_govt_construction.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_govt_construction, regression="c"))
print("ADF Test Result: ", adfuller(transform_series(pct_chg_govt_construction, 5).dropna(), regression="c"))
plot_acf_pacf(pct_chg_govt_construction)
plt.show()

# best_arma(pct_chg_govt_construction, trend='c', test_size=10, start_p= 0, start_q=0, max_p=5, max_q=5)
# best arma p=5, q=5, but gridsearch chosen base on pcf and acf, p=1, q=1
model = ARIMA(pct_chg_govt_construction, order=(1, 0, 1), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(1+1+1+1, .01))

fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_govt_construction)
plt.show()

plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_govt_construction.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_govt_construction, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_govt_constr(date = "2020-01-01", period = 'Q'):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("TLPBLCONS", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_govt_constr = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_govt_constr, order=(1, 0, 1), trend = 'c', freq = 'MS').fit(start_params = np.full(1+1+1+1, .01))
    start_date_pred = pct_chg_govt_constr.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_govt_constr, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage