from package_imports import *

fred = Fred(api_key = os.getenv("API_KEY"))

given_date = "2008-01-01"
df = get_most_recent_series_of_date("IPBUSEQ", given_date, fred)
df = df[df.index<=pd.to_datetime("2007-06-01")]

pct_chg_business_equipment = transform_series(df, 5).dropna()
pct_chg_business_equipment.plot()
plt.show()

print("ADF Test Result: ", adfuller(pct_chg_business_equipment))

plot_acf_pacf(pct_chg_business_equipment)
plt.show() 

best_p, best_q = best_arma(pct_chg_business_equipment, max_p = 5, start_q=5, max_q = 8, test_size = 10, trend = "c")

model = ARIMA(pct_chg_business_equipment, order=(5, 0, 8), trend = 'c', freq = 'MS')
model = model.fit(start_params = np.full(20, .01))

fig, ax = plt.subplots()
ax.plot(model.fittedvalues, label = "fitted")
ax.plot(pct_chg_business_equipment, label = "actual")
ax.legend(loc="upper left")
plt.show()

plot_acf_pacf(model.resid)
plt.plot(model.resid)
plt.show()

start_date_pred = pct_chg_business_equipment.index[-1]+ pd.offsets.MonthBegin(1)
end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time

#prediction
pred = model.predict(start = start_date_pred, end = end_date_pred)

pct_chg_pred = pd.concat([pct_chg_business_equipment, pred])

quarterly_pct_chage = pct_chg_pred.resample('QS').sum()

# takes in the given dates and return values up to the date if have if not predict
#takes in given date and period, so 'Q' or 'M' for bridge or midas
def quart_pct_chg_biz_equip(date = "2020-01-01", period = 'Q'):
    given_date = "2020-01-01"
    fred = Fred(api_key = os.getenv("API_KEY"))
    df = get_most_recent_series_of_date("IPBUSEQ", given_date, fred)
    df = df[df.index<pd.Timestamp(date).to_period('M').start_time - pd.offsets.MonthBegin(1)]
    pct_chg_business_equipment = transform_series(df, 5).dropna().diff().dropna()*100
    model = ARIMA(pct_chg_business_equipment, order=(5, 0, 1), trend = 'n', freq = 'MS').fit(start_params = np.full(5+1+1, .01))
    start_date_pred = pct_chg_business_equipment.index[-1]+ pd.offsets.MonthBegin(1)
    end_date_pred = pd.Period(given_date, freq='Q').end_time.to_period(freq='M').start_time
    pred = model.predict(start = start_date_pred, end = end_date_pred)
    pct_chg_pred = pd.concat([pct_chg_business_equipment, pred])
    if period == 'M':
        return pct_chg_pred
    elif period == 'Q':

        quarterly_pct_chage = pct_chg_pred.resample('QS').sum()
        return quarterly_pct_chage