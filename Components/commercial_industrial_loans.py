from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2007-12-01"
df = get_most_recent_series_of_date("BUSLOANS", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]
print(df)

pct_chg_commercial_industrial_loans = transform_series(df, 5).dropna()
pct_chg_commercial_industrial_loans.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_commercial_industrial_loans, regression="c"))
plot_acf_pacf(pct_chg_commercial_industrial_loans)
plt.show()

# best_arma(pct_chg_commercial_industrial_loans, trend='c', test_size=10, start_p= 0, start_q=10, max_p=5, max_q=12)
# best arma: p= 2, q =1

model = ARIMA(pct_chg_commercial_industrial_loans, order=(2, 0, 12), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(2+1+12+2, .01))

fig, ax = plt.subplots()
ax.plot(model.fittedvalues)
ax.plot(pct_chg_commercial_industrial_loans)
plt.show()

plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_commercial_industrial_loans.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_commercial_industrial_loans, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_comm_loans(date = "2020-01-01", period = 'Q'):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("BUSLOANS", given_date, fred)
    df = df[df.index<pd.Timestamp(given_date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_comms_loans = transform_series(df, 5).dropna()*100
    model = ARIMA(pct_chg_comms_loans, order=(2, 0, 12), trend = 'c', freq = 'QS').fit(start_params = np.full(5+5+1+1, .01))
    start_date_pred = pct_chg_comms_loans.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_comms_loans, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage